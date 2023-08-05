from hestia_earth.schema import NodeType, TermTermType, SiteSiteType
from hestia_earth.utils.model import find_term_match, find_primary_product
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import non_empty_list
from hestia_earth.distribution.cycle import (
    group_cycle_inputs, get_input_group, FERTILISER_COLUMNS, PESTICIDE_COLUMN, IRRIGATION_COLUMN
)
from hestia_earth.distribution.posterior_fert import get_post as get_post_fert
from hestia_earth.distribution.prior_fert import get_prior as get_prior_fert
from hestia_earth.distribution.posterior_pest import get_post as get_post_pest
from hestia_earth.distribution.prior_pest import get_prior as get_prior_pest
from hestia_earth.distribution.posterior_irrigation import get_post as get_post_irri
from hestia_earth.distribution.prior_irrigation import get_prior as get_prior_irri
from hestia_earth.validation.log import logger
from hestia_earth.validation.utils import _filter_list_errors, update_error_path, is_live_animal_cycle
from hestia_earth.validation.distribution import UNIVARIATE_DEFAULT_THRESHOLD, validate as validate_distribution
from .shared import validate_country

MUST_INCLUDE_ID_COL = column_name('mustIncludeId')
MUST_INCLUDE_ID_TERM_TYPES = [
    TermTermType.INORGANICFERTILISER.value
]
FEED_TERM_TYPES = [
    TermTermType.CROP.value,
    TermTermType.ANIMALPRODUCT.value,
    TermTermType.FEEDFOODADDITIVE.value,
    TermTermType.FORAGE.value,
    TermTermType.LIVEAQUATICSPECIES.value
]
FEED_SITE_TYPE = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.PERMANENT_PASTURE.value,
    SiteSiteType.ANIMAL_HOUSING.value
]
CROP_SITE_TYPE = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.GLASS_OR_HIGH_ACCESSIBLE_COVER.value
]


def validate_must_include_id(inputs: list):
    def missingRequiredIds(term: dict):
        term_id = term.get('@id')
        lookup = download_lookup(f"{term.get('termType')}.csv")
        other_term_ids = (get_table_value(lookup, 'termid', term_id, MUST_INCLUDE_ID_COL) or '').split(',')
        return non_empty_list([
            term_id for term_id in other_term_ids if find_term_match(inputs, term_id, None) is None
        ])

    def validate(values: tuple):
        index, input = values
        term = input.get('term', {})
        should_validate = term.get('termType') in MUST_INCLUDE_ID_TERM_TYPES
        missing_ids = missingRequiredIds(term) if should_validate else []
        return len(missing_ids) == 0 or {
            'level': 'warning',  # added gap-filling which makes it non-required anymore
            'dataPath': f".inputs[{index}]",
            'message': f"should add missing inputs: {', '.join(missing_ids)}"
        }

    return _filter_list_errors(map(validate, enumerate(inputs)))


def validate_input_country(node: dict, list_key: list = 'inputs'):
    def validate(values: tuple):
        index, input = values
        country = input.get('country')
        error = country is None or validate_country(input)
        return error is True or update_error_path(error, list_key, index)

    return _filter_list_errors(map(validate, enumerate(node.get(list_key, []))))


def validate_related_impacts(node: dict, list_key: list, node_map: dict = {}):
    related_impacts = node_map.get(NodeType.IMPACTASSESSMENT.value)

    def validate(values: tuple):
        index, input = values
        impact_id = input.get('impactAssessment', {}).get('id')
        impact = related_impacts.get(impact_id) if impact_id else None
        related_node_id = impact.get(node.get('type').lower(), {}).get('id') if impact else None
        return related_node_id is None or related_node_id != node.get('id') or {
            'level': 'error',
            'dataPath': f".inputs[{index}].impactAssessment",
            'message': f"can not be linked to the same {node.get('type')}"
        }

    return _filter_list_errors(map(validate, enumerate(node.get(list_key, [])))) if related_impacts else True


def _get_stats_by_group_key(key: str, country_id: str, product_id: str, input_id: str):
    if key in FERTILISER_COLUMNS:
        mu, sd = get_post_fert(country_id, product_id, input_id)
        return (mu, sd) if mu is not None else get_prior_fert(country_id, input_id)
    elif key == PESTICIDE_COLUMN:
        mu, sd = get_post_pest(country_id, product_id)
        return (mu, sd) if mu is not None else get_prior_pest(country_id)
    elif key == IRRIGATION_COLUMN:
        mu, sd = get_post_irri(country_id, product_id)
        return (mu, sd) if mu is not None else get_prior_irri(country_id)


def _completeness_key(key: str):
    return 'fertiliser' if key in FERTILISER_COLUMNS else (
        'pesticidesAntibiotics' if key == PESTICIDE_COLUMN
        else 'water' if key == IRRIGATION_COLUMN
        else ''
    )


def _validate_input_value(cycle: dict, country: dict, list_key: str, threshold: float):
    groups = group_cycle_inputs(cycle)
    completeness = cycle.get('completeness', {})
    country_id = country.get('@id')
    product = find_primary_product(cycle) or {}
    product_id = product.get('term', {}).get('@id')

    def validate(values: tuple):
        index, input = values

        input_id = input.get('term', {}).get('@id')
        group_key = get_input_group(input)
        input_value = groups.get(group_key)

        def _get_mu_sd():
            return _get_stats_by_group_key(group_key, country_id, product_id, input_id)

        complete = completeness.get(_completeness_key(group_key), False)
        valid, outliers, min, max = (validate_distribution([input_value], threshold, get_mu_sd=_get_mu_sd)
                                     if complete else (True, None, None, None))

        return valid or {
            'level': 'warning',
            'dataPath': f".{list_key}[{index}].value",
            'message': 'is outside confidence interval',
            'params': {
                'term': input.get('term', {}),
                'group': group_key,
                'country': country,
                'outliers': outliers,
                'threshold': threshold,
                'min': min,
                'max': max
            }
        }
    return validate


def validate_input_distribution_value(
    cycle: dict, site: dict, list_key: str = 'inputs', threshold: float = UNIVARIATE_DEFAULT_THRESHOLD
):
    try:
        country = site.get('country', {})
        inputs = cycle.get(list_key, [])
        validate_input = _validate_input_value(cycle, country, list_key, threshold)
        return site.get('siteType') not in CROP_SITE_TYPE or _filter_list_errors(map(validate_input, enumerate(inputs)))
    except Exception as e:
        logger.error(f"Error validating using distribution: '{str(e)}'")
        return True


def validate_animalFeed_requires_isAnimalFeed(cycle: dict, site: dict, list_key: str = 'inputs'):
    site_type = site.get('siteType')
    is_liveAnimal = is_live_animal_cycle(cycle)

    def validate(values: tuple):
        index, input = values
        term_type = input.get('term', {}).get('termType')
        return term_type not in FEED_TERM_TYPES or input.get('isAnimalFeed') is not None or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}]",
            'message': 'must specify is it an animal feed'
        }

    return site_type not in FEED_SITE_TYPE or not is_liveAnimal or \
        _filter_list_errors(map(validate, enumerate(cycle.get(list_key, []))))
