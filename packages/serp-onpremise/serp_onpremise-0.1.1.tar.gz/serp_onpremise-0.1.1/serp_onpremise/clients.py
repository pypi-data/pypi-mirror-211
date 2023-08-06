from importlib import import_module
from typing import Any, Dict, Optional

from serp_onpremise import constants
from serp_onpremise.auth_token import AuthorizationTokenAuth
from serp_onpremise.utils import cached_property, get_package_version


class Catcher:
    def __init__(
        self, prev: str, is_async: bool, settings: dict, api_version: int
    ) -> None:
        self.prev = prev
        self.settings = settings
        self.is_async = is_async
        self.api_version = api_version

    def __getattr__(self, item: str) -> Any:
        return Catcher(
            prev=f"{self.prev}.{item}",
            is_async=self.is_async,
            settings=self.settings,
            api_version=self.api_version,
        )

    def __call__(self, *args: list, **kwargs: dict) -> Any:
        method = self.prev.split(".")[-1]
        path = ".".join(self.prev.split(".")[:-1])
        module_path = f"serp_onpremise.{path}.v{self.api_version}"
        module = import_module(module_path)
        if module:
            cls = getattr(module, ("ImplAsync" if self.is_async else "Impl"))
            inst = cls(settings=self.settings)
            if inst:
                return getattr(inst, method)(*args, **kwargs)


class Client:
    def __init__(
        self,
        base_url: str,
        api_token: Optional[str] = None,
        timeout: float = constants.HTTP_CLIENT_TIMEOUT,
    ):
        """
        Creates and manages singleton of HTTP client, that is used to make
        request to API.
        """
        self.api_version = 1
        self.client_settings = self.create_client_settings(
            base_url=base_url, timeout=timeout, token=api_token
        )
        self.api_atrr_names = [
            "licenses",
            "statistics",
            "whoami",
            "auth",
            "users",
            "spaces",
            "tokens",
            "groups_profiles",
            "entries",
            "origins",
            "profiles",
            "compare",
            "asm",
            "liveness",
        ]

    @cached_property
    def is_async(self) -> bool:
        return self.__class__.__name__ == "AsyncClient"

    @property
    def common_headers(self) -> dict:
        root = "serp-onpremise-python"
        if self.is_async:
            root = "serp-onpremise-python-async"
        return {"User-Agent": f"{root}/{get_package_version()}"}

    def create_client_settings(
        self, base_url: str, timeout: float, token: str = None
    ) -> Dict[Any, Any]:
        settings = {
            "base_url": base_url,
            "timeout": timeout,
            "headers": self.common_headers,
        }
        if token:
            settings["auth"] = AuthorizationTokenAuth(api_token=token)

        return settings

    def __getattr__(self, item: str) -> Any:
        if item in self.api_atrr_names:
            return Catcher(
                prev=item,
                is_async=self.is_async,
                settings=self.client_settings,
                api_version=self.api_version,
            )
        else:
            # Default behaviour
            raise AttributeError


class AsyncClient(Client):
    pass
