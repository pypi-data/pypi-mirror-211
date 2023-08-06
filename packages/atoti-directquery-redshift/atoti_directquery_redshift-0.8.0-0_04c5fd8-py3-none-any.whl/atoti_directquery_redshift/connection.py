from collections.abc import Mapping

import atoti as tt
from atoti._external_table_coordinates import ExternalTableCoordinates
from atoti.directquery._external_database_with_cache_connection import (
    ExternalDatabaseWithCacheConnection,
)

from .table import RedshiftTable


class RedshiftConnection(ExternalDatabaseWithCacheConnection[RedshiftTable]):
    """Connection to an external Redshift database.

    Use :meth:`atoti.Session.connect_to_external_database` to create one.

    Example :

    .. doctest::
        :hide:

        >>> import os
        >>> from atoti_directquery_redshift import RedshiftConnectionInfo
        >>> connection_info = RedshiftConnectionInfo(
        ...     f"jdbc:redshift://{os.environ['REDSHIFT_ACCOUNT_IDENTIFIER']}.redshift.amazonaws.com:5439/dev?user={os.environ['REDSHIFT_USERNAME']}&schema=test_resources",
        ...     password=os.environ["REDSHIFT_PASSWORD"],
        ... )

    .. doctest::

        >>> external_database = session.connect_to_external_database(connection_info)
    """

    def _create_table(
        self,
        coordinates: ExternalTableCoordinates,
        /,
        *,
        types: Mapping[str, tt.DataType],
    ) -> RedshiftTable:
        return RedshiftTable(
            _coordinates=coordinates, types=types, _database_key=self._database_key
        )
