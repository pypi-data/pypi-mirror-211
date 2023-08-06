from typing import Any, Union, Optional, Tuple, TYPE_CHECKING

from pydantic import BaseModel

from .types import ObjectIdStr
from .exceptions import MotordanticValidationError


__all__ = ('validate_field_value', 'sort_validation')

if TYPE_CHECKING:
    from .models import MongoModel
    from .typing import MongoModelType


def validate_field_value(
    model: Union['MongoModel', 'MongoModelType'], field_name: str, value: Any
) -> Any:
    """extra helper value validation

    Args:
        cls ('MongoModel'): mongo model class
        field_name (str): name of field
        value (Any): value

    Raises:
        AttributeError: if not field in __fields__
        MongoValidationError: if invalid value type

    Returns:
        Any: value
    """
    if field_name == '_id':
        field = ObjectIdStr()  # type: ignore
    else:
        field = model.__fields__.get(field_name)  # type: ignore
    error_ = None
    if isinstance(field, ObjectIdStr):
        try:
            value = field.validate(value)
        except ValueError as e:
            error_ = e
    elif not field:
        raise AttributeError(f'invalid field - {field_name}')
    else:
        value, error_ = field.validate(value, {}, loc=field.alias, cls=model)  # type: ignore
    if error_:
        raise MotordanticValidationError([error_], type(value))
    if field_name in model.__db_refs__:  # type: ignore
        if isinstance(value, list):
            s = [v.to_ref() for v in value]
            return s
        return value.to_ref() if value else None
    else:
        return value.dict() if isinstance(value, BaseModel) else value


def sort_validation(
    sort: Optional[int] = None, sort_fields: Union[list, tuple, None] = None
) -> Tuple[Any, ...]:
    if sort is not None:
        if sort not in (1, -1):
            raise ValueError(f'invalid sort value must be 1 or -1 not {sort}')
        if not sort_fields:
            sort_fields = ('_id',)
    return sort, sort_fields
