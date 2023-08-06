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
MSSQL usage module
"""

from typing import Any, Dict, Iterable

from metadata.generated.schema.entity.services.connections.database.mssqlConnection import (
    MssqlConnection,
)
from metadata.generated.schema.metadataIngestion.workflow import (
    Source as WorkflowSource,
)
from metadata.generated.schema.metadataIngestion.workflow import WorkflowConfig
from metadata.ingestion.api.source import InvalidSourceException, Source, SourceStatus

# This import verifies that the dependencies are available.
from metadata.ingestion.models.table_queries import TableQuery
from metadata.ingestion.source.sql_alchemy_helper import SQLSourceStatus
from metadata.utils.connections import get_connection, test_connection
from metadata.utils.helpers import get_start_and_end
from metadata.utils.sql_queries import MSSQL_SQL_USAGE_STATEMENT


class MssqlUsageSource(Source[TableQuery]):
    def __init__(self, config: WorkflowSource, metadata_config: WorkflowConfig):
        super().__init__()
        self.config = config
        self.connection = config.serviceConnection.__root__.config
        start, end = get_start_and_end(self.config.sourceConfig.config.queryLogDuration)
        self.analysis_date = start
        self.sql_stmt = MSSQL_SQL_USAGE_STATEMENT.format(start_date=start, end_date=end)
        self.report = SQLSourceStatus()
        self.engine = get_connection(self.connection)

    @classmethod
    def create(cls, config_dict, metadata_config: WorkflowConfig):
        """Create class instance"""
        config: WorkflowSource = WorkflowSource.parse_obj(config_dict)
        connection: MssqlConnection = config.serviceConnection.__root__.config
        if not isinstance(connection, MssqlConnection):
            raise InvalidSourceException(
                f"Expected MssqlConnection, but got {connection}"
            )
        return cls(config, metadata_config)

    def prepare(self):
        return super().prepare()

    def _get_raw_extract_iter(self) -> Iterable[Dict[str, Any]]:

        rows = self.engine.execute(self.sql_stmt)
        for row in rows:
            yield row

    def next_record(self) -> Iterable[TableQuery]:
        """
        Using itertools.groupby and raw level iterator,
        it groups to table and yields TableMetadata
        :return:
        """
        for row in self._get_raw_extract_iter():
            table_query = TableQuery(
                query=row["query_type"],
                user_name=row["user_name"],
                starttime=str(row["start_time"]),
                endtime=str(row["end_time"]),
                analysis_date=self.analysis_date,
                aborted=row["aborted"],
                database=row["database_name"],
                sql=row["query_text"],
                service_name=self.config.serviceName,
            )
            if row["schema_name"] is not None:
                self.report.scanned(f"{row['database_name']}.{row['schema_name']}")
            else:
                self.report.scanned(f"{row['database_name']}")
            yield table_query

    def get_report(self):
        """
        get report

        Returns:
        """
        return self.report

    def close(self):
        pass

    def get_status(self) -> SourceStatus:
        return self.report

    def test_connection(self) -> None:
        test_connection(self.engine)
