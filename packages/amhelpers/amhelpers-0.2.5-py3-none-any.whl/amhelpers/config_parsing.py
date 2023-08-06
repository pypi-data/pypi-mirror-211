import copy
from .amhelpers import get_class_from_str
from .amhelpers import create_object_from_dict

NET_PARAMS = [
    'module',
    'criterion',
    'optimizer',
    'lr',
    'max_epochs',
    'batch_size',
    'iterator_train',
    'iterator_valid',
    'dataset',
    'train_split',
    'callbacks',
    'predict_nonlinearity',
    'warm_start',
    'verbose',
    'device'
]

def _check_value(value):
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, bool):
        return value
    elif isinstance(value, str):
        return value
    elif isinstance(value, list):
        return [_check_value(v) for v in value]
    elif isinstance(value, dict):
        if 'type' in value:
            is_called = value.pop('is_called')
            if is_called:
                has_nested_dict = any(
                    [isinstance(v, dict) and 'type' in v for v in value.values()]
                )
                if has_nested_dict:
                    return create_object_from_dict(
                        {k: _check_value(v) for k, v in value.items()}
                    )
                else:
                    return create_object_from_dict(value)
            else:
                type_str = value['type']
                return get_class_from_str(type_str)
        else:
            return {k: _check_value(v) for k, v in value.items()}
    elif value is None:
        return value
    else:
        raise ValueError('The value of type {} is unknown.'.format(type(value)))

def _get_object_and_parameters(name, default_params, specified_params):
    default_params.pop('is_called', None)
    specified_params.pop('is_called', None)

    prefix = name + '__'

    if 'type' in specified_params:
        # Take everything from specified_params
        out = {name: get_class_from_str(specified_params.pop('type'))}
        out.update(
            {prefix+k: _check_value(v) for k, v in specified_params.items()}
        )
    elif 'type' in default_params:
        # Replace default values if they exist in specified_params
        out = {name: get_class_from_str(default_params.pop('type'))}
        new = {}
        for k in default_params.keys():
            if k in specified_params:
                v = specified_params.pop(k)
                new[prefix+k] = _check_value(v)
            else:
                new[prefix+k] = _check_value(default_params[k])
        out.update(new)
        # Add values that exist in specified_params but not in default_params
        out.update({prefix+k: _check_value(v) for k, v in specified_params.items()})
    else:
        out = {}
        for k in set(list(default_params.keys()) + list(specified_params.keys())):
            out[prefix+k] = _check_value(specified_params[k]) if k in specified_params else _check_value(default_params[k])

    return out

def get_net_params(default, specified):
    '''Get parameters for a skorch neural net.

    Parameters
    ----------
    default : dict
        Default parameter values on the format "parameter name: value".
    specified : dict
        Specified parameter values on the format "parameter name: value". Will replace the default values.

    Returns
    -------
    params : dict
        All model parameters.
    '''
    default = copy.deepcopy(default)
    specified = copy.deepcopy(specified)
    
    params = {}
    for param in NET_PARAMS:
        try:
            default_value = default[param]
        except KeyError:
            default_value = {}
        try:
            specified_value = specified[param]
        except KeyError:
            specified_value = {}

        if param in [
            'module',
            'criterion',
            'optimizer',
            'iterator_train',
            'iterator_valid',
            'dataset'
        ]:
            params.update(
                _get_object_and_parameters(param, default_value, specified_value)
            )
        else:
            if param in specified:
                params[param] = _check_value(specified[param])
            elif param in default:
                params[param] = _check_value(default_value)
            else:
                # Use skorch default
                pass

    return params
