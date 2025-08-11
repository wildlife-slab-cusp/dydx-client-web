# modules/type_caster.py - updated 2025-08-11

from typing import Union, List
from .type_caster_models import _MODEL_REGISTRY

def cast_type(
    data: Union[dict, List[dict]],
    model_name: str
) -> Union[dict, List[dict]]:
    """
    Type-cast and validate raw dict(s) into type-cast dicts.

    Parameters:
        data (dict | list[dict]):
            Raw input data to be type-cast and validated.
        model_name (str):
            The key name in _MODEL_REGISTRY for the desired model.

    Returns:
        A type-cast dict, or a list of dicts, depending on input type.
    """
    model_class = _MODEL_REGISTRY.get(model_name)
    if not model_class:
        raise ValueError(f"Unknown model name: {model_name}")

    def cast_item(item: dict):
        model_instance = model_class(**item)
        return model_instance.model_dump(mode="json")

    if isinstance(data, list):
        return [cast_item(item) for item in data]
    return cast_item(data)
