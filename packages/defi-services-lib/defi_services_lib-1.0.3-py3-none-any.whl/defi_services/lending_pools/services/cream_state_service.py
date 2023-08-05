import logging

from defi_services.abis.erc20_abi import ERC20_ABI
from defi_services.abis.lending_pool.cream_comptroller_abi import CREAM_COMPTROLLER_ABI
from defi_services.abis.lending_pool.cream_lens_abi import CREAM_LENS_ABI
from defi_services.abis.lending_pool.ctoken_abi import CTOKEN_ABI
from defi_services.constants.contract_address import ContractAddresses, AbnormalCreamPool
from defi_services.constants.db_constant import DBConst
from defi_services.state_service import StateService
from defi_services.utils.batch_queries_service import add_rpc_call, decode_data_response

_LOGGER = logging.getLogger("TravaVaultSS")


class CreamStateService(StateService):
    def __init__(self, provider_uri):
        super().__init__(provider_uri)

    def ctoken_metadata_all(
            self, lens_address: str, lens_abi: list, token_addresses: list, block_number: int = 'latest'):
        lens_contract = self._w3.eth.contract(
            address=self.to_checksum(lens_address), abi=lens_abi
        )
        tokens = [self.to_checksum(i) for i in token_addresses]
        reserve_tokens_info = lens_contract.functions.cTokenMetadataAll(tokens).call(block_identifier=block_number)
        return reserve_tokens_info

    def ctoken_underlying_price_all(
            self, lens_address: str, lens_abi: list, token_addresses: list, bnb_price: float,
            block_number: int = 'latest'):
        lens_contract = self._w3.eth.contract(
            address=self.to_checksum(lens_address), abi=lens_abi
        )
        tokens = [self.to_checksum(i) for i in token_addresses]
        reserve_tokens_info = lens_contract.functions.cTokenUnderlyingPriceAll(tokens).call(
            block_identifier=block_number)
        for price_token in reserve_tokens_info:
            reserve_tokens_info[price_token[0].lower()] = price_token[1] * bnb_price
        return reserve_tokens_info

    def get_all_markets(
            self, comptroller: str, comptroller_abi: list, block_number: int = 'latest'):
        comptroller_contract = self._w3.eth.contract(
            address=self._w3.toChecksumAddress(comptroller), abi=comptroller_abi)
        tokens = []
        for token in comptroller_contract.functions.getAllMarkets().call(block_identifier=block_number):
            if token in [ContractAddresses.LUNA.lower(), ContractAddresses.UST.lower(), ContractAddresses.LUNA,
                         ContractAddresses.UST]:
                continue
            tokens.append(token)
        return tokens

    @staticmethod
    def _encode_apy_lending_pool_function_call(
            lens_address: str,
            lens_abi: list,
            comptroller_address: str,
            comptroller_abi: list,
            token_addresses: list,
            block_number: int = "latest"
    ):
        list_call_id, list_rpc_call = [], []
        for token_address in token_addresses:
            add_rpc_call(
                abi=comptroller_abi, fn_name='compSpeeds', contract_address=comptroller_address,
                block_number=block_number, fn_paras=token_address, list_rpc_call=list_rpc_call,
                list_call_id=list_call_id
            )
            add_rpc_call(
                abi=comptroller_abi, fn_name='mintGuardianPaused', contract_address=comptroller_address,
                block_number=block_number, fn_paras=token_address, list_rpc_call=list_rpc_call,
                list_call_id=list_call_id
            )
            add_rpc_call(
                abi=comptroller_abi, fn_name='borrowGuardianPaused', contract_address=comptroller_address,
                block_number=block_number, fn_paras=token_address, list_rpc_call=list_rpc_call,
                list_call_id=list_call_id
            )
            add_rpc_call(abi=lens_abi, contract_address=lens_address, fn_paras=token_address, block_number=block_number,
                         list_call_id=list_call_id, list_rpc_call=list_rpc_call, fn_name="cTokenMetadata")
            add_rpc_call(abi=lens_abi, contract_address=lens_address, fn_paras=token_address,
                         block_number=block_number,
                         list_call_id=list_call_id, list_rpc_call=list_rpc_call, fn_name="cTokenUnderlyingPrice")
        return list_rpc_call, list_call_id

    def _decode_apy_lending_pool_function_call(
            self,
            list_rpc_call: list,
            list_call_id: list,
            lens_address: str,
            comptroller_address: str,
            token_addresses: list,
            block_number: int = "latest",
            wrapped_native_token_price: float = 310,
    ):
        data_response = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=100)
        decoded_data = decode_data_response(data_response, list_call_id)
        underlying_prices, reserve_tokens_info = {}, []
        ctoken_speeds, borrow_paused_tokens, mint_paused_tokens = {}, {}, {}
        for token_address in token_addresses:
            lower_address = token_address.lower()
            speeds_call_id = f'compSpeeds_{comptroller_address}_{token_address}_{block_number}'.lower()
            borrow_guardian_paused_call_id = f'borrowGuardianPaused_{comptroller_address}_{token_address}_{block_number}'.lower()
            mint_guardian_paused_call_id = f'mintGuardianPaused_{comptroller_address}_{token_address}_{block_number}'.lower()
            ctoken_speeds[lower_address] = decoded_data.get(speeds_call_id)
            borrow_paused_tokens[lower_address] = decoded_data.get(borrow_guardian_paused_call_id)
            mint_paused_tokens[lower_address] = decoded_data.get(mint_guardian_paused_call_id)
            metadata_id = f"cTokenMetadata_{lens_address}_{token_address}_{block_number}".lower()
            reserve_tokens_info.append(decoded_data.get(metadata_id))
            underlying_id = f"cTokenUnderlyingPrice_{lens_address}_{token_address}_{block_number}".lower()
            price_token = decoded_data.get(underlying_id)
            underlying_prices[lower_address] = price_token[1] * wrapped_native_token_price
            if lower_address in AbnormalCreamPool.decimals.keys():
                underlying_prices[lower_address] /= 10 ** AbnormalCreamPool.decimals.get(lower_address)
        return {
            "reserve_tokens_info": reserve_tokens_info,
            "ctoken_speeds": ctoken_speeds,
            "borrow_paused_tokens": borrow_paused_tokens,
            "mint_paused_tokens": mint_paused_tokens,
            "underlying_prices": underlying_prices
        }

    def get_apy_lending_pool(
            self,
            lens_address: str,
            comptroller_address: str,
            pool_token_price: float,
            lens_abi: list = CREAM_LENS_ABI,
            comptroller_abi: list = CREAM_COMPTROLLER_ABI,
            pool_decimals: int = 18,
            block_number: int = "latest",
            wrapped_native_token_price: float = 310
    ):
        tokens_interest_rates = dict()
        ctokens = self.get_all_markets(comptroller_address, comptroller_abi, block_number)
        for token in ctokens:
            if token in [ContractAddresses.LUNA.lower(), ContractAddresses.UST.lower(), ContractAddresses.LUNA,
                         ContractAddresses.UST]:
                ctokens.remove(token)
        list_rpc_call, list_call_id = self._encode_apy_lending_pool_function_call(
            lens_address, lens_abi, comptroller_address, comptroller_abi, ctokens, block_number)
        decode_data = self._decode_apy_lending_pool_function_call(
            list_rpc_call, list_call_id, lens_address, comptroller_address, ctokens, block_number,
            wrapped_native_token_price)
        mint_paused_tokens = decode_data["mint_paused_tokens"]
        borrow_paused_tokens = decode_data["borrow_paused_tokens"]
        reserve_tokens_info = decode_data["reserve_tokens_info"]
        ctoken_speeds = decode_data["ctoken_speeds"]
        for data in reserve_tokens_info:
            address = data[0].lower()
            underlying_token_price = float(decode_data["underlying_prices"][address]) / 10 ** int(data[13])
            token_info = {
                "token": address,
                "token_decimals": data[12],
                "borrow_rate": data[3],
                "supply_rate": data[2],
                "supply": data[7],
                "borrow": data[5],
                "exchange_rate": data[1],
                "underlying": data[11].lower(),
                "underlying_price": underlying_token_price,
                "underlying_decimals": data[13],
                "speed": ctoken_speeds[address]
            }
            underlying_token = token_info['underlying']
            token_info["mint_paused"] = mint_paused_tokens[address]
            token_info["borrow_paused"] = borrow_paused_tokens[address]
            tokens_interest_rates[underlying_token] = self._calculate_interest_rates(
                token_info, pool_decimals, pool_token_price)

        return tokens_interest_rates

    def get_token_speed(self, token_addresses: list, comptroller: str, comptroller_abi: list = CREAM_COMPTROLLER_ABI,
                        block_number: int = 'latest'):
        list_rpc_call = []
        list_call_id = []
        for token_address in token_addresses:
            add_rpc_call(
                abi=comptroller, fn_name='compSpeeds', contract_address=comptroller_abi,
                block_number=block_number, fn_paras=token_address, list_rpc_call=list_rpc_call,
                list_call_id=list_call_id
            )
        data_response = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=100)
        decoded_data = decode_data_response(data_response, list_call_id)
        result = {}
        for token_address in token_addresses:
            get_asset_data_call_id = f'compSpeeds_{comptroller}_{token_address}_{block_number}'.lower()
            result[token_address.lower()] = decoded_data.get(get_asset_data_call_id)

        return result

    def mint_guardian_paused(
            self, token_addresses: list, comptroller: str, comptroller_abi: list, block_number: int = "latest"):
        list_rpc_call = []
        list_call_id = []
        for token_address in token_addresses:
            add_rpc_call(
                abi=comptroller, fn_name='mintGuardianPaused', contract_address=comptroller_abi,
                block_number=block_number, fn_paras=token_address, list_rpc_call=list_rpc_call,
                list_call_id=list_call_id
            )
        data_response = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=100)
        decoded_data = decode_data_response(data_response, list_call_id)
        result = {}
        for token_address in token_addresses:
            get_asset_data_call_id = f'mintGuardianPaused_{comptroller}_{token_address}_{block_number}'.lower()
            result[token_address.lower()] = decoded_data.get(get_asset_data_call_id)

        return result

    def borrow_guardian_paused(
            self, token_addresses: list, comptroller: str, comptroller_abi: list, block_number: int = "latest"):
        list_rpc_call = []
        list_call_id = []
        for token_address in token_addresses:
            add_rpc_call(
                abi=comptroller, fn_name='borrowGuardianPaused', contract_address=comptroller_abi,
                block_number=block_number, fn_paras=token_address, list_rpc_call=list_rpc_call,
                list_call_id=list_call_id
            )
        data_response = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=100)
        decoded_data = decode_data_response(data_response, list_call_id)
        result = {}
        for token_address in token_addresses:
            get_asset_data_call_id = f'borrowGuardianPaused_{comptroller}_{token_address}_{block_number}'.lower()
            result[token_address.lower()] = decoded_data.get(get_asset_data_call_id)

        return result

    @staticmethod
    def _calculate_interest_rates(token_info: dict, pool_decimals: int, pool_price: float):
        apx_block_speed_in_seconds = 3
        exchange_rate = float(token_info["exchange_rate"]) / 10 ** pool_decimals
        block_per_day = int(60 * 60 * 24 / apx_block_speed_in_seconds)
        venus_per_day = token_info["speed"] * block_per_day / 10 ** pool_decimals
        underlying_price = float(token_info["underlying_price"])
        total_borrow = float(token_info["borrow"]) / 10 ** int(token_info["underlying_decimals"])
        total_supply = float(token_info["supply"]) * exchange_rate / 10 ** int(token_info["underlying_decimals"])
        total_borrow_usd = total_borrow * underlying_price
        total_supply_usd = total_supply * underlying_price

        if total_borrow_usd == 0:
            borrow_apr = 0
        else:
            borrow_apr = (1 + (pool_price * venus_per_day / total_borrow_usd)) ** 365 - 1

        if total_supply_usd == 0:
            supply_apr = 0
        else:
            supply_apr = (1 + (pool_price * venus_per_day / total_supply_usd)) ** 365 - 1

        supply_apy = ((token_info["supply_rate"] / 10 ** pool_decimals) * block_per_day + 1) ** 365 - 1
        borrow_apy = ((token_info["borrow_rate"] / 10 ** pool_decimals) * block_per_day + 1) ** 365 - 1

        liquidity_log = {
            DBConst.total_borrow: {
                DBConst.amount: total_borrow,
                DBConst.value_in_usd: total_borrow_usd
            },
            DBConst.total_deposit: {
                DBConst.amount: total_supply,
                DBConst.value_in_usd: total_supply_usd
            }
        }
        return {
            DBConst.reward_borrow_apy: borrow_apr,
            DBConst.reward_deposit_apy: supply_apr,
            DBConst.deposit_apy: supply_apy,
            DBConst.borrow_apy: borrow_apy,
            DBConst.liquidity_change_logs: liquidity_log,
            DBConst.mint_paused: token_info[DBConst.mint_paused],
            DBConst.borrow_paused: token_info[DBConst.borrow_paused]
        }

    def get_rewards_balance(
            self,
            wallet_address: str,
            lens_address: str,
            comptroller_implementation_address: str,
            pool_token: str,
            lens_abi: list = CREAM_LENS_ABI,
            block_number: int = "latest",
    ):
        list_rpc_call = []
        list_call_id = []
        fn_paras = [self.to_checksum(pool_token),
                    self.to_checksum(comptroller_implementation_address),
                    self.to_checksum(wallet_address)]
        add_rpc_call(abi=lens_abi,
                     fn_paras=fn_paras,
                     contract_address=lens_address,
                     fn_name="getCompBalanceMetadataExt", block_number=block_number,
                     list_call_id=list_call_id, list_rpc_call=list_rpc_call)
        get_reward_id = f"getCompBalanceMetadataExt_{lens_address}_{fn_paras}_{block_number}".lower()
        data_response = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=100)
        decoded_data = decode_data_response(data_response, list_call_id)
        reward = decoded_data[get_reward_id][-1] / 10 ** 18
        return reward

    def get_wallet_deposit_borrow_balance(
            self,
            wallet_address: str,
            lens_address: str,
            reserves_info: dict,
            lens_abi: list = CREAM_LENS_ABI,
            block_number: int = "latest",
            wrapped_native_token_price: float = 310,
    ):
        list_rpc_call = []
        list_call_id = []
        for token in reserves_info:
            underlying = token
            value = reserves_info[token]
            if token == ContractAddresses.BNB:
                underlying = ContractAddresses.WBNB
            add_rpc_call(abi=lens_abi, contract_address=lens_address, fn_paras=value["cToken"],
                         block_number=block_number,
                         list_call_id=list_call_id, list_rpc_call=list_rpc_call, fn_name="cTokenUnderlyingPrice")
            add_rpc_call(abi=CTOKEN_ABI, contract_address=value["cToken"], fn_name="borrowBalanceCurrent",
                         block_number=block_number,
                         fn_paras=wallet_address, list_call_id=list_call_id, list_rpc_call=list_rpc_call)
            add_rpc_call(abi=CTOKEN_ABI, contract_address=value["cToken"], fn_name="balanceOfUnderlying",
                         block_number=block_number,
                         fn_paras=wallet_address, list_call_id=list_call_id, list_rpc_call=list_rpc_call)
            add_rpc_call(abi=ERC20_ABI, contract_address=underlying, fn_name="decimals", block_number=block_number,
                         list_call_id=list_call_id, list_rpc_call=list_rpc_call)

        data_response = self.client_querier.sent_batch_to_provider(list_rpc_call, batch_size=100)
        decoded_data = decode_data_response(data_response, list_call_id)
        total_borrow, result = 0, {
            "borrow_amount_in_usd": 0,
            "deposit_amount_in_usd": 0,
            "health_factor": 0,
            'reserves_data': {}
        }
        for token in reserves_info:
            underlying = token
            value = reserves_info[token]
            if token == ContractAddresses.BNB:
                underlying = ContractAddresses.WBNB
            get_total_deposit_id = f"balanceOfUnderlying_{value['cToken']}_{wallet_address}_{block_number}".lower()
            get_total_borrow_id = f"borrowBalanceCurrent_{value['cToken']}_{wallet_address}_{block_number}".lower()
            get_decimals_id = f"decimals_{underlying}_{block_number}".lower()
            decimals = decoded_data[get_decimals_id]
            deposit_amount = decoded_data[get_total_deposit_id] / 10 ** decimals
            borrow_amount = decoded_data[get_total_borrow_id] / 10 ** decimals
            get_underlying_token_price = f"cTokenUnderlyingPrice_{lens_address}_{value['cToken']}_{block_number}".lower()
            token_price = decoded_data.get(get_underlying_token_price)[1] * wrapped_native_token_price / 10 ** decimals
            deposit_amount_in_usd = deposit_amount * token_price
            borrow_amount_in_usd = borrow_amount * token_price
            total_borrow += borrow_amount_in_usd
            result['health_factor'] += deposit_amount_in_usd * value["liquidationThreshold"]
            result['borrow_amount_in_usd'] += borrow_amount_in_usd
            result['deposit_amount_in_usd'] += deposit_amount_in_usd
            if (borrow_amount > 0) or (deposit_amount > 0):
                result['reserves_data'][token] = {
                    "borrow_amount": borrow_amount,
                    "borrow_amount_in_usd": borrow_amount_in_usd,
                    "deposit_amount": deposit_amount,
                    "deposit_amount_in_usd": deposit_amount_in_usd,
                }
        if total_borrow != 0:
            result['health_factor'] /= total_borrow
        else:
            result['health_factor'] = 100
        return result
