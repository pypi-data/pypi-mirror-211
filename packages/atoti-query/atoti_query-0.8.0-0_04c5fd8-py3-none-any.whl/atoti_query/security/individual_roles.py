from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
    overload,
)

from atoti_core import DelegateMutableMapping, ReactiveMutableSet, deprecated
from typeguard import typechecked

from ._service import Service

if TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem  # pylint: disable=nested-import


class _UserRoles(ReactiveMutableSet[str]):
    def __init__(
        self,
        data: Iterable[str],
        /,
        *,
        username: str,
        user_role_mapping: IndividualRoles,
    ) -> None:
        super().__init__(data)

        self._username = username
        self._user_role_mapping = user_role_mapping

    def _on_change(self, *, in_place: bool) -> None:
        if in_place:
            deprecated("Mutating roles is deprecated. Reassign them instead.")

        self._user_role_mapping[self._username] = self


_UserRolesDescription = Union[Iterable[str], _UserRoles]


class IndividualRoles(DelegateMutableMapping[str, _UserRoles]):
    """Mapping from username to roles granted on top of the ones that can be added by authentication providers.

    Example:
        >>> session = tt.Session(authentication=tt.BasicAuthenticationConfig())
        >>> username = "John"
        >>> session.security.basic.credentials[username] = "X Æ A-12"
        >>> username in session.security.individual_roles
        False
        >>> session.security.individual_roles[username] = {
        ...     "ROLE_USA",
        ...     "ROLE_USER",
        ... }
        >>> sorted(session.security.individual_roles[username])
        ['ROLE_USA', 'ROLE_USER']
        >>> session.security.individual_roles[username] -= {"ROLE_USA"}
        >>> session.security.individual_roles[username]
        {'ROLE_USER'}
        >>> # Removing all the roles will prevent the user from accessing the application:
        >>> del session.security.individual_roles[username]
        >>> username in session.security.individual_roles
        False
    """

    def __init__(self, *, service: Service) -> None:
        super().__init__()

        self._service = service

    def _get_underlying(self) -> dict[str, _UserRoles]:
        return {
            username: _UserRoles(  # Replace with `username: frozenset(roles)` in the next breaking release.
                roles, username=username, user_role_mapping=self
            )
            for username, roles in self._service.individual_roles.items()
        }

    def _delete_keys(self, keys: Optional[Iterable[str]] = None, /) -> None:
        keys = self._default_to_all_keys(keys)
        for username in keys:
            self._service.delete_individual_roles_for_user(username)

    # Custom override with same value type as the one used in `update()`.
    @typechecked
    def __setitem__(self, key: str, value: _UserRolesDescription, /) -> None:
        self.update({key: value})

    def _update(self, other: Mapping[str, _UserRolesDescription], /) -> None:
        for username, roles in other.items():
            self._service.upsert_individual_roles(username, roles=roles)

    @overload
    def update(
        self,
        __m: SupportsKeysAndGetItem[str, _UserRolesDescription],
        **kwargs: _UserRolesDescription,
    ) -> None:
        ...

    @overload
    def update(
        self,
        __m: Iterable[tuple[str, _UserRolesDescription]],
        **kwargs: _UserRolesDescription,
    ) -> None:
        ...

    @overload
    def update(self, **kwargs: _UserRolesDescription) -> None:
        ...

    # Custom override types on purpose so that `Iterable[str]` can be inserted.
    def update(  # type:ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
        self,
        __m: Optional[
            Union[
                Mapping[str, _UserRolesDescription],
                Iterable[tuple[str, _UserRolesDescription]],
            ]
        ] = None,
        **kwargs: _UserRolesDescription,
    ) -> None:
        other: dict[str, _UserRolesDescription] = {}
        if __m is not None:
            other.update(__m)
        other.update(**kwargs)
        self._update(other)
