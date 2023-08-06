from collections.abc import Mapping

import atoti as tt
from atoti._external_table_coordinates import ExternalTableCoordinates
from atoti.directquery._external_database_with_cache_connection import (
    ExternalDatabaseWithCacheConnection,
)

from .table import ClickhouseTable


class ClickhouseConnection(ExternalDatabaseWithCacheConnection[ClickhouseTable]):
    """Connection to an external ClickHouse database.

    Use :meth:`atoti.Session.connect_to_external_database` to create one.
    """

    def _create_table(
        self,
        coordinates: ExternalTableCoordinates,
        /,
        *,
        types: Mapping[str, tt.DataType],
    ) -> ClickhouseTable:
        return ClickhouseTable(
            _coordinates=coordinates, types=types, _database_key=self._database_key
        )
