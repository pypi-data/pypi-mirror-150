from hestia_earth.schema import SiteSiteType

from hestia_earth.models.log import logger
from . import MODEL

MODEL_KEY = 'excretaManagement'


def run(cycle: dict):
    site_type = cycle.get('site', {}).get('siteType')
    is_complete = all([site_type == SiteSiteType.CROPLAND.value])
    logger.debug('model=%s, key=%s, value=%s', MODEL, MODEL_KEY, is_complete)
    return is_complete
