from typing import Final

class PackageInstaller:
    PYTHON_PREFIX: Final[str]
    @classmethod
    def install(cls, pkg_name: str, upgrade: bool = ..., user: bool = ...) -> None: ...
    @classmethod
    def uninstall(cls, pkg_name: str) -> None: ...
    @classmethod
    def upgrade_all(cls) -> None: ...
