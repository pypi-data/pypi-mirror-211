from collections.abc import Mapping
from pathlib import Path
from typing import Optional, Union

from .base_session import BaseSessionBound
from .empty_mapping import EMPTY_MAPPING


class Plugin:
    @property
    def app_extensions(self) -> Mapping[str, Union[str, Path]]:
        """The app extensions contributed by the plugin to be added to the session configuration."""
        return EMPTY_MAPPING

    def init_session(self, session: BaseSessionBound, /) -> None:
        """Handle newly initialized session."""

    @property
    def jar_path(self) -> Optional[Path]:
        """The path to the plugin's JAR.

        When not ``None``, the JAR will be added to the classpath of the Java process.
        """
        return None
