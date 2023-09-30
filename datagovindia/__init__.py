"""
Python API-wrapper for Government of India’s [Open Government Data OGD platform](https://data.gov.in/)

datagovindia` is an API wrapper for the over 100,000 APIs available at Government of India’s 
[Open Government Data OGD platform](https://data.gov.in/ogpl_apis)

==============================================================================
                            LICENSE
==============================================================================

MIT License

Copyright (c) 2021 ADITYA KARAN CHHABRA and ABHISHEK ARORA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
==============================================================================

"""
# Libraries
import os
import re
import time
import difflib
import requests
import concurrent.futures
import numpy as np
import pandas as pd
from . import util

# Functions
def extract_keys(json_map):
    return np.ravel([list(j.keys()) for j in json_map])


def intersect(list_of_arrays):
    return list(set.intersection(*[set(x) for x in list_of_arrays]))


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


def calc_loop_steps(n, step_size, offset=0):
    """Calculates a list of 2-tuples for looping
    through `n` results with steps of size `step_size`.
    """
    steps = (n - offset) // step_size
    remainder = (n - offset) % step_size
    moves = [
        (offset + (step_size * s), offset + (step_size * (s + 1))) for s in range(steps)
    ]
    if remainder > 0:
        moves.append(
            (offset + (step_size * steps), (step_size * steps) + remainder + offset)
        )
    return moves


def regexmatch(s, pat):
    """Search `title` and `desc` fields

      Args:
          s   : `title` | `desc` field
          pat : search-query

    Removes whitespace and special characters in
    both `s` and `pat` before matching regular
    expressions.

      Returns:
          `bool` --> True/False
    """
    m = False
    special_chars = "[^a-zA-Z0-9\.]"
    if isinstance(s, str) == True:
        pat = re.sub(special_chars, "", pat)
        s = re.sub(special_chars, "", s)
        if re.search(pat, s, flags=re.I):
            m = True
    return m


def quickdict(json_map):
    """Quickly convert a mapping list to a dictionary."""
    D = {}
    for j in json_map:
        D.update(j)
    return D


def filtertime(timestamp, interval):
    """Check if timestamp is between timestamp_range - (time1,time2)

    Args:
        timestamp --> UNIX timestamp value.
        interval  --> `Tuple` of 2 UNIX timestamp values.

    Returns:
        `bool` --> True/False
    """
    T0, T1 = interval
    if (timestamp <= T1) and (timestamp >= T0):
        return True
    else:
        return False


def search_json(attr_map, query, n, error_handle=True):
    """Search imported JSON-object

    Args:
        attr_map : List((Dictionaries))
        query    : string to be matched

    Returns:

    """
    query = str(query)
    if len(query) > 0:
        results = list(
            filter(lambda x: regexmatch(list(x.values())[0], query), attr_map)
        )
        R = len(results)
        if R == 0:

            if error_handle == True:
                print("Found 0 results. Try searching with shorter queries")
            else:
                pass
            return []
        else:
            if error_handle == True:
                print("{} of {} results for : `{}`".format(min(R, n), R, query))
            else:
                pass
            return results[:n]
    else:
        if error_handle == True:
            print("Empty Query : Please enter a valid query")
        else:
            pass
        return []


def pp_results(results):
    if len(results) > 0:
        print(
            "\n==================================================================================\n"
        )
        for result in results:
            idx = list(result.keys())[0]
            val = list(result.values())[0]
            print("Resource-ID:\t{}\n\n{}".format(idx, val), end="\n\n")
            print(
                "==================================================================================\n"
            )


def pp_time_results(results):
    if len(results) > 0:
        print(
            "\n==================================================================================\n"
        )
        for result in results:
            idx = result["resourceid"]
            title = result["title"]
            ftime = util.format_time(result["timestamp"])
            print("Resource-ID:\t{}\n{}\n{}".format(idx, ftime, title), end="\n\n")
            print(
                "==================================================================================\n"
            )


def standard_fetch(url_seq, time_out=31):
    session = requests.Session()
    responses = []
    url_seq = np.unique(url_seq)
    error_count = 0
    error_thresh = np.ceil(len(url_seq) * 0.3)
    for url in url_seq:
        if error_count < error_thresh:
            try:
                response = session.get(url, timeout=(time_out, time_out + 15))
                resp_dict = response.json()
                if len(resp_dict["records"]) == 0:
                    error_count += 1
                    continue
                elif len(resp_dict["records"]) > 0:
                    responses.append(resp_dict)
            except:  # Enable better logging
                continue
        else:
            break
    session.close()
    return responses


def advanced_fetch(url_seq, time_out=31):
    def request_get(url, time_out=time_out):
        return requests.get(url, timeout=(time_out, time_out + 15))

    responses = []
    url_seq = np.unique(url_seq)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(request_get, url) for url in url_seq]
    executor.shutdown()
    for future in futures:
        try:
            resp_dict = future.result().json()
            responses.append(resp_dict)
        except:
            continue
    return responses


# Classes


class URLTool:
    def __init__(self, api_key, max_results=500):
        self.base_url_str = "https://api.data.gov.in/resource/"
        self.format_arg_str = "&format=json"
        self.resource_id_str = ""
        self.api_key = api_key.lower().strip()
        self.api_key_str = "?api-key={}".format(self.api_key)
        self.max_results = max_results
        self.offset_str = "&offset=0"
        self.limit_str = "&limit={}".format(self.max_results)
        self.filter_str = ""
        self.field_str = ""
        self.sort_str = ""

    def reset_params(self, max_results=500):
        self.base_url_str = "https://api.data.gov.in/resource/"
        self.format_arg_str = "&format=json"
        self.max_results = max_results
        self.offset_str = "&offset=0"
        self.limit_str = "&limit={}".format(self.max_results)
        self.filter_str = ""
        self.field_str = ""
        self.sort_str = ""

    def reset_resource(self, resource_id="", max_results=500):
        self.base_url_str = "https://api.data.gov.in/resource/"
        self.format_arg_str = "&format=json"
        self.resource_id_str = resource_id
        self.max_results = max_results
        self.offset_str = "&offset=0"
        self.limit_str = "&limit={}".format(self.max_results)
        self.filter_str = ""
        self.field_str = ""
        self.sort_str = ""

    def add_resource_id(self, resource_id):
        self.resource_id_str = scrub_resource_id(resource_id)

    def add_api_key(self, api_key):
        self.api_key = api_key.lower().strip()
        self.api_key_str = "?api-key={}".format(self.api_key)

    def add_offset(self, o):
        if isinstance(o, int):
            self.offset_str = "&offset={}".format(int(o))
        else:
            self.offset_str = "&offset=0"

    def add_limit(self, l):
        if isinstance(l, int):
            self.limit_str = "&limit={}".format(int(l))
        else:
            self.limit_str = "&limit={}".format(self.max_results)

    def add_filters(self, filter_key, filter_val):
        self.filter_str = "&filters[{}]={}".format(filter_key, filter_val)

    def add_fields(self, field_list):
        if (isinstance(field_list, list) or (isinstance(field_list, np.array))) & (
            len(field_list) > 0
        ):
            self.field_str = "&fields={}".format(",".join([f for f in field_list]))
        else:
            self.field_str = ""

    def add_sort_key(self, sortby_key, sort_order="asc"):
        if isinstance(sortby_key, str):
            if len(sortby_key) > 0:
                self.sort_str = "&sort[{}]={}".format(sortby_key, sort_order)
            else:
                self.sort_str = ""
        else:
            self.sort_str = ""

    def build(self):
        url_params = [
            self.base_url_str,
            self.resource_id_str,
            self.api_key_str,
            self.format_arg_str,
            self.offset_str,
            self.limit_str,
            self.filter_str,
            self.field_str,
            self.sort_str,
        ]
        url = "".join([u.strip() for u in url_params])
        return url

    def build_url_seq(self, offset=0, num_results=10000, max_results=1000):
        self.max_results = max_results
        loop_seq = calc_loop_steps(num_results, self.max_results, offset=offset)
        url_seq = []
        for (o, l) in loop_seq:
            self.add_offset(o)
            self.add_limit(min(self.max_results, num_results - o))
            url = self.build()
            url_seq.append(url)
        self.reset_params()
        return url_seq


class Resource:
    def __init__(self, DataGovIndia):
        self.parent = DataGovIndia
        self.resource_fields = []
        self.resource_index_string = ""
        self.rsrc_id = ""
        self.count = np.inf
        self.multi_thread = DataGovIndia.multi_thread
        self.sortkey = ""
        self.sort_order = "asc"
        self.offset = 0
        self.filters = []
        self.fields = []

    def set_resource_id(self, resource_index_string):
        self.resource_index_string = wipe_resource_id(resource_index_string)
        if self.resource_index_string not in self.parent.assets.resource_ids:
            print("{} is not a valid Resource-ID".format(resource_index_string))
        else:
            self.rsrc_id = scrub_resource_id(self.resource_index_string)
            try:
                self.count = util.fetch_nrecords(
                    self.resource_index_string, self.parent.api_key
                )
            except KeyError as err:
                self.count = np.inf

    def fetch_true_fields(self):
        if len(self.resource_fields) == 0:
            self.resource_fields = self.parent.idxfieldmap[self.resource_index_string]
            self.correct_field_list_str = "\n".join([f for f in self.resource_fields])
        else:
            pass

    def set_filters(self, filters):
        if isinstance(filters, list):
            if len(filters) > 0:
                filter_field_codes = np.unique(
                    np.hstack([list(f.keys()) for f in filters])
                )
                self.fetch_true_fields()
                potential_incorrect_fields = np.setdiff1d(
                    filter_field_codes, self.resource_fields, assume_unique=True
                )
                if len(potential_incorrect_fields) > 0:
                    incorrect_field_list_str = "; ".join(
                        [p for p in potential_incorrect_fields]
                    )
                    print(
                        "These field(s) are invalid for this resource - {}".format(
                            incorrect_field_list_str
                        ),
                        end="\n\n",
                    )
                    print(
                        "Valid field(s) are - \n{}".format(self.correct_field_list_str)
                    )

                else:
                    self.filters = filters
        else:
            self.filters = []

    def set_fields(self, fields):
        if len(fields) > 0:
            self.fetch_true_fields()
            potential_incorrect_fields = np.setdiff1d(
                fields, self.resource_fields, assume_unique=True
            )
            if len(potential_incorrect_fields) > 0:
                incorrect_field_list_str = "; ".join(
                    [p for p in potential_incorrect_fields]
                )

                print(
                    "These field(s) are invalid for this resource - {}".format(
                        incorrect_field_list_str
                    ),
                    end="\n\n",
                )
                print("Valid field(s) are - \n{}".format(self.correct_field_list_str))
            else:
                self.fields = fields

    def set_sort_key(self, sort_key, sort_order):
        if len(sort_key) > 0:
            self.fetch_true_fields()
            if sort_key not in self.resource_fields:
                close_matches = difflib.get_close_matches(
                    sort_key, self.resource_fields, n=1, cutoff=0.75
                )
                print(
                    "This field is invalid for this resource - {}".format(sort_key),
                    end="\n\n",
                )
                if len(close_matches) > 0:
                    print("Did you mean - {}?".format(close_matches[0]))
                else:
                    print("Valid fields are - \n{}".format(self.correct_field_list_str))

            else:
                self.sortkey = sort_key
                self.sort_order = sort_order

    def set_req_method(self, num=np.inf):
        self.num_results = min(self.count, num)
        if isinstance(self.num_results, int) == False:
            self.num_results = 10 ** 10

    def make_urls(self):
        urltool = URLTool(self.parent.api_key)
        urltool.add_resource_id(self.rsrc_id)
        self.url_seq = []
        if len(self.filters) > 0:
            for filter_dict in self.filters:
                for filter_key in filter_dict:
                    filter_values = filter_dict[filter_key]
                    if isinstance(filter_values, list) == False:
                        filter_values = [filter_values]
                    else:
                        pass
                    for val in filter_values:
                        urltool.add_fields(self.fields)
                        urltool.add_filters(filter_key, val)
                        urls = urltool.build_url_seq(
                            offset=self.offset,
                            num_results=self.num_results,
                            max_results=self.parent.max_results_per_req,
                        )
                        urltool.reset_params(
                            max_results=self.parent.max_results_per_req
                        )
                        self.url_seq.extend(urls)
        else:
            if len(self.fields) > 0:
                urltool.add_fields(self.fields)
                pass
            if len(self.sortkey) > 0:
                if self.sort_order in ["asc", "desc"]:
                    urltool.add_sort_key(self.sortkey, self.sort_order)
                else:
                    urltool.add_sort_key(self.sortkey, "asc")
                pass
            urls = urltool.build_url_seq(
                offset=self.offset,
                num_results=self.num_results,
                max_results=self.parent.max_results_per_req,
            )
            self.url_seq.extend(urls)

    def get_data(self):
        self.data = pd.DataFrame()
        if self.multi_thread == True:
            responses = advanced_fetch(self.url_seq, time_out=19)
        elif self.multi_thread == False:
            responses = standard_fetch(self.url_seq, time_out=19)
        for resp in responses:
            try:
                df = pd.DataFrame(resp["records"])
                self.data = self.data.append(df, ignore_index=True)
            except KeyError as err:
                continue
        return self.data.drop_duplicates()


def test_server(n=3):
    """
    Checks server status at datagovin.
    Returns list of n working-apis if server is functional.
    """

    server_response = {}
    working_api_url = "https://api.data.gov.in/lists?format=json&notfilters[source]=visualize.data.gov.in&filters[active]=1&offset=0&sort[updated]=desc&limit={}".format(
        n
    )
    working_api_response = requests.get(working_api_url, timeout=30)
    working_api_content = working_api_response.json()

    if working_api_content["status"] == "ok":
        records = working_api_content["records"]
        working_apis = [record.get("index_name", "") for record in records]
        working_apis = [w for w in working_apis if len(w) > 0]
        server_response["working_apis"] = working_apis
        server_response["status"] = True
    else:
        server_response["working_apis"] = []
        server_response["status"] = False
    return server_response


def validate_key(api_key, attempts=1):
    """
    Runs a quick test on server
    If server is UP, uses working-api-indices to fetch a dataframe
    """
    api_validity = False
    server_status = False
    if len(api_key) == 56:
        server_response = test_server(n=3)
        server_status = server_response["status"]
        test_api_idx_list = server_response["working_apis"]
        if server_status == True:
            for _ in range(attempts):
                test_api_idx = np.random.choice(test_api_idx_list)
                try:
                    urltool = URLTool(
                        api_key, max_results=10
                    )  # Dependency on previous func
                    urltool.add_resource_id(test_api_idx)
                    test_api_url = urltool.build()
                    test_response = requests.get(test_api_url, timeout=30)
                    test_content = test_response.json()
                    records = test_content["records"]
                    if len(records) > 0:
                        api_validity = True
                        break
                except:
                    api_validity = False
                    continue
    else:
        api_validity = False
        server_status = True
        pass
    return {"APIKEY": api_validity, "SERVER": server_status}


class DataGovIndia:
    """
    datagovindia
    ============

     A Python API-wrapper for Government of India’s [Open Government Data OGD platform](https://data.gov.in/)

    datagovindia` is an API wrapper for the over 80,000 APIs available at Government of India’s
    [Open Government Data OGD platform](https://data.gov.in/ogpl_apis)

    Features
    ========
    > DISCOVERY
        Find the right API resource.
    > INFORMATION
        Retrieve information about an API resource.
    > DATA
        Download data in a convenient pandas DataFrame from the chosen API.

    For more documentation, visit -
            https://github.com/addypy/datagovindia

    For the R/CRAN package, visit -
            https://github.com/econabhishek/datagovindia

            https://github.com/cran/datagovindia
    """

    sample_key = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

    def __init__(self, api_key, enable_multithreading=False):
        """
        Initialize `class` by providing a valid `api-key` from `data.gov.in/user`

        Args:
        =====
            `api_key` : API-KEY (str)

        Optional:
        =========
            `enable_multithreading`: (bool)
                    When `True`, enables faster downloads
                    with multi-threaded requests

        Note:
        =====
        Initializing this class may take a few seconds, depending on the speed
        of your internet connection.

        Initialization performs two key tasks:
            1) Tests server
            - Tests data.gov.in server to check if APIs are functional.
            2) Validates the API-key provided
            - Once validated, the API-key is stored and does not need to be entered again.
            3) Loads latest API meta-data.
            - Downloads and loads data containing the latest details of available APIs.

        """
        self.api_key = "".join([a for a in api_key if a.isalnum()]).lower().strip()
        print(
            ".... Step (1/2) - Validating API-Key                                      \r",
            end="",
        )
        validation_response = validate_key(self.api_key)
        self.is_key_valid, self.is_server_up = (
            validation_response["APIKEY"],
            validation_response["SERVER"],
        )
        if self.is_server_up == True:
            if self.is_key_valid == False:
                print(
                    "This key - {} is INVALID! Please generate a valid API key here - https://data.gov.in/user".format(
                        api_key
                    )
                )
            elif self.is_key_valid == True:
                if api_key == self.sample_key:
                    print(
                        "Step (1/2) : This API key is a sample-key with limited access.    ",
                        end="\n",
                    )
                    print(
                        "\tFor full access, generate a valid API key here - https://data.gov.in/user",
                        end="\n",
                    )
                    self.is_sample_key = True
                    pass
                else:
                    print(
                        "Step (1/2) : API key is VALID                               ",
                        end="\n",
                    )
                    print(
                        "\tYou don't need to enter it again                          ",
                        end="\n",
                    )
                    self.is_sample_key = False
                    pass
                self.max_results_per_req = 1000
                self.assets = util.git_assets()
                self.attributes = self.assets.attribute_dict
                self.org_types = self.attributes["org_types"]
                self.org_names = self.attributes["org_names"]
                self.sources = self.attributes["sources"]
                self.sectors = self.attributes["sectors"]
                self.idxtitlemap = quickdict(self.assets.idx_title_map)
                self.idxfieldmap = quickdict(self.assets.idx_field_map)
                self.resource = None
                self.error_handle = True
                self.multi_thread = enable_multithreading
                print(
                    "Step (2/2) : Latest API meta-data loaded! You may begin.                                                       \r",
                    end="\n",
                )
        else:
            print(
                "The `data.gov.in` server appears to be down. Please try a little while later."
            )

    def enable_multithreading(self):
        """Enables multi-thread API-requests for fast downloads of
        large datasets.
        """
        print("Multi-Threaded API requests enabled.")
        self.multi_thread = True

    def disable_multithreading(self):
        """Disables multi-thread API-requests."""
        print("Multi-Threaded API requests disabled.")
        self.multi_thread = False

    def list_org_types(self):
        """
        Returns list of organization-types as available on `data.gov.in`
        """
        return self.org_types

    def list_org_names(self):
        """
        Returns list of organizations-names as available on `data.gov.in`
        """
        return self.org_names

    def list_sectors(self):
        """
        Returns list of sectors listed on `data.gov.in`
        """
        return self.sectors

    def list_sources(self):
        """
        Returns list of data-sources listed on `data.gov.in`
        """
        return self.sources

    def list_all_attributes(self):
        """
        Returns a dictionary of lists -
            - Sectors
            - Sources
            - Organization-Types
            - Organization-Names
        """
        return self.attributes

    def list_recently_updated(self, days=7, max_results=10, print_results=True):
        """
        Returns list of resources updated in the last N days.

        Args:
            days          : Number of days. Defaults to 7.                (int)
            max_results   : number of results to return. Defaults to 10.  (int)
            print_results : prints results when enabled.                  (bool)
        Returns:
            List of resources with `titles` and `Resource-ID`s that were updated
            in the last `N` days.
        """
        TimeNow = int(time.time())
        TimePast = TimeNow - int(86400 * days)
        TimeInterval = (TimePast, TimeNow)

        filtered_json = list(
            filter(
                lambda x: filtertime(list(x.values())[0], TimeInterval),
                self.assets.idx_updationtime_map,
            )
        )
        num_total_results = len(filtered_json)
        timedict = quickdict(filtered_json)

        finalitems = [
            {k: v} for k, v in sorted(timedict.items(), key=lambda item: item[1])
        ][-max_results:]
        timedict = quickdict(finalitems)

        resourceids = list(timedict.keys())
        timestamps = list(timedict.values())
        titles = [self.idxtitlemap[r] for r in resourceids]

        results = [
            {
                "resourceid": resourceids[r],
                "timestamp": timestamps[r],
                "title": titles[r],
            }
            for r in range(len(resourceids))
        ]
        results.reverse()

        print(
            "{} of {} results that were updated in the last - `{}` days".format(
                len(results), num_total_results, days
            )
        )
        if print_results == True:
            pp_time_results(results)
        return results

    def list_recently_created(self, days=7, max_results=10, print_results=True):
        """
        Returns list of resources created in the last N days.

        Args:
            days          : Number of days. Defaults to 7.                (int)
            max_results   : number of results to return. Defaults to 10.  (int)
            print_results : prints results when enabled.                  (bool)
        Returns:
            List of resources with `titles` and `Resource-ID`s that were created
            in the last `N` days.
        """
        TimeNow = int(time.time())
        TimePast = TimeNow - int(86400 * days)
        TimeInterval = (TimePast, TimeNow)

        filtered_json = list(
            filter(
                lambda x: filtertime(list(x.values())[0], TimeInterval),
                self.assets.idx_creationtime_map,
            )
        )
        num_total_results = len(filtered_json)
        timedict = quickdict(filtered_json)

        finalitems = [
            {k: v} for k, v in sorted(timedict.items(), key=lambda item: item[1])
        ][-max_results:]
        timedict = quickdict(finalitems)

        resourceids = list(timedict.keys())
        timestamps = list(timedict.values())
        titles = [self.idxtitlemap[r] for r in resourceids]

        results = [
            {
                "resourceid": resourceids[r],
                "timestamp": timestamps[r],
                "title": titles[r],
            }
            for r in range(len(resourceids))
        ]
        results.reverse()

        print(
            "{} of {} results that were created in the last - `{}` days".format(
                len(results), num_total_results, days
            )
        )
        if print_results == True:
            pp_time_results(results)
        return results

    def search_by_title(self, query, max_results=10, print_results=True):
        """Search for a `data.gov.in` data-resource in `titles` of resources.

        Args:
            query         : the query string to search for.               (str)
            max_results   : number of results to return. Defaults to 10.  (int)
            print_results : prints results when enabled.                  (bool)
        Returns:
            List of matching resources with `titles` and `Resource-ID`s.
        """
        results = search_json(
            self.assets.idx_title_map, query, max_results, self.error_handle
        )
        if print_results == True:
            pp_results(results)
        return results

    def search_by_description(self, query, max_results=10, print_results=True):
        """Search for a `data.gov.in` dataset resource in the descriptions of datasets.

        Args:
            query         : the query string to search for.               (str)
            max_results   : number of results to return. Defaults to 10.  (int)
            print_results : prints results when enabled.                  (bool)
        Returns:
            List of matching resources with `descriptions` and `Resource-ID`s.
        """
        results = search_json(
            self.assets.idx_desc_map, query, max_results, self.error_handle
        )
        if print_results == True:
            pp_results(results)
        return results

    def search_by_org_name(self, query, max_results=10, print_results=True):
        """Search for a `data.gov.in` dataset resource using the name of the organization.

        Args:
            query         : the query string to search for.               (str)
            max_results   : number of results to return. Defaults to 10.  (int)
            print_results : prints results when enabled.                  (bool)
        Returns:
            List of matching resources with `org-names` and `Resource-ID`s.
        """
        if query in self.org_names:
            result_indices = np.ravel(
                [
                    list(item.values())
                    for item in self.assets.org_idx_map
                    if list(item.keys())[0] == query
                ]
            )
            if self.error_handle == True:
                print(
                    "{} of {} results for `organization` - `{}`".format(
                        min(len(result_indices), max_results),
                        len(result_indices),
                        query,
                    )
                )
            else:
                pass
            results = [{r: self.idxtitlemap[r]} for r in result_indices][:max_results]
            if print_results == True:
                pp_results(results)
            return results
        else:
            try:
                close_match = difflib.get_close_matches(
                    query, self.org_names, n=1, cutoff=0.75
                )[0]
                if self.error_handle == True:
                    print(
                        "No organization named - `{}`. Did you mean - `{}`?".format(
                            query, close_match
                        )
                    )
                else:
                    pass
            except:
                print(
                    "No organization named - `{}`".format(query),
                    "Try using `.list_org_names()` to see a list of available organizations",
                    sep="\n",
                )
            return []

    def search_by_org_type(self, query, max_results=10, print_results=True):
        """Search for a `data.gov.in` dataset resource using an organization type.

        Args:
            query         : the query string to search for.               (str)
            max_results   : number of results to return. Defaults to 10.  (int)
            print_results : prints results when enabled.                  (bool)
        Returns:
            List of matching resources by `org-types` and `Resource-ID`s.
        """
        if query in self.org_types:
            result_indices = np.ravel(
                [
                    list(item.values())
                    for item in self.assets.orgtype_idx_map
                    if list(item.keys())[0] == query
                ]
            )
            if self.error_handle == True:
                print(
                    "{} of {} results for `organization type` - `{}`".format(
                        min(len(result_indices), max_results),
                        len(result_indices),
                        query,
                    )
                )
            else:
                pass
            results = [{r: self.idxtitlemap[r]} for r in result_indices][:max_results]
            if print_results == True:
                pp_results(results)
            return results
        else:
            try:
                close_match = difflib.get_close_matches(
                    query, self.org_types, n=1, cutoff=0.5
                )[0]
                if self.error_handle == True:
                    print(
                        "No `organization type` named - `{}`. Did you mean - `{}`?".format(
                            query, close_match
                        )
                    )
                else:
                    pass
            except:
                if self.error_handle == True:
                    print(
                        "No `organization type` named - `{}`".format(query),
                        "Try using `.list_org_types()` to see a list of available organization types",
                        sep="\n",
                    )
                else:
                    pass
            return []

    def search_by_sector(self, query, max_results=10, print_results=True):
        """Search for a `data.gov.in` dataset resource using the `sector` attribute.

        Args:
            query         : the query string to search for.               (str)
            max_results   : number of results to return. Defaults to 10   (int)
            print_results : prints results when enabled.                  (bool)
        Returns:
            List of matching resources by `sector` and their `Resource-IDs`.

        """
        if query in self.sectors:
            result_indices = self.assets.sector_idx_map[query]
            if self.error_handle == True:
                print(
                    "{} of {} results for `sector` : `{}`".format(
                        min(len(result_indices), max_results),
                        len(result_indices),
                        query,
                    )
                )
            else:
                pass
            results = [{r: self.idxtitlemap[r]} for r in result_indices][:max_results]
            if print_results == True:
                pp_results(results)
            return results
        else:
            try:
                close_match = difflib.get_close_matches(
                    query, self.sectors, n=1, cutoff=0.7
                )[0]
                if self.error_handle == True:
                    print(
                        "No `sector` : `{}`. Did you mean : `{}`?".format(
                            query, close_match
                        )
                    )
                else:
                    pass
            except:
                if self.error_handle == True:
                    print(
                        "No `sector` : `{}`".format(query),
                        "Try using `.list_sectors()` to see a list of available sectors",
                        sep="\n",
                    )
                else:
                    pass
            return []

    def search_by_source(self, query, max_results=10, print_results=True):
        """Search for a `data.gov.in` dataset resource using the `source` attribute.
        Args:
            query         : the query string to search for.               (str)
            max_results   : number of results to return. Defaults to 10.  (int)
            print_results : prints results when enabled.                  (bool)
        Returns:
            List of matching resources by `source` and their `Resource-IDs`.

        """
        if query in self.sources:
            result_indices = self.assets.source_idx_map[query]
            if self.error_handle == True:
                print(
                    "{} of {} results for `source` : `{}`".format(
                        min(len(result_indices), max_results),
                        len(result_indices),
                        query,
                    )
                )
            else:
                pass
            results = [{r: self.idxtitlemap[r]} for r in result_indices][:max_results]
            if print_results == True:
                pp_results(results)
            return results
        else:
            try:
                close_match = difflib.get_close_matches(
                    query, self.sources, n=1, cutoff=0.75
                )[0]
                if self.error_handle == True:
                    print(
                        "No `source` : `{}`. Did you mean : `{}`?".format(
                            query, close_match
                        )
                    )
                else:
                    pass
            except:
                if self.error_handle == True:
                    print(
                        "No `source` : `{}`".format(query),
                        "Try using `.list_sources()` to see a list of available sources",
                        sep="\n",
                    )
                else:
                    pass

    def search(
        self,
        title=None,
        description=None,
        org_name=None,
        org_type=None,
        sector=None,
        source=None,
        max_results=10,
        print_results=True,
    ):
        """Search for resource using multiple filters.

        Args:
            title         : title query string. (str)
            description   : description query string. (str)
            org_type      : organization-type query string. (str)
            org_name      : organization-name query string. (str)
            sector        : sector query string. (str)
            source        : source query string. (str)


            max_results   : number of results to return. Defaults to 10.    (int)
            print_results : prints results if enabled. (bool)

        """
        print("Searching  ...                         \r", end="")
        self.error_handle = False

        if pd.isnull(org_type) == False:
            org_type_matches = extract_keys(
                self.search_by_org_type(
                    org_type, max_results=10 ** 10, print_results=False
                )
            )
        else:
            org_type_matches = self.assets.resource_ids

        if pd.isnull(org_name) == False:
            org_name_matches = extract_keys(
                self.search_by_org_name(
                    org_name, max_results=10 ** 10, print_results=False
                )
            )
        else:
            org_name_matches = self.assets.resource_ids

        if pd.isnull(sector) == False:
            sector_matches = extract_keys(
                self.search_by_sector(sector, max_results=10 ** 10, print_results=False)
            )
        else:
            sector_matches = self.assets.resource_ids

        if pd.isnull(source) == False:
            source_matches = extract_keys(
                self.search_by_source(source, max_results=10 ** 10, print_results=False)
            )
        else:
            source_matches = self.assets.resource_ids

        if pd.isnull(title) == False:
            title_matches = extract_keys(
                self.search_by_title(title, max_results=10 ** 10, print_results=False)
            )
        else:
            title_matches = self.assets.resource_ids

        if pd.isnull(description) == False:
            description_matches = extract_keys(
                self.search_by_description(
                    description, max_results=10 ** 10, print_results=False
                )
            )
        else:
            description_matches = self.assets.resource_ids
        match_list_1 = [
            org_type_matches,
            org_name_matches,
            sector_matches,
            source_matches,
            title_matches,
            description_matches,
        ]
        match_list_2 = [
            m if len(m) > 0 else self.assets.resource_ids for m in match_list_1
        ]
        matches = intersect(match_list_2)
        M = len(matches)
        self.error_handle = True

        if M > 0:
            print("{} of {} results".format(min(M, max_results), M))
            results = [{match: self.idxtitlemap[match]} for match in matches][
                :max_results
            ]
            if print_results == True:
                pp_results(results)
            return results
        elif M == 0:
            print("Found 0 results. Try searching with fewer parameters.")

    def get_resource_info(self, rsrc_id):
        """Get all available meta-data for a `data.gov.in` data resource
        Meta-Data includes -
            - Resource-ID
            - Title
            - Description
            - Total records available
            - Date-Created
            - Data-Updated
            - Organization-Type
            - Organization-Name
            - Source
            - Sector
            - Fields
        """
        rsrc_id = wipe_resource_id(rsrc_id)
        results = self.assets.compile_all_information(rsrc_id, self.api_key)

        return results

    def get_resource_fields(self, rsrc_id):
        """Get details of fields (variables) available for a `data.gov.in` data resource."""
        try:
            rsrc_id = wipe_resource_id(rsrc_id)
            if rsrc_id in self.assets.resource_ids:
                fieldcodes = self.idxfieldmap[rsrc_id]
                fieldlabels = [self.assets.field_label_map[f] for f in fieldcodes]
                fielddtypes = [self.assets.field_dtype_map[f] for f in fieldcodes]
                fieldinfo = [
                    {
                        "field_code": fieldcodes[f],
                        "field_label": fieldlabels[f],
                        "field_type": fielddtypes[f],
                    }
                    for f in range(len(fieldcodes))
                ]
                return pd.DataFrame(fieldinfo)
            else:
                print("{} is not a valid Resource-ID".format(rsrc_id))
        except AssertionError:
            print("{} is not a valid Resource-ID".format(rsrc_id))

    def get_last_resource(self):
        """Returns the last collected data."""
        try:
            return self.resource.data
        except:
            return None

    def get_data(
        self,
        resource_id,
        start_from=0,
        num_results="all",
        filters=[],
        fields=[],
        sort_key="",
        sort_order="asc",
    ):
        """Returns requested data in a dataframe format.

        Args:
            resource_id : Resource-ID selected using search functionality (str)
            start_from  : Start Index. Defaults to 0.                    (int)
            num_results : Total number of results desired. Defaults to 'all'. (int)
            filters     : Filters for request               (List of dicts/ dict)
            fields      : List of fields (variables) to return
            sort_key    : Sort dataframe using an available field (variable)
            sort_order  : Ascending- 'asc' , Descending - 'desc'

        """
        self.resource = Resource(self)
        self.resource.set_resource_id(resource_id)
        if isinstance(filters, dict) or isinstance(filters, list):
            if isinstance(filters, dict):
                self.resource.set_filters([filters])
            elif isinstance(filters, list):
                self.resource.set_filters(filters)
        else:
            self.resource.set_filters([])

        self.resource.set_fields(fields)
        self.resource.set_sort_key(sort_key, sort_order)
        n = np.inf
        if isinstance(num_results, int) == True:
            if n > 0:
                n = num_results
        self.resource.set_req_method(num=n)
        self.resource.make_urls()
        data = self.resource.get_data()
        if self.is_sample_key == True:
            print(
                "*Warning*\nYou are using a sample API-key. Some observations may be missing."
            )
        else:
            pass
        return data
