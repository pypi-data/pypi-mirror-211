from collections.abc import Mapping

import atoti as tt
from atoti._external_table_coordinates import ExternalTableCoordinates
from atoti.directquery._external_database_connection import ExternalDatabaseConnection

from .table import MsSqlTable


class MsSqlConnection(ExternalDatabaseConnection[MsSqlTable]):
    """Connection to an external Microsoft SQL Server database.

    Use :meth:`atoti.Session.connect_to_external_database` to create one.
    """

    def _create_table(
        self,
        coordinates: ExternalTableCoordinates,
        /,
        *,
        types: Mapping[str, tt.DataType],
    ) -> MsSqlTable:
        return MsSqlTable(
            _coordinates=coordinates, types=types, _database_key=self._database_key
        )
