#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
Redshift usage module
"""

# This import verifies that the dependencies are available.
import logging
from typing import Any, Dict, Iterable, Iterator, Union

# pylint: disable=useless-super-delegation
from metadata.generated.schema.entity.services.connections.database.redshiftConnection import (
    RedshiftConnection,
)
from metadata.generated.schema.entity.services.databaseService import (
    DatabaseServiceType,
)
from metadata.generated.schema.metadataIngestion.workflow import (
    Source as WorkflowSource,
)
from metadata.generated.schema.metadataIngestion.workflow import WorkflowConfig
from metadata.ingestion.api.source import InvalidSourceException, Source, SourceStatus
from metadata.ingestion.models.table_queries import TableQuery
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.ingestion.source.sql_alchemy_helper import SQLSourceStatus
from metadata.utils.connections import get_connection, test_connection
from metadata.utils.helpers import get_start_and_end
from metadata.utils.sql_queries import REDSHIFT_SQL_STATEMENT

logger = logging.getLogger(__name__)


class RedshiftUsageSource(Source[TableQuery]):
    # SELECT statement from mysql information_schema to extract table and column metadata
    SQL_STATEMENT = REDSHIFT_SQL_STATEMENT
    # CONFIG KEYS
    WHERE_CLAUSE_SUFFIX_KEY = "where_clause"
    CLUSTER_SOURCE = "cluster_source"
    CLUSTER_KEY = "cluster_key"
    USE_CATALOG_AS_CLUSTER_NAME = "use_catalog_as_cluster_name"
    DATABASE_KEY = "database_key"
    SERVICE_TYPE = DatabaseServiceType.Redshift.value
    DEFAULT_CLUSTER_SOURCE = "CURRENT_DATABASE()"

    def __init__(self, config: WorkflowSource, metadata_config: WorkflowConfig):
        super().__init__()
        self.config = config
        self.service_connection = config.serviceConnection.__root__.config
        self.metadata_config = metadata_config
        self.metadata = OpenMetadata(metadata_config)
        start, end = get_start_and_end(self.config.sourceConfig.config.queryLogDuration)
        self.sql_stmt = RedshiftUsageSource.SQL_STATEMENT.format(
            start_time=start, end_time=end
        )
        self.analysis_date = start
        self._extract_iter: Union[None, Iterator] = None
        self._database = "redshift"
        self.status = SQLSourceStatus()
        self.engine = get_connection(self.service_connection)

    @classmethod
    def create(cls, config_dict, metadata_config: WorkflowConfig):
        config: WorkflowSource = WorkflowSource.parse_obj(config_dict)
        connection: RedshiftConnection = config.serviceConnection.__root__.config
        if not isinstance(connection, RedshiftConnection):
            raise InvalidSourceException(
                f"Expected RedshiftConnection, but got {connection}"
            )
        return cls(config, metadata_config)

    def prepare(self):
        pass

    def _get_raw_extract_iter(self) -> Iterable[Dict[str, Any]]:

        rows = self.engine.execute(self.sql_stmt)
        for row in rows:
            yield row

    def next_record(self) -> Iterable[TableQuery]:
        """
        Using itertools.groupby and raw level iterator, it groups to table and yields TableMetadata
        :return:
        """
        for row in self._get_raw_extract_iter():
            tq = TableQuery(
                query=row["query"],
                user_name=row["usename"],
                starttime=str(row["starttime"]),
                endtime=str(row["endtime"]),
                analysis_date=str(self.analysis_date),
                database=self.service_connection.database,
                aborted=row["aborted"],
                sql=row["querytxt"],
                service_name=self.config.serviceName,
            )
            yield tq

    def close(self):
        pass

    def get_status(self) -> SourceStatus:
        return self.status

    def test_connection(self) -> None:
        test_connection(self.engine)
