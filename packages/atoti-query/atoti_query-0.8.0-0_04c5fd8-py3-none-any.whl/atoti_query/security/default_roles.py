from collections.abc import Set

from atoti_core import DelegateMutableSet

from ._authentication_type import AuthenticationType
from ._service import Service


class DefaultRoles(DelegateMutableSet[str]):
    """Roles granted to users who have been granted no :attr:`individual <atoti_query.security.Security.individual_roles>` and :class:`mapped <atoti_query.security.role_mapping.RoleMapping>` roles."""

    def __init__(
        self, *, authentication_type: AuthenticationType, service: Service
    ) -> None:
        super().__init__()

        self._authentication_type: AuthenticationType = authentication_type
        self._service = service

    def _get_underlying(self) -> set[str]:
        return set(
            self._service.get_default_roles(
                authentication_type=self._authentication_type,
            )
        )

    def _set_underlying(self, new_set: Set[str], /) -> None:
        self._service.set_default_roles(
            new_set,
            authentication_type=self._authentication_type,
        )
