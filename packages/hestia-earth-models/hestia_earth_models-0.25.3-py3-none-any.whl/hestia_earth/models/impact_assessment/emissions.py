from functools import reduce
from hestia_earth.schema import IndicatorStatsDefinition
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.impact_assessment import get_product, convert_value_from_cycle
from hestia_earth.models.utils.indicator import _new_indicator
from . import MODEL


def _indicator(term_id: str, value: float):
    indicator = _new_indicator(term_id)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator


def _run_emission(product: dict):
    def run(group: dict, emission: dict):
        emission_value = list_sum(emission.get('value', [0]))
        value = convert_value_from_cycle(product, emission_value)
        term_id = emission.get('term', {}).get('@id')
        logShouldRun(MODEL, emission.get('term', {}).get('@id'), True)
        return {**group, **({term_id: (group.get(term_id, 0) + value)} if value is not None else {})}
    return run


def _should_run_emission(emission: dict): return emission.get('deleted', False) is not True


def _should_run(impact_assessment: dict):
    product = get_product(impact_assessment)
    product_id = product.get('term', {}).get('@id')
    logRequirements(model=MODEL, key='emissions',
                    product=product_id)
    should_run = product_id is not None
    logShouldRun(MODEL, None, should_run, key='emissions')
    return should_run, product


def run(impact_assessment: dict):
    should_run, product = _should_run(impact_assessment)
    emissions = list(filter(_should_run_emission, impact_assessment.get('cycle', {}).get('emissions', [])))
    emissions = reduce(_run_emission(product), emissions, {}) if should_run else {}
    return [_indicator(id, value) for id, value in emissions.items()]
