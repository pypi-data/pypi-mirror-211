from collections.abc import Mapping

import atoti as tt
from atoti._external_table_coordinates import ExternalTableCoordinates
from atoti.directquery._external_database_with_cache_connection import (
    ExternalDatabaseWithCacheConnection,
)

from .table import BigqueryTable


class BigqueryConnection(ExternalDatabaseWithCacheConnection[BigqueryTable]):
    """Connection to an external BigQuery database.

    Use :meth:`atoti.Session.connect_to_external_database` to create one.

    Example:
        >>> from atoti_directquery_bigquery import BigqueryConnectionInfo
        >>> connection_info = BigqueryConnectionInfo()
        >>> external_database = session.connect_to_external_database(connection_info)
    """

    def _create_table(
        self,
        coordinates: ExternalTableCoordinates,
        /,
        *,
        types: Mapping[str, tt.DataType],
    ) -> BigqueryTable:
        return BigqueryTable(
            _coordinates=coordinates, types=types, _database_key=self._database_key
        )
