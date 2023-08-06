from __future__ import annotations

import random
import string
from abc import abstractmethod
from collections.abc import Mapping
from datetime import timedelta
from time import time
from typing import Any, Generic, Literal, Optional, TypeVar, cast

import pandas as pd

from .activeviam_client import ActiveViamClient
from .base_cubes import BaseCubesBound
from .context import Context
from .default_query_timeout import DEFAULT_QUERY_TIMEOUT
from .doc import doc
from .empty_mapping import EMPTY_MAPPING
from .find_corresponding_top_level_variable_name import (
    find_corresponding_top_level_variable_name,
)
from .missing_plugin_error import MissingPluginError
from .query_doc import QUERY_ARGS_DOC
from .repr_json import ReprJson, ReprJsonable

CubesT = TypeVar("CubesT", bound=BaseCubesBound, covariant=True)
_SecurityT = TypeVar("_SecurityT", covariant=True)


def _generate_session_id() -> str:
    random_string = "".join(
        # No cryptographic security required.
        random.choices(string.ascii_uppercase + string.digits, k=6)  # noqa: S311
    )
    return f"{int(time())}_{random_string}"


class BaseSession(Generic[CubesT, _SecurityT], ReprJsonable):
    """Base class for session."""

    def __init__(self) -> None:
        self.__id = _generate_session_id()

        def link(
            session: BaseSessionBound,  # noqa: ARG001
            /,
            *,
            path: str,  # noqa: ARG001
        ) -> object:
            raise MissingPluginError("jupyterlab3")

        def visualize(
            session: BaseSessionBound,  # noqa: ARG001
            /,
            *,
            name: Optional[str] = None,  # noqa: ARG001
        ) -> None:
            raise MissingPluginError("jupyterlab3")

        self._link = link
        self._visualize = visualize

    @property
    @abstractmethod
    def _client(self) -> ActiveViamClient:
        ...

    @property
    @abstractmethod
    def _location(self) -> Mapping[str, Any]:
        """Location data used to create a link to this session."""

    def link(
        self,
        *,
        path: str = "",
    ) -> object:
        """Display a link to this session.

        Clicking on the link will open it in a new browser tab.

        Note:
            This method requires the :mod:`atoti-jupyterlab3 <atoti_jupyterlab3>` plugin.

        The extension will try to access the session through (in that order):

        #. `Jupyter Server Proxy <https://jupyter-server-proxy.readthedocs.io/>`__ if it is enabled.
        #. ``f"{session_protocol}//{jupyter_server_hostname}:{session.port}"`` for :class:`atoti.Session` and ``session.url`` for :class:`atoti_query.QuerySession`.

        Args:
            path: The path to append to the session base URL.
                Defaults to the session home page.

        Example:
            Pointing directly to an existing dashboard:

            .. testcode::

                dashboard_id = "92i"
                session.link(path=f"#/dashboard/{dashboard_id}")

        """
        return self._link(self, path=path)

    @property
    @abstractmethod
    def cubes(self) -> CubesT:
        """Cubes of the session."""

    @property
    @abstractmethod
    def _security(self) -> _SecurityT:
        ...

    @property
    @abstractmethod
    def _local_url(self) -> str:
        """URL that can be used to access the session on the host machine's network."""

    def visualize(
        self,
        name: Optional[str] = None,
    ) -> None:
        """Display an Atoti widget to explore the session interactively.

        Note:
            This method requires the :mod:`atoti-jupyterlab3 <atoti_jupyterlab3>` plugin.

        The widget state will be stored in the cell metadata.
        This state should not have to be edited but, if desired, it can be found in JupyterLab by opening the "Notebook tools" sidebar and expanding the "Advanced Tools" section.

        Args:
            name: The name to give to the widget.
        """
        return self._visualize(self, name=name)

    @property
    def _id(self) -> str:
        return self.__id

    @doc(
        f"""Execute an MDX query and return its result as a pandas DataFrame.

        Args:

            mdx: The MDX ``SELECT`` query to execute.

                Regardless of the axes on which levels and measures appear in the MDX, the returned DataFrame will have all levels on rows and measures on columns.

                Example:

                    .. doctest:: query_mdx

                        >>> from datetime import date
                        >>> df = pd.DataFrame(
                        ...     columns=["Country", "Date", "Price"],
                        ...     data=[
                        ...         ("China", date(2020, 3, 3), 410.0),
                        ...         ("France", date(2020, 1, 1), 480.0),
                        ...         ("France", date(2020, 2, 2), 500.0),
                        ...         ("France", date(2020, 3, 3), 400.0),
                        ...         ("India", date(2020, 1, 1), 360.0),
                        ...         ("India", date(2020, 2, 2), 400.0),
                        ...         ("UK", date(2020, 2, 2), 960.0),
                        ...     ],
                        ... )
                        >>> table = session.read_pandas(
                        ...     df, keys=["Country", "Date"], table_name="Prices"
                        ... )
                        >>> cube = session.create_cube(table)

                    This MDX:

                    .. doctest:: query_mdx

                        >>> mdx = (
                        ...     "SELECT"
                        ...     "  NON EMPTY Hierarchize("
                        ...     "    DrilldownLevel("
                        ...     "      [Prices].[Country].[ALL].[AllMember]"
                        ...     "    )"
                        ...     "  ) ON ROWS,"
                        ...     "  NON EMPTY Crossjoin("
                        ...     "    [Measures].[Price.SUM],"
                        ...     "    Hierarchize("
                        ...     "      DrilldownLevel("
                        ...     "        [Prices].[Date].[ALL].[AllMember]"
                        ...     "      )"
                        ...     "    )"
                        ...     "  ) ON COLUMNS"
                        ...     "  FROM [Prices]"
                        ... )

                    Returns this DataFrame:

                    .. doctest:: query_mdx

                        >>> session.query_mdx(mdx, keep_totals=True)
                                           Price.SUM
                        Date       Country
                        Total               3,510.00
                        2020-01-01            840.00
                        2020-02-02          1,860.00
                        2020-03-03            810.00
                                   China      410.00
                        2020-01-01 China
                        2020-02-02 China
                        2020-03-03 China      410.00
                                   France   1,380.00
                        2020-01-01 France     480.00
                        2020-02-02 France     500.00
                        2020-03-03 France     400.00
                                   India      760.00
                        2020-01-01 India      360.00
                        2020-02-02 India      400.00
                        2020-03-03 India
                                   UK         960.00
                        2020-01-01 UK
                        2020-02-02 UK         960.00
                        2020-03-03 UK

                    But, if it was displayed into a pivot table, would look like this:

                    +---------+-------------------------------------------------+
                    | Country | Price.sum                                       |
                    |         +----------+------------+------------+------------+
                    |         | Total    | 2020-01-01 | 2020-02-02 | 2020-03-03 |
                    +---------+----------+------------+------------+------------+
                    | Total   | 3,510.00 | 840.00     | 1,860.00   | 810.00     |
                    +---------+----------+------------+------------+------------+
                    | China   | 410.00   |            |            | 410.00     |
                    +---------+----------+------------+------------+------------+
                    | France  | 1,380.00 | 480.00     | 500.00     | 400.00     |
                    +---------+----------+------------+------------+------------+
                    | India   | 760.00   | 360.00     | 400.00     |            |
                    +---------+----------+------------+------------+------------+
                    | UK      | 960.00   |            | 960.00     |            |
                    +---------+----------+------------+------------+------------+

                    .. doctest:: query_mdx
                        :hide:

                        Clear the session to isolate the multiple methods sharing this docstring.
                        >>> session._clear()

            keep_totals: Whether the resulting DataFrame should contain, if they are present in the query result, the grand total and subtotals.
                {QUERY_ARGS_DOC["totals"]}

            {QUERY_ARGS_DOC["timeout"]}

            {QUERY_ARGS_DOC["mode"]}

              {QUERY_ARGS_DOC["pretty"]}

              {QUERY_ARGS_DOC["raw"]}

            {QUERY_ARGS_DOC["context"]}
        """
    )
    @abstractmethod
    def query_mdx(
        self,
        mdx: str,
        *,
        keep_totals: bool = False,
        timeout: timedelta = DEFAULT_QUERY_TIMEOUT,
        mode: Literal["pretty", "raw"] = "pretty",
        context: Context = EMPTY_MAPPING,
    ) -> pd.DataFrame:
        ...

    @abstractmethod
    def _generate_auth_headers(self) -> dict[str, str]:
        """Generate authentication headers that can be used to authenticate against this session."""

    def _get_widget_creation_code(self) -> Optional[str]:
        session_variable_name = find_corresponding_top_level_variable_name(self)

        return f"{session_variable_name}.visualize()" if session_variable_name else None

    def _block_until_widget_loaded(self, widget_id: str) -> None:
        # Nothing to do by default.
        ...

    def _repr_json_(self) -> ReprJson:
        cubes = self.cubes._repr_json_()[0]
        data = (
            {"Tables": cast(Any, self).tables._repr_json_()[0], "Cubes": cubes}
            if hasattr(self, "tables")
            else {"Cubes": cubes}
        )
        return (
            data,
            {"expanded": False, "root": type(self).__name__},
        )


BaseSessionBound = BaseSession[BaseCubesBound, Any]
