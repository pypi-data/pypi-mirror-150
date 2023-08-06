from hestia_earth.schema import PracticeStatsDefinition
from hestia_earth.utils.tools import non_empty_list, safe_parse_float

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.practice import _new_practice
from hestia_earth.models.utils.dataCompleteness import _is_term_type_incomplete
from hestia_earth.models.utils.cycle import valid_site_type
from hestia_earth.models.utils.crop import get_crop_lookup_value
from . import MODEL

TERM_ID = 'orchardDensity'
LOOKUP_COL = 'Orchard_density'


def _get_value(product: dict):
    term_id = product.get('term', {}).get('@id', '')
    return safe_parse_float(get_crop_lookup_value(MODEL, term_id, LOOKUP_COL), None)


def _practice(value: float):
    practice = _new_practice(TERM_ID, MODEL)
    practice['value'] = [value]
    practice['statsDefinition'] = PracticeStatsDefinition.MODELLED.value
    return practice


def _run(cycle: dict):
    def run_product(product):
        value = _get_value(product)
        return None if value is None else _practice(value)

    return non_empty_list(map(run_product, cycle.get('products', [])))


def _should_run(cycle: dict):
    term_type_incomplete = _is_term_type_incomplete(cycle, TERM_ID)
    site_type_valid = valid_site_type(cycle)

    logRequirements(model=MODEL, term=TERM_ID,
                    term_type_incomplete=term_type_incomplete,
                    site_type_valid=site_type_valid)

    should_run = all([site_type_valid, term_type_incomplete])
    logShouldRun(MODEL, TERM_ID, should_run)
    return should_run


def run(cycle: dict): return _run(cycle) if _should_run(cycle) else []
