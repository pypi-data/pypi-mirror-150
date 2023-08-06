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
"""Metadata source module"""

import logging
from dataclasses import dataclass, field
from typing import Iterable, List

from metadata.generated.schema.entity.data.dashboard import Dashboard
from metadata.generated.schema.entity.data.glossaryTerm import GlossaryTerm
from metadata.generated.schema.entity.data.pipeline import Pipeline
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.entity.data.topic import Topic
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.entity.teams.team import Team
from metadata.generated.schema.entity.teams.user import User
from metadata.generated.schema.metadataIngestion.workflow import (
    Source as WorkflowSource,
)
from metadata.ingestion.api.common import Entity
from metadata.ingestion.api.source import Source, SourceStatus

logger = logging.getLogger(__name__)


@dataclass
class MetadataSourceStatus(SourceStatus):
    """Metadata Source class -- extends SourceStatus class

    Attributes:
        success:
        failures:
        warnings:
    """

    success: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def scanned_table(self, table_name: str) -> None:
        """scanned table method

        Args:
            table_name (str):
        """
        self.success.append(table_name)
        logger.info("Table Scanned: %s", table_name)

    def scanned_topic(self, topic_name: str) -> None:
        """scanned topic method

        Args:
            topic_name (str):
        """
        self.success.append(topic_name)
        logger.info("Topic Scanned: %s", topic_name)

    def scanned_dashboard(self, dashboard_name: str) -> None:
        """scanned dashboard method

        Args:
            dashboard_name (str)
        """
        self.success.append(dashboard_name)
        logger.info("Dashboard Scanned: %s", dashboard_name)

    def scanned_team(self, team_name: str) -> None:
        """scanned team method

        Args:
            team_name (str)
        """
        self.success.append(team_name)
        logger.info("Team Scanned: %s", team_name)

    def scanned_user(self, user_name: str) -> None:
        """scanned user method

        Args:
            user_name (str)
        """
        self.success.append(user_name)
        logger.info("User Scanned: %s", user_name)

    def scanned_glossary_term(self, glossary_term: str) -> None:
        """scanned glossary method

        Args:
            glossary_term (str)
        """
        self.success.append(glossary_term)
        logger.info("Glossary Term Scanned: %s", glossary_term)

    # pylint: disable=unused-argument
    def filtered(
        self, table_name: str, err: str, dataset_name: str = None, col_type: str = None
    ) -> None:
        """filtered methods

        Args:
            table_name (str):
            err (str):
        """
        self.warnings.append(table_name)
        logger.warning("Dropped Entity %s due to %s", table_name, err)


class MetadataSource(Source[Entity]):
    """Metadata source class

    Args:
        config:
        metadata_config:

    Attributes:
        config:
        report:
        metadata_config:
        status:
        wrote_something:
        metadata:
        tables:
        topics:
    """

    config: WorkflowSource
    report: SourceStatus

    def __init__(
        self,
        config: WorkflowSource,
        metadata_config: OpenMetadataConnection,
    ):
        super().__init__()
        self.config = config
        self.metadata_config = metadata_config
        self.service_connection = config.serviceConnection.__root__.config
        self.status = MetadataSourceStatus()
        self.wrote_something = False
        self.metadata = None
        self.tables = None
        self.topics = None

    def prepare(self):
        pass

    @classmethod
    def create(cls, config_dict, metadata_config: OpenMetadataConnection):
        raise NotImplementedError("Create Method not implemented")

    def next_record(self) -> Iterable[Entity]:
        yield from self.fetch_table()
        yield from self.fetch_topic()
        yield from self.fetch_dashboard()
        yield from self.fetch_pipeline()
        yield from self.fetch_users()
        yield from self.fetch_teams()
        yield from self.fetch_glossary_terms()

    def fetch_table(self) -> Table:
        """Fetch table method

        Returns:
            Table
        """
        if self.service_connection.includeTables:
            after = None
            while True:
                table_entities = self.metadata.list_entities(
                    entity=Table,
                    fields=[
                        "columns",
                        "tableConstraints",
                        "usageSummary",
                        "owner",
                        "tags",
                        "followers",
                    ],
                    after=after,
                    limit=self.service_connection.limitRecords,
                )
                for table in table_entities.entities:
                    self.status.scanned_table(table.name.__root__)
                    yield table
                if table_entities.after is None:
                    break
                after = table_entities.after

    def fetch_topic(self) -> Topic:
        """fetch topic method

        Returns:
            Topic
        """
        if self.service_connection.includeTopics:
            after = None
            while True:
                topic_entities = self.metadata.list_entities(
                    entity=Topic,
                    fields=["owner", "tags", "followers"],
                    after=after,
                    limit=self.service_connection.limitRecords,
                )
                for topic in topic_entities.entities:
                    self.status.scanned_topic(topic.name.__root__)
                    yield topic
                if topic_entities.after is None:
                    break
                after = topic_entities.after

    def fetch_dashboard(self) -> Dashboard:
        """fetch dashboard method

        Returns:
            Dashboard:
        """
        if self.service_connection.includeDashboards:
            after = None
            while True:
                dashboard_entities = self.metadata.list_entities(
                    entity=Dashboard,
                    fields=[
                        "owner",
                        "tags",
                        "followers",
                        "charts",
                        "usageSummary",
                    ],
                    after=after,
                    limit=self.service_connection.limitRecords,
                )
                for dashboard in dashboard_entities.entities:
                    self.status.scanned_dashboard(dashboard.name)
                    yield dashboard
                if dashboard_entities.after is None:
                    break
                after = dashboard_entities.after

    def fetch_pipeline(self) -> Pipeline:
        """fetch pipeline method

        Returns:
            Pipeline:
        """
        if self.service_connection.includePipelines:
            after = None
            while True:
                pipeline_entities = self.metadata.list_entities(
                    entity=Pipeline,
                    fields=["owner", "tags", "followers", "tasks"],
                    after=after,
                    limit=self.service_connection.limitRecords,
                )
                for pipeline in pipeline_entities.entities:
                    self.status.scanned_dashboard(pipeline.name)
                    yield pipeline
                if pipeline_entities.after is None:
                    break
                after = pipeline_entities.after

    def fetch_users(self) -> User:
        """fetch users method

        Returns:
            User:
        """
        if self.service_connection.includeUsers:
            after = None
            while True:
                user_entities = self.metadata.list_entities(
                    entity=User,
                    fields=["teams", "roles"],
                    after=after,
                    limit=self.service_connection.limitRecords,
                )
                for user in user_entities.entities:
                    self.status.scanned_user(user.name)
                    yield user
                if user_entities.after is None:
                    break
                after = user_entities.after

    def fetch_teams(self) -> Team:
        """fetch teams method

        Returns:
            Team:
        """
        if self.service_connection.includeTeams:
            after = None
            while True:
                team_entities = self.metadata.list_entities(
                    entity=Team,
                    fields=["users", "owns"],
                    after=after,
                    limit=self.service_connection.limitRecords,
                )
                for team in team_entities.entities:
                    self.status.scanned_team(team.name)
                    yield team
                if team_entities.after is None:
                    break
                after = team_entities.after

    def fetch_glossary_terms(self) -> GlossaryTerm:
        """fetch glossary terms method

        Returns:
            GlossaryTerm:
        """
        if self.service_connection.includeGlossaryTerms:
            after = None
            while True:
                glossary_term_entities = self.metadata.list_entities(
                    entity=GlossaryTerm,
                    fields=[],
                    after=after,
                    limit=self.service_connection.limitRecords,
                )
                for glossary_term in glossary_term_entities.entities:
                    self.status.scanned_team(glossary_term.name)
                    yield glossary_term
                if glossary_term_entities.after is None:
                    break
                after = glossary_term_entities.after

    def get_status(self) -> SourceStatus:
        return self.status

    def close(self):
        pass

    def test_connection(self) -> None:
        pass
