import os
import time
import numpy as np
import json
import gzip
import concurrent.futures
import requests


def fetch_assets_from_github(url_seq, time_out=60):
    """
    Downloads reference data from github rep, updated periodically.
    """

    def fetch_asset(url, time_out=time_out):
        response = requests.get(url, timeout=(time_out, time_out + 15))
        return json.loads(gzip.decompress(response.content))

    datasets = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_asset, url) for url in url_seq]
    executor.shutdown()
    return [future.result() for future in futures]


def format_time(ts):
    """Converts UNIX timestamp to local timestring with human-readable format"""
    return time.strftime("%d %B %Y, %I:%M %p", time.localtime(int(ts)))


def wipe_resource_id(rsrc_id):
    """Basic cleaning of resource-id string."""
    rsrc_id = "".join([c for c in str(rsrc_id) if c.isalnum()]).strip()
    assert len(rsrc_id) == 32, "{} is not a valid Resource-ID".format(rsrc_id)
    return rsrc_id


def scrub_resource_id(rsrc_id):
    """Converts Resource-ID in the correct format
    acceptable format : 8,4,4,4,12
    """
    rsrc_id = wipe_resource_id(rsrc_id)
    rsrc_id = "-".join(
        [rsrc_id[:8], rsrc_id[8:12], rsrc_id[12:16], rsrc_id[16:20], rsrc_id[20:32]]
    )
    assert len(rsrc_id) == 36, "{} is not a valid Resource-ID".format(rsrc_id)
    return rsrc_id


def fetch_nrecords(resourceid, api_key):
    """
    Fetch number of records in realtime
    resourceid must be in in `scrub_resource_id` format
    """
    try:
        url = "https://api.data.gov.in/resource/{}?api-key={}&format=json&offset=0&limit=0".format(
            scrub_resource_id(resourceid), api_key
        )
        response = requests.get(url).json()
        total = response.get("total", np.inf)
    except:
        total = np.inf
    return total


class git_assets:
    """
    Holds json serialized static files for `data.gov.in` resources,
    indexed by resource-id(s).
    """

    def __init__(self):
        # Change absolute path to relative path
        #
        print(
            ".... Step (2/2) - Loading latest API reference data. This may take a few seconds......... \r",
            end="",
        )
        util_base_url = "https://raw.github.com/addypy/datagovindia/master/data/"
        attribute_fp = util_base_url + "attributes.gz"
        idx_map_fp = util_base_url + "idx_maps.gz"
        field_label_fp = util_base_url + "fieldlabel_map.gz"
        field_dtype_fp = util_base_url + "fielddtype_map.gz"
        org_idx_fp = util_base_url + "orgidx_map.gz"
        orgtype_idx_fp = util_base_url + "orgtypeidx_map.gz"
        source_idx_fp = util_base_url + "sourceidx_map.gz"
        sector_idx_fp = util_base_url + "sectoridx_map.gz"

        asset_url_seq = [
            attribute_fp,
            idx_map_fp,
            org_idx_fp,
            orgtype_idx_fp,
            source_idx_fp,
            sector_idx_fp,
            field_label_fp,
            field_dtype_fp,
        ]
        print(
            ".... Step (2/2) - Loading latest API meta-data. This may take a few seconds........               \r",
            end="",
        )
        asset_data = fetch_assets_from_github(asset_url_seq)
        print(
            ".... Step (2/2) - Loading latest API meta-data. This may take a few seconds......                   \r",
            end="",
        )
        self.attribute_dict = asset_data[0]
        self.idx_map = asset_data[1]
        self.org_idx_map = asset_data[2]
        self.orgtype_idx_map = asset_data[3]
        self.source_idx_map = asset_data[4]
        self.sector_idx_map = asset_data[5]
        self.field_label_map = asset_data[6]
        self.field_dtype_map = asset_data[7]
        print(
            ".... Step (2/2) - Loading latest API meta-data. This may take a few seconds.....                    \r",
            end="",
        )
        self.resource_ids = np.array([k.get("resourceid") for k in self.idx_map])
        self.idx_title_map = [
            {k.get("resourceid"): k.get("title", "")} for k in self.idx_map
        ]
        self.idx_desc_map = [
            {k.get("resourceid"): k.get("desc", "")} for k in self.idx_map
        ]
        self.idx_creationtime_map = [
            {k.get("resourceid"): k.get("date_created", np.nan)} for k in self.idx_map
        ]
        self.idx_updationtime_map = [
            {k.get("resourceid"): k.get("date_updated", np.nan)} for k in self.idx_map
        ]
        self.idx_field_map = [
            {k.get("resourceid"): k.get("fields", [])} for k in self.idx_map
        ]
        self.idx_source_map = [
            {k.get("resourceid"): k.get("source", "")} for k in self.idx_map
        ]
        self.idx_orgname_map = [
            {k.get("resourceid"): k.get("orgnames", [])} for k in self.idx_map
        ]
        self.idx_orgtype_map = [
            {k.get("resourceid"): k.get("orgtype", "")} for k in self.idx_map
        ]
        self.idx_sector_map = [
            {k.get("resourceid"): k.get("sectors", [])} for k in self.idx_map
        ]
        print(
            ".... Step (2/2) - Loading latest API meta-data. This may take a few seconds...                            \r",
            end="",
        )

    def compile_resource_fields(self, rsrc_id):
        """
        Compile Field Information specific to resource.
        """
        fields = list(
            np.ravel(
                [
                    next(iter(d.values()))
                    for d in self.idx_field_map
                    if next(iter(d)) == rsrc_id
                ]
            )
        )
        labels = [self.field_label_map[f] for f in fields]
        return {fields[f]: labels[f] for f in range(len(fields))}

    def compile_all_information(self, rsrc_id, api_key):
        """ """
        if rsrc_id in self.resource_ids:
            title = [
                list(item.values())[0]
                for item in self.idx_title_map
                if list(item.keys())[0] == rsrc_id
            ][0]
            desc = [
                list(item.values())[0]
                for item in self.idx_desc_map
                if list(item.keys())[0] == rsrc_id
            ][0]
            nrecords = fetch_nrecords(scrub_resource_id(rsrc_id), api_key)
            created_on = format_time(
                [
                    list(item.values())[0]
                    for item in self.idx_creationtime_map
                    if list(item.keys())[0] == rsrc_id
                ][0]
            )
            updated_on = format_time(
                [
                    list(item.values())[0]
                    for item in self.idx_updationtime_map
                    if list(item.keys())[0] == rsrc_id
                ][0]
            )
            orgnames = list(
                np.ravel(
                    [
                        list(item.values())
                        for item in self.idx_orgname_map
                        if list(item.keys())[0] == rsrc_id
                    ]
                )
            )
            org_type = np.ravel(
                [
                    list(item.values())
                    for item in self.idx_orgtype_map
                    if list(item.keys())[0] == rsrc_id
                ][0]
            )[0]
            sector = np.ravel(
                [
                    list(item.values())
                    for item in self.idx_sector_map
                    if list(item.keys())[0] == rsrc_id
                ][0]
            )[0]
            source = np.ravel(
                [
                    list(item.values())
                    for item in self.idx_source_map
                    if list(item.keys())[0] == rsrc_id
                ][0]
            )[0]
            fields = list(
                np.ravel(
                    [
                        list(item.values())
                        for item in self.idx_field_map
                        if list(item.keys())[0] == rsrc_id
                    ][0]
                )
            )
            ApiInformation = {
                "ResourceID": rsrc_id,
                "Title": title,
                "Description": desc,
                "TotalRecords": nrecords,
                "DateCreated": created_on,
                "DateUdpated": updated_on,
                "OrganizationNames": orgnames,
                "OrganizationTypes": org_type,
                "Sector": sector,
                "Source": source,
                "Fields": fields,
            }
        else:
            print("{} is not a valid Resource-ID".format(rsrc_id))
            ApiInformation = {}
        return ApiInformation
