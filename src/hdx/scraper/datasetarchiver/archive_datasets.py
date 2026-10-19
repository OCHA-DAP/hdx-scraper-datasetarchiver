import logging

from dateutil.relativedelta import relativedelta
from hdx.api.utilities.date_helper import DateHelper
from hdx.data.dataset import Dataset
from hdx.utilities.dateparse import parse_date

logger = logging.getLogger(__name__)


def archive(configuration, today, DatasetCls=Dataset):
    already_archived = []
    not_archived = []
    archived = []
    for org_name, fields_to_match in configuration["orgs"].items():
        org_already_archived = []
        org_not_archived = []
        org_archived = []
        logger.info(f"Organisation: {org_name}\n")
        set_update_frequency_never = fields_to_match.pop(
            "set_update_frequency_never", False
        )
        for name in fields_to_match:
            if name == "before":
                for field_name, match_value in fields_to_match["before"].items():
                    date = today - relativedelta(**match_value)
                    fields_to_match["before"][field_name] = date

        datasets = DatasetCls.search_in_hdx(fq=f"organization:{org_name}")
        for dataset in datasets:
            if dataset["archived"]:
                org_already_archived.append(dataset)
                continue
            match = True
            for field_name, match_value in fields_to_match.items():
                if field_name == "before":
                    for field_name, match_value in fields_to_match["before"].items():
                        if field_name == "dataset_date":
                            time_period = DateHelper.get_time_period_info(
                                dataset[field_name], today=today
                            )
                            field_value = time_period.get("enddate")
                        else:
                            field_value = parse_date(dataset[field_name])
                        if field_value is None or field_value >= match_value:
                            match = False
                            break
                    continue
                field_value = dataset[field_name]
                if field_value != match_value:
                    match = False
                    break
            if match:
                name = dataset["name"]
                title = dataset["title"]
                logger.info(
                    f"Archiving dataset: {name} with title: {title} and url: {dataset.get_hdx_url()}"
                )
                dataset["archived"] = True
                if set_update_frequency_never:
                    dataset["data_update_frequency"] = "-1"
                dataset.update_in_hdx(
                    operation="patch",
                    batch_mode="KEEP_OLD",
                    skip_validation=True,
                    ignore_check=True,
                )
                org_archived.append(dataset)
            else:
                org_not_archived.append(dataset)
        logger.info(f"{org_name}: {len(org_archived)} datasets archived!\n")
        logger.info(f"{org_name}: {len(org_not_archived)} datasets not archived!\n")
        logger.info(
            f"{org_name}: {len(org_already_archived)} datasets already archived!\n"
        )
        archived.extend(org_archived)
        not_archived.extend(org_not_archived)
        already_archived.extend(org_already_archived)
    return archived, not_archived, already_archived
