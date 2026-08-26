from collections import UserDict
from os.path import join

import pytest
from hdx.api.configuration import Configuration
from hdx.utilities.dateparse import parse_date
from hdx.utilities.useragent import UserAgent

from hdx.scraper.datasetarchiver.archive_datasets import archive


class CutDownDataset(UserDict):
    def get_hdx_url(self):
        return f"https://data.humdata.org/dataset/{self.data['name']}"

    def update_in_hdx(self, **args):
        return


class TestDataset:
    @staticmethod
    def search_in_hdx(fq):
        if "unosat" in fq:
            datasets = [
                {
                    "name": "unosat-test-recent",
                    "title": "unosat test recent",
                    "last_modified": "2023-10-10T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": False,
                },
                {
                    "name": "unosat-test2-recent",
                    "title": "unosat test 2 recent",
                    "last_modified": "2023-04-12T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": False,
                },
                {
                    "name": "unosat-test-should_archive",
                    "title": "unosat test old",
                    "last_modified": "2023-04-11T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": False,
                },
                {
                    "name": "unosat-test-should_not_archive",
                    "title": "unosat test old",
                    "last_modified": "2023-04-11T00:00:00",
                    "data_update_frequency": "-2",
                    "archived": False,
                },
            ]
        elif "philsa" in fq:
            datasets = [
                {
                    "name": "philsa-test-recent",
                    "title": "philsa test recent",
                    "last_modified": "2023-10-10T00:00:00",
                    "data_update_frequency": "-2",
                    "archived": False,
                },
                {
                    "name": "philsa-test-should_archive",
                    "title": "philsa test old",
                    "last_modified": "2023-04-11T00:00:00",
                    "data_update_frequency": "-2",
                    "archived": False,
                },
                {
                    "name": "philsa-test-should_not_archive",
                    "title": "philsa test frequency mismatch",
                    "last_modified": "2023-04-11T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": False,
                },
            ]
        else:
            datasets = [
                {
                    "name": "wfp-adam-test-recent",
                    "title": "wfp adam test recent",
                    "last_modified": "2023-04-12T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": False,
                },
                {
                    "name": "wfp-adam-test-should_archive",
                    "title": "wfp adam test old",
                    "last_modified": "2022-03-02T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": False,
                },
                {
                    "name": "wfp-adam-test-already_archived",
                    "title": "wfp adam test old",
                    "last_modified": "2022-03-02T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": True,
                },
            ]
        datasets = [CutDownDataset(dataset) for dataset in datasets]
        return datasets


class TestDatasetArchiver:
    @pytest.fixture(scope="function")
    def configuration(self):
        Configuration._create(
            hdx_read_only=True,
            user_agent="test",
            project_config_yaml=join("config", "project_configuration.yaml"),
        )
        UserAgent.set_global("test")
        return Configuration.read()

    def test_archive(self, configuration):
        today = parse_date("2023-10-12")
        archived, not_archived, already_archived = archive(
            configuration, today, DatasetCls=TestDataset
        )
        for dataset in archived:
            assert "should_archive" in dataset["name"]
        for dataset in not_archived:
            name = dataset["name"]
            assert "recent" in name or "should_not_archive" in name
        for dataset in already_archived:
            assert "already_archived" in dataset["name"]
