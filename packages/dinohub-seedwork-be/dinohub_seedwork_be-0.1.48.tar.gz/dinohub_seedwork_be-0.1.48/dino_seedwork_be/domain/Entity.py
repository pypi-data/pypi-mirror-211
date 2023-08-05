import datetime
from abc import abstractmethod
from typing import Generic, TypedDict, TypeVar

from returns.maybe import Maybe, Nothing, Some
from returns.result import Result, Success, safe
from typing_extensions import Self

from dino_seedwork_be.utils.functional import unwrap

from .IdentifiedDomainObject import IdentifiedDomainObject, IdentityType


class BaseRawAttributes(TypedDict):
    created_at: Maybe[datetime.datetime]
    updated_at: Maybe[datetime.datetime]


RawAttributes = TypeVar("RawAttributes", bound=BaseRawAttributes)


# __all__ = ["Entity", "BaseRawAttributes"]


class Entity(
    Generic[RawAttributes, IdentityType], IdentifiedDomainObject[IdentityType]
):
    _created_at: Maybe[datetime.datetime] = Nothing
    _updated_at: Maybe[datetime.datetime] = Nothing

    _concurrency_version: int = 0

    def __init__(self, id: Maybe[IdentityType] = Nothing):
        self._concurrency_version = 0
        super().__init__(id)

    def updated_at(self) -> Maybe:
        return self._updated_at

    def created_at(self) -> Maybe:
        return self._created_at

    def set_update_at(self, a_date_time: datetime.datetime) -> Result:
        self._updated_at = Some(a_date_time)
        return Success("OK")

    def set_created_at(self, a_date_time: datetime.datetime) -> Result:
        self._created_at = Some(a_date_time)
        return Success("OK")

    def concurrency_version(self) -> int:
        return self._concurrency_version

    def increase_concurrency_version(self):
        self._concurrency_version += 1

    @classmethod
    @safe
    def create(cls, raw_attributes: RawAttributes, id: Maybe[IdentityType]) -> Self:
        entity = cls(id)
        entity._created_at = raw_attributes["created_at"]
        entity._updated_at = raw_attributes["updated_at"]
        unwrap(entity.init_by_atributes(raw_attributes))
        return entity

    @abstractmethod
    def init_by_atributes(self, raw_attributes: RawAttributes) -> Result:
        pass
