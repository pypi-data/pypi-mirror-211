from collections.abc import Mapping

import atoti as tt
from atoti._external_table_coordinates import ExternalTableCoordinates
from atoti.directquery._external_database_connection import ExternalDatabaseConnection

from .table import SynapseTable


class SynapseConnection(ExternalDatabaseConnection[SynapseTable]):
    """Connection to an external Synapse database.

    This connection can be created from a :class:`atoti.Session`.

    Example:
        .. doctest::
            :hide:

            >>> import os
            >>> from atoti_directquery_synapse import SynapseConnectionInfo
            >>> connection_info = SynapseConnectionInfo(
            ...     f"jdbc:sqlserver://tck-directquery-ondemand.sql.azuresynapse.net;authentication={os.environ['SYNAPSE_AUTHENTICATION_METHOD']};database=test_resources;user={os.environ['SYNAPSE_USERNAME']}",
            ...     password=os.environ["SYNAPSE_PASSWORD"],
            ... )

        .. doctest::

            >>> external_database = session.connect_to_external_database(
            ...     connection_info
            ... )

    """

    def _create_table(
        self,
        coordinates: ExternalTableCoordinates,
        /,
        *,
        types: Mapping[str, tt.DataType],
    ) -> SynapseTable:
        return SynapseTable(
            _coordinates=coordinates, types=types, _database_key=self._database_key
        )
