from os.path import expanduser, join

from hdx.api.configuration import Configuration
from hdx.facades.simple import facade
from hdx.utilities.dateparse import now_utc

from hdx.scraper.datasetarchiver.archive_datasets import archive


def main():
    archive(Configuration.read(), now_utc())


if __name__ == "__main__":
    facade(
        main,
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="hdx-scraper-datasetarchiver",
        project_config_yaml=join("config", "project_configuration.yaml"),
    )
