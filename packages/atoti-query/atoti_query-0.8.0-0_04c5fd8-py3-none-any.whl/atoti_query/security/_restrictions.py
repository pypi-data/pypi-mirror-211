from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Optional

from atoti_core import DelegateMutableMapping

from ._constants import SPECIAL_ROLES
from ._restriction import Restriction
from ._service import Service


class Restrictions(DelegateMutableMapping[str, Restriction]):
    def __init__(
        self,
        *,
        service: Service,
    ) -> None:
        self._service = service

    def _get_underlying(self) -> dict[str, Restriction]:
        return self._service.restrictions

    def _update(self, other: Mapping[str, Restriction], /) -> None:
        for role_name, restriction in other.items():
            if role_name in SPECIAL_ROLES:
                raise ValueError(
                    f"Role `{role_name}` is reserved and cannot be assigned restrictions, use another role."
                )

            self._service.upsert_restriction(restriction, role_name=role_name)

    def _delete_keys(self, keys: Optional[Iterable[str]] = None, /) -> None:
        keys = self._default_to_all_keys(keys)
        for role_name in keys:
            self._service.delete_restriction(role_name)
