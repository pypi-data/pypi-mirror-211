from functools import reduce
from hestia_earth.schema import TermTermType
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import list_sum, non_empty_list, safe_parse_float, flatten

from hestia_earth.validation.utils import _filter_list_errors, _value_average, _node_year
from hestia_earth.validation.models import is_enabled as models_is_enabled, value_from_model
from .shared import need_validate_coordinates, value_difference


SOIL_TEXTURE_IDS = ['sandContent', 'siltContent', 'clayContent']


def _precipitationAnnual(site: dict, measurement: dict):
    from hestia_earth.models.geospatialDatabase.precipitationAnnual import _run
    year = _node_year(measurement)
    result = _run(site, year) if year and need_validate_coordinates(site) else None
    return result


MEASUREMENTS_MODELS = {
    'precipitationAnnual': [
        'geospatialDatabase',
        _precipitationAnnual
    ]
}


def _group_measurement_key(measurement: dict):
    keys = non_empty_list([
        str(measurement.get('depthUpper', '')),
        str(measurement.get('depthLower', '')),
        measurement.get('startDate'),
        measurement.get('endDate')
    ])
    return '-'.join(keys) if len(keys) > 0 else 'default'


def _group_measurements_depth(measurements: list):
    def group_by(group: dict, values: tuple):
        index, measurement = values
        key = _group_measurement_key(measurement)
        if key not in group:
            group[key] = []
        group[key].extend([{'index': index, 'measurement': measurement}])
        return group

    return reduce(group_by, measurements, {})


def _validate_soilTexture_percent(lookup):
    soil_texture_ids = list(lookup.termid)

    def validate_single(measurements: list, texture: dict, measurement_id: str):
        term_id = texture['measurement'].get('term', {}).get('@id')
        min = safe_parse_float(get_table_value(lookup, 'termid', term_id, column_name(f"{measurement_id}min")), 0)
        max = safe_parse_float(get_table_value(lookup, 'termid', term_id, column_name(f"{measurement_id}max")), 100)
        # set default value to min so if no value then passes validation
        measurement = next(
            (v for v in measurements if v['measurement'].get('term', {}).get('@id') == measurement_id), {})
        texture_value = _value_average(measurement.get('measurement'), min)
        return min <= texture_value <= max or {
            'level': 'error',
            'dataPath': f".measurements[{measurement['index']}].value",
            'message': 'is outside the allowed range',
            'params': {
                'term': measurement['measurement'].get('term', {}),
                'range': {'min': min, 'max': max}
            }
        }

    def validate(values: list):
        texture_ids = list(filter(lambda v: v['measurement'].get('term', {}).get('@id') in soil_texture_ids, values))
        return len(texture_ids) == 0 or flatten(map(
            lambda texture: list(map(lambda id: validate_single(values, texture, id), SOIL_TEXTURE_IDS)),
            texture_ids
        ))

    return validate


def _validate_soiltTexture_sum(values: list):
    measurements = list(filter(lambda v: v['measurement'].get('term', {}).get('@id') in SOIL_TEXTURE_IDS, values))
    measurements = list(filter(lambda v: 'value' in v['measurement'], measurements))
    terms = list(map(lambda v: v['measurement'].get('term', {}).get('@id'), measurements))
    sum_values = sum(map(lambda v: _value_average(v['measurement']), measurements))
    return len(set(terms)) != len(SOIL_TEXTURE_IDS) or 99.5 < sum_values < 100.5 or [{
        'level': 'error',
        'dataPath': f".measurements[{m['index']}]",
        'message': f"sum not equal to 100% for {', '.join(SOIL_TEXTURE_IDS)}"
    } for m in measurements]


def validate_soilTexture(measurements: list):
    soilTexture = download_lookup('soilTexture.csv')
    groupped_values = _group_measurements_depth(enumerate(measurements)).values()
    return _filter_list_errors(
        list(map(_validate_soiltTexture_sum, groupped_values)) +
        flatten(map(_validate_soilTexture_percent(soilTexture), groupped_values))
    )


def validate_depths(measurements: list):
    def validate(values: tuple):
        index, measurement = values
        return measurement.get('depthUpper', 0) <= measurement.get('depthLower', 1) or {
            'level': 'error',
            'dataPath': f".measurements[{index}].depthLower",
            'message': 'must be greater than or equal to depthUpper'
        }

    return _filter_list_errors(map(validate, enumerate(measurements)))


def validate_required_depths(site: dict, list_key: str):
    values = site.get(list_key, [])
    required_has_depths = any(filter(
        lambda v: v.get('term', {}).get('@id') in SOIL_TEXTURE_IDS and (
            v.get('depthUpper') or v.get('depthLower')
        ),
        values
    ))

    def validate(values: tuple):
        index, measurement = values
        term = measurement.get('term', {})
        term_id = term.get('@id')
        term_type = term.get('termType')
        lookup = download_lookup(f"{term_type}.csv")
        with_depth = get_table_value(lookup, 'termid', term_id, column_name('recommendAddingDepth'))
        has_depths = measurement.get('depthUpper') is not None and measurement.get('depthLower') is not None
        level = 'error' if all([required_has_depths, term_type == TermTermType.SOILTEXTURE.value]) else 'warning'
        return not with_depth or with_depth == '' or has_depths or {
            'level': level,
            'dataPath': f".{list_key}[{index}]",
            'message': f"{'must' if level == 'error' else 'should'} set both depthUpper and depthLower"
        }

    return _filter_list_errors(map(validate, enumerate(values)))


def validate_term_unique(measurements: list):
    lookup = download_lookup('measurement.csv')

    def count_same_term(term_id: str):
        return len(list(filter(lambda x: x.get('term', {}).get('@id') == term_id, measurements)))

    def validate(values: tuple):
        index, measurement = values
        term_id = measurement.get('term', {}).get('@id')
        unique = get_table_value(lookup, 'termid', term_id, 'onemeasurementpersite')
        unique = False if unique is None or unique == '-' else bool(unique)
        return not unique or count_same_term(term_id) == 1 or {
            'level': 'error',
            'dataPath': f".measurements[{index}].term.name",
            'message': 'must be unique'
        }

    return _filter_list_errors(map(validate, enumerate(measurements)))


def validate_require_startDate_endDate(site: dict, list_key: str):
    lookup = download_lookup('measurement.csv')
    site_start_date = site.get('startDate')
    site_end_date = site.get('endDate')

    def validate(values: tuple):
        index, measurement = values
        term_id = measurement.get('term', {}).get('@id')
        start_date = measurement.get('startDate')
        end_date = measurement.get('endDate')
        required = get_table_value(lookup, 'termid', term_id, column_name('needStartDateEndDate'))
        return any([
            not required,
            start_date is not None and end_date is not None,
            site_start_date is not None and start_date == site_start_date,
            site_end_date is not None and end_date == site_end_date
        ]) or list(map(lambda k: {
            'level': 'error',
            'dataPath': f".{list_key}[{index}]",
            'message': f"should have required property '{k}'",
            'params': {
                'missingProperty': k
            }
        }, ['startDate', 'endDate']))

    return _filter_list_errors(flatten(map(validate, enumerate(site.get(list_key, [])))))


def validate_with_models(site: dict, list_key: str):
    threshold = 0.25

    def validate(values: tuple):
        index, blank_node = values
        term_id = blank_node.get('term', {}).get('@id')
        value = blank_node.get('value', [0])
        value = list_sum(value, value)
        model, model_run = MEASUREMENTS_MODELS.get(term_id, [None, None])
        expected_node = model_run(site, blank_node) if model else {}
        expected_value = value_from_model(expected_node) if expected_node else value
        delta = value_difference(value, expected_value) if expected_value else 0
        data_path = '' if blank_node.get('value') is None else '.value'
        return delta < threshold or {
            'level': 'warning',
            'dataPath': f".{list_key}[{index}]{data_path}",
            'message': 'the measurement provided might be in error',
            'params': {
                'term': blank_node.get('term', {}),
                'model': expected_node.get('methodModel', {}),
                'current': value,
                'expected': expected_value,
                'delta': delta * 100,
                'threshold': threshold
            }
        }

    nodes = site.get(list_key, []) if models_is_enabled() else []
    return _filter_list_errors(flatten(map(validate, enumerate(nodes))))


def validate_value_length(site: dict, list_key: str):
    def validate(values: tuple):
        index, blank_node = values
        term_id = blank_node.get('term', {}).get('@id')
        lookup = download_lookup('measurement.csv')
        array_type = get_table_value(lookup, 'termid', term_id, column_name('arrayTreatment'))
        value_length = len(blank_node.get('value', []))
        return array_type != 'arrayNotAllowed' or value_length <= 1 or {
            'level': 'error',
            'dataPath': f".measurements[{index}].value",
            'message': 'must not contain more than 1 value'
        }

    return _filter_list_errors(flatten(map(validate, enumerate(site.get(list_key, [])))))
