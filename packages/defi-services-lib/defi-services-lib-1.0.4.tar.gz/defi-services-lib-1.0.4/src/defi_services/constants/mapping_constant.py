from defi_services.lending_pools.aave_v2_service import AaveV2Service
from defi_services.lending_pools.compound_service import CompoundService
from defi_services.lending_pools.cream_service import CreamService
from defi_services.lending_pools.geist_service import GeistService
from defi_services.lending_pools.radiant_service import RadiantService
from defi_services.lending_pools.trava_service import TravaService
from defi_services.lending_pools.valas_service import ValasService
from defi_services.lending_pools.venus_service import VenusService

LENDING_POOL_SERVICE = {
    "0x38": [TravaService, ValasService, VenusService, CreamService, RadiantService],
    "0xfa": [TravaService, GeistService],
    "0x1": [TravaService, AaveV2Service, CompoundService],
    "0x89": [AaveV2Service]
}
