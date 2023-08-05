from hestia_earth.schema import SiteSiteType, TermTermType
from hestia_earth.utils.tools import flatten, list_sum
from hestia_earth.utils.date import diff_in_days, is_in_days
from hestia_earth.utils.model import find_term_match, filter_list_term_type
from hestia_earth.utils.lookup import get_table_value, download_lookup, column_name

from hestia_earth.validation.utils import _find_linked_node, _value_average, _list_sum_terms
from hestia_earth.validation.terms import get_crop_residue_terms
from .shared import (
    validate_dates, validate_list_dates, validate_list_dates_after, validate_date_lt_today, validate_list_min_below_max,
    validate_list_term_percent, validate_linked_source_privacy, validate_list_dates_length, validate_list_date_lt_today,
    validate_list_model, validate_list_model_config, validate_list_dates_format,
    validate_list_duplicate_values, validate_private_has_source, validate_list_value_between_min_max
)
from .emission import validate_linked_terms, validate_method_not_relevant, validate_methodTier_not_relevant
from .input import (
    validate_must_include_id, validate_input_country, validate_related_impacts, validate_input_distribution_value,
    validate_animalFeed_requires_isAnimalFeed
)
from .practice import (
    validate_cropResidueManagement, validate_longFallowPeriod, validate_excretaManagement, validate_no_tillage,
    validate_tillage_site_type, validate_tillage_values, validate_liveAnimal_system, validate_pastureGrass_key_units,
    validate_has_pastureGrass, validate_pastureGrass_key_value
)
from .product import (
    validate_economicValueShare, validate_value_empty, validate_value_0, validate_excreta,
    validate_primary as validate_product_primary, validate_product_ha_functional_unit_ha, validate_product_yield
)
from .completeness import validate_completeness
from .transformation import (
    validate_previous_transformation, validate_transformation_excretaManagement, validate_linked_emission
)
from .property import (
    validate_valueType as validate_properties_valueType, validate_default_value as validate_properties_default_value,
    validate_volatileSolidsContent
)


SITE_TYPES_RESTRICTED = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.GLASS_OR_HIGH_ACCESSIBLE_COVER.value,
    SiteSiteType.PERMANENT_PASTURE.value
]
PRODUCTS_MODEL_CONFIG = {
    'aboveGroundCropResidueTotal': {
        'level': 'warning',
        'model': 'ipcc2006',
        'delta': 0.5,
        'resetDataCompleteness': True
    }
}


def validate_cycle_dates(cycle: dict):
    return validate_dates(cycle) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def _should_validate_cycleDuration(cycle: dict):
    return 'cycleDuration' in cycle and is_in_days(cycle.get('startDate')) and is_in_days(cycle.get('endDate'))


def validate_cycleDuration(cycle: dict):
    duration = diff_in_days(cycle.get('startDate'), cycle.get('endDate'))
    return duration == round(cycle.get('cycleDuration'), 1) or {
        'level': 'error',
        'dataPath': '.cycleDuration',
        'message': f"must equal to endDate - startDate in days (~{duration})"
    }


def validate_sum_aboveGroundCropResidue(products: list):
    prefix = 'aboveGroundCropResidue'
    total_residue_index = next((n for n in range(len(products)) if 'Total' in products[n].get(
        'term', {}).get('@id') and products[n].get('term', {}).get('@id').startswith(prefix)), None)
    total_residue = None if total_residue_index is None else _value_average(products[total_residue_index])

    other_residues = list(filter(lambda n: n.get('term').get('@id').startswith(prefix)
                                 and 'Total' not in n.get('term').get('@id'), products))
    other_residues_ids = list(map(lambda n: n.get('term').get('@id'), other_residues))
    other_sum = sum([_value_average(node) for node in other_residues])

    return total_residue_index is None or len(other_residues) == 0 or (total_residue * 1.01) >= other_sum or {
        'level': 'error',
        'dataPath': f".products[{total_residue_index}].value",
        'message': f"must be more than or equal to ({' + '.join(other_residues_ids)})"
    }


def _crop_residue_fate(cycle: dict):
    practices = filter_list_term_type(cycle.get('practices', []), TermTermType.CROPRESIDUEMANAGEMENT)

    products = filter_list_term_type(cycle.get('products', []), TermTermType.CROPRESIDUE)
    terms = get_crop_residue_terms()
    above_terms = list(filter(lambda term: term.startswith('above'), terms))
    sum_above_ground = _list_sum_terms(products, above_terms)
    below_terms = list(filter(lambda term: term.startswith('below'), terms))
    sum_below_ground = _list_sum_terms(products, below_terms)
    return (practices, sum_above_ground, sum_below_ground)


def validate_crop_residue_complete(cycle: dict, site: dict):
    def validate():
        practices, sum_above_ground, sum_below_ground = _crop_residue_fate(cycle)
        return all([len(practices) > 0, sum_above_ground > 0, sum_below_ground > 0]) or {
            'level': 'error',
            'dataPath': '',
            'message': 'must specify the fate of cropResidue'
        }

    data_complete = cycle.get('completeness', {}).get(TermTermType.CROPRESIDUE.value, False)
    site_type = site.get('siteType')
    return not data_complete or site_type not in SITE_TYPES_RESTRICTED or validate()


def validate_crop_residue_incomplete(cycle: dict, site: dict):
    def validate():
        practices, sum_above_ground, sum_below_ground = _crop_residue_fate(cycle)
        return any([len(practices) > 0, sum_above_ground > 0, sum_below_ground > 0]) or {
            'level': 'warning',
            'dataPath': '',
            'message': 'should specify the fate of cropResidue'
        }

    data_complete = cycle.get('completeness', {}).get(TermTermType.CROPRESIDUE.value, False)
    site_type = site.get('siteType')
    return data_complete or site_type not in SITE_TYPES_RESTRICTED or validate()


def validate_siteDuration(cycle: dict):
    cycleDuration = cycle.get('cycleDuration')
    siteDuration = cycle.get('siteDuration')
    has_multiple_sites = len(cycle.get('otherSites', [])) > 0
    return cycleDuration is None or siteDuration is None or (cycleDuration != siteDuration or {
        'level': 'error',
        'dataPath': '.siteDuration',
        'message': 'must not be equal to cycleDuration'
    } if has_multiple_sites else cycleDuration == siteDuration or {
        'level': 'error',
        'dataPath': '.siteDuration',
        'message': 'must be equal to cycleDuration'
    })


def validate_otherSites_cycleDuration(cycle: dict):
    cycleDuration = cycle.get('cycleDuration', 0)
    siteDuration = cycle.get('siteDuration')
    total_duration = list_sum([siteDuration or 0] + cycle.get('otherSitesDuration', [0]))
    return siteDuration is None or cycleDuration == total_duration or {
        'level': 'error',
        'dataPath': '.cycleDuration',
        'message': 'must be equal to the sum of siteDuration and otherSitesDuration'
    }


def _product_cover_crop(product: dict):
    term_id = product.get('term', {}).get('@id')
    term_type = product.get('term', {}).get('termType')
    lookup = download_lookup(f"{term_type}.csv")
    is_cover_crop = get_table_value(lookup, 'termid', term_id, column_name('possibleCoverCrop'))
    return not (not is_cover_crop)  # convert numpy boolean to boolean


def validate_possibleCoverCrop(cycle: dict):
    cover_crop = find_term_match(cycle.get('practices', []), 'coverCrop', None)
    cover_crop_value = cover_crop.get('value', []) if cover_crop else None
    has_cover_crop = cover_crop_value is not None and (
        len(cover_crop_value) == 0 or (cover_crop_value[0] != 0 and cover_crop_value[0] != 'false')
    )
    invalid_product = next((p for p in cycle.get('products', []) if not _product_cover_crop(p)), None)

    return not has_cover_crop or invalid_product is None or {
        'level': 'error',
        'dataPath': '',
        'message': 'cover crop cycle contains non cover crop product'
    }


def validate_set_treatment(cycle: dict, source: dict):
    key = 'treatment'
    has_experimentDesign = 'experimentDesign' in source
    has_treatment = key in cycle
    return not has_experimentDesign or has_treatment or {
        'level': 'warning',
        'dataPath': f".{key}",
        'message': f"should specify a {key} when experimentDesign is specified"
    }


def validate_products_animals(cycle: dict):
    products = cycle.get('products', [])
    has_liveAnimal = len(filter_list_term_type(products, TermTermType.LIVEANIMAL)) > 0
    has_animalProduct = len(filter_list_term_type(products, TermTermType.ANIMALPRODUCT)) > 0
    return not all([has_liveAnimal, has_animalProduct]) or {
        'level': 'warning',
        'dataPath': '.products',
        'message': 'should not specify both liveAnimal and animalProduct'
    }


def validate_cycle(cycle: dict, node_map: dict = {}):
    """
    Validates a single `Cycle`.

    Parameters
    ----------
    cycle : dict
        The `Cycle` to validate.
    node_map : dict
        The list of all nodes to do cross-validation, grouped by `type` and `id`.

    Returns
    -------
    List
        The list of errors for the `Cycle`, which can be empty if no errors detected.
    """
    site = _find_linked_node(node_map, cycle.get('site', {}))
    source = _find_linked_node(node_map, cycle.get('defaultSource', {}))
    return flatten([
        validate_cycle_dates(cycle),
        validate_date_lt_today(cycle, 'startDate'),
        validate_date_lt_today(cycle, 'endDate'),
        validate_linked_source_privacy(cycle, 'defaultSource', node_map),
        validate_private_has_source(cycle, 'defaultSource'),
        validate_cycleDuration(cycle) if _should_validate_cycleDuration(cycle) else True,
        validate_completeness(cycle, site) if 'completeness' in cycle else True,
        validate_siteDuration(cycle),
        validate_otherSites_cycleDuration(cycle),
        validate_possibleCoverCrop(cycle),
        validate_products_animals(cycle),
        validate_set_treatment(cycle, source) if source else True
    ]) + flatten(
        ([
            validate_list_model(cycle, 'emissions'),
            validate_list_dates(cycle, 'emissions'),
            validate_list_dates_after(cycle, 'startDate', 'emissions', ['startDate', 'endDate']),
            validate_list_dates_format(cycle, 'emissions'),
            validate_list_min_below_max(cycle, 'emissions'),
            validate_list_value_between_min_max(cycle, 'emissions'),
            validate_list_term_percent(cycle, 'emissions'),
            validate_list_dates_length(cycle, 'emissions'),
            validate_list_date_lt_today(cycle, 'emissions', ['startDate', 'endDate']),
            validate_properties_default_value(cycle, 'emissions'),
            validate_properties_valueType(cycle, 'emissions'),
            validate_linked_terms(cycle, 'emissions', 'inputs', 'inputs', True),
            validate_linked_terms(cycle, 'emissions', 'transformation', 'transformations', True),
            validate_method_not_relevant(cycle, 'emissions'),
            validate_methodTier_not_relevant(cycle, 'emissions')
        ] if len(cycle.get('emissions', [])) > 0 else []) +
        ([
            validate_list_dates(cycle, 'inputs'),
            validate_list_dates_after(cycle, 'startDate', 'inputs', ['startDate', 'endDate', 'dates']),
            validate_list_dates_format(cycle, 'inputs'),
            validate_list_dates_length(cycle, 'inputs'),
            validate_list_date_lt_today(cycle, 'inputs', ['startDate', 'endDate']),
            validate_list_min_below_max(cycle, 'inputs'),
            validate_list_value_between_min_max(cycle, 'inputs'),
            validate_list_term_percent(cycle, 'inputs'),
            validate_properties_default_value(cycle, 'inputs'),
            validate_properties_valueType(cycle, 'inputs'),
            validate_volatileSolidsContent(cycle, 'inputs'),
            validate_must_include_id(cycle['inputs']),
            validate_input_country(cycle, 'inputs'),
            validate_related_impacts(cycle, 'inputs', node_map),
            validate_input_distribution_value(cycle, site, 'inputs') if site else True,
            validate_animalFeed_requires_isAnimalFeed(cycle, site, 'inputs') if site else True
        ] if len(cycle.get('inputs', [])) > 0 else []) +
        ([
            validate_list_dates(cycle, 'products'),
            validate_list_dates_after(cycle, 'startDate', 'products', ['startDate', 'endDate', 'dates']),
            validate_list_dates_format(cycle, 'products'),
            validate_list_dates_length(cycle, 'products'),
            validate_list_date_lt_today(cycle, 'products', ['startDate', 'endDate']),
            validate_list_min_below_max(cycle, 'products'),
            validate_list_value_between_min_max(cycle, 'products'),
            validate_list_term_percent(cycle, 'products'),
            validate_economicValueShare(cycle.get('products')),
            validate_sum_aboveGroundCropResidue(cycle.get('products')),
            validate_value_empty(cycle.get('products')),
            validate_value_0(cycle.get('products')),
            validate_product_primary(cycle.get('products')),
            validate_properties_default_value(cycle, 'products'),
            validate_properties_valueType(cycle, 'products'),
            validate_volatileSolidsContent(cycle, 'products'),
            validate_crop_residue_complete(cycle, site) if site else True,
            validate_crop_residue_incomplete(cycle, site) if site else True,
            validate_list_model_config(cycle, 'products', PRODUCTS_MODEL_CONFIG),
            validate_excreta(cycle, 'products'),
            validate_product_ha_functional_unit_ha(cycle, 'products'),
            validate_product_yield(cycle, site, 'products') if site else True
        ] if len(cycle.get('products', [])) > 0 else []) +
        ([
            validate_list_dates(cycle, 'practices'),
            validate_list_dates_after(cycle, 'startDate', 'practices', ['startDate', 'endDate', 'dates']),
            validate_list_dates_format(cycle, 'practices'),
            validate_list_date_lt_today(cycle, 'practices', ['startDate', 'endDate']),
            validate_list_min_below_max(cycle, 'practices'),
            validate_list_value_between_min_max(cycle, 'practices'),
            validate_list_term_percent(cycle, 'practices'),
            validate_cropResidueManagement(cycle.get('practices')),
            validate_longFallowPeriod(cycle.get('practices')),
            validate_properties_default_value(cycle, 'practices'),
            validate_properties_valueType(cycle, 'practices'),
            validate_list_duplicate_values(cycle, 'practices', 'term.termType', TermTermType.EXCRETAMANAGEMENT.value),
            validate_excretaManagement(cycle, cycle.get('practices')),
            validate_no_tillage(cycle.get('practices')),
            validate_tillage_site_type(cycle.get('practices'), site) if site else True,
            validate_tillage_values(cycle.get('practices')),
            validate_liveAnimal_system(cycle),
            validate_pastureGrass_key_units(cycle, 'practices'),
            validate_pastureGrass_key_value(cycle, 'practices'),
            validate_has_pastureGrass(cycle, site, 'practices') if site else True
        ] if len(cycle.get('practices', [])) > 0 else []) +
        ([
            validate_list_dates(cycle, 'transformations'),
            validate_list_dates_after(cycle, 'startDate', 'transformations', ['startDate', 'endDate']),
            validate_list_dates_format(cycle, 'transformations'),
            validate_list_date_lt_today(cycle, 'transformations', ['startDate', 'endDate']),
            validate_previous_transformation(cycle, 'transformations'),
            validate_transformation_excretaManagement(cycle, 'transformations'),
            validate_linked_emission(cycle, 'transformations')
        ] if len(cycle.get('transformations', [])) > 0 else [])
    )
