def _convert_dataclass_to_json_dict(x):
    if hasattr(x, '__dict__'):
        return {
            key: _convert_dataclass_to_json_dict(x.__dict__[key])
            for key in x.__dict__
        }
    if type(x) == list:
        return [
            _convert_dataclass_to_json_dict(element)
            for element in x
        ]
    return x


