"""Python API-wrapper for Government of India’s [Open Government Data OGD platform](https://data.gov.in/)
`datagovindia` is an API wrapper for APIs available at Government of India’s [Open Government Data OGD platform](https://data.gov.in/ogpl_apis)"""

import os
import re
import sys
import time
import requests
import signal
import sqlite3
import pandas as pd
import multiprocessing as mp
from typing import List, Dict
from urllib.parse import urlencode
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryError
from dateutil.parser import parse as dateutil_parse
from collections.abc import Iterable
from urllib.parse import urlencode
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

__version__ = "1.0.2"

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=5, max=60),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
)
def make_request_with_retry(url: str, **kwargs) -> requests.Response:
    response = requests.get(url, timeout=(kwargs.get("timeout", 10), kwargs.get("timeout", 30)))
    response.raise_for_status()
    return response

def flatten(lst):
    """Flatten a nested list"""
    for item in lst:
        if isinstance(item, Iterable) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item

def construct_url_for_lists(params: dict) -> str:
    """
    Construct URL with query parameters.
    """
    base_url = "https://api.data.gov.in/lists"
    query_string = urlencode(params)
    return f"{base_url}?{query_string}"

def get_total_available_resources() -> int:
    """Retrieve total number of available records."""
    params = {
        "format": "json",
        "notfilters[source]": "visualize.data.gov.in",
        "filters[active]": 1,
        "offset": 0,
        "limit": 0,
    }
    api_url = construct_url_for_lists(params)
    api_response = make_request_with_retry(api_url)
    return api_response.json()["total"]
    
def _fetch_metadata(api_key: str, start: int = 0, end: int = 1000) -> list:
    """Retrieve records using single thread."""
    params = {
        "api-key": api_key,
        "notfilters[source]": "visualize.data.gov.in",
        "filters[active]": 1,
        "sort[updated]": "desc",
        "format": "json",
        "offset": start,
        "limit": end - start,
    }
    api_url = construct_url_for_lists(params)

    try:
        resp = make_request_with_retry(api_url)
        resp.raise_for_status()
        # logger.info(f"Successfully fetched data for range ({start}-{end}")
        return [compile_record_info(record) for record in resp.json().get("records", [])]
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for range ({start}-{end}): {e}")
        raise




def build_url(
    api_key: str,
    resource_id: str,
    offset: int = 0,
    limit: int = 1000,
    filters: Dict[str, str] = None,
    fields: List[str] = None,
    sort_by: str = None,
    sort_order: str = "asc",
) -> str:
    """Build url to fetch data from data.gov.in

        api_key: (str) - API key for data.gov.in
        resource_id: (str) - Unique identifier of the resource.
        offset: (int) - Offset of the records to be fetched. Defaults to 0.
        limit: (int) - Number of records to be fetched. Defaults to 1000.
        filters: (dict) - Filters to be applied on the records, should be a list of dicts of the form {<field>:<value>}. Defaults to {}.
        fields: (list) - Fields to be fetched. Defaults to [].
        sort_by: (str) - Field to sort results by. Defaults to None.
        sort_order: (str) - Order of sorting. Defaults to "asc". Only applicable if sort_by is not None.

    Returns: (str) - Url to fetch data from data.gov.in
    """
    base_url = f"https://api.data.gov.in/resource/{resource_id}"
    params = {"api-key": api_key, "format": "json", "offset": offset, "limit": limit}
    if fields:
        params["fields"] = ",".join(fields)
    if sort_by:
        params[f"sort[{sort_by}]"] = sort_order or "asc"
    if filters:
        params.update({f"filters[{k}]": v for k, v in filters.items()})
    url = base_url + "?" + urlencode(params, doseq=True, safe="\],\[")
    return url

def check_api_key(api_key: str) -> bool:
    """Check if API key is valid by making a request to the API for 1 record."""
    params = {
        "api-key": api_key,
        "format": "json",
        "offset": 0,
        "limit": 1,
    }
    api_url = construct_url_for_lists(params)
    resp    = requests.get(api_url)
    # Get 1 record to check if the API key is valid
    resource_id = resp.json().get("records", [{}])[0].get("index_name")
    if resource_id:
        url = build_url(api_key=api_key,resource_id=resource_id, limit=1)
        try:
            response = requests.get(url)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False
    else:
        return False



def remove_special_chars(s: str) -> str:
    """
    Remove special characters from string.
    """
    return re.sub("[^a-zA-Z0-9\.]", "", s).strip().lower()  # type: ignore

def regexmatch(text: str, query: str) -> bool:
    """Search for 'query' within 'text' using regex"""
    if text and query:  # Check only non-null
        text, query = remove_special_chars(text), remove_special_chars(query)
        if re.search(query, text, flags=re.I):
            return True
        else:
            return False
    else:
        return False

def format_date(date_string: str):
    """Parse date string with given format and return ISO 8601 formatted date string"""
    try:
        return dateutil_parse(date_string).isoformat(timespec="seconds")
    except (ValueError, TypeError):
        return None

def current_datetime() -> str:
    """Get the current datetime as a string in ISO 8601 format."""
    return datetime.now().isoformat(timespec="seconds")

def is_nested(lst: list) -> bool:
    """Check if list is nested"""
    return any(isinstance(i, list) for i in lst)

def format_seconds(seconds: int, padding: int = 8) -> str:
    """Format seconds into a readable format"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if hours:
        parts.append(f"{int(hours)}h{'' if hours > 1 else ''}")
    if minutes:
        parts.append(f"{int(minutes)}m{'' if minutes > 1 else ''}")
    if seconds or not parts:
        parts.append(f"{int(seconds)}s{'' if seconds > 1 else ''}")
    eta_string = ":".join(parts)
    return eta_string.ljust(padding)

def display_progress_bar(iteration, total, bar_length=50, char="=", fill_char=".", eta=None):
    """
    Display a progress bar in the console.

    Parameters:
    ------------
        iteration (int): Current iteration.
        total (int): Total number of iterations.
        bar_length (int): Length of the progress bar.
        char (str): Character for completed progress.
        fill_char (str): Character for remaining progress.
        eta (str or None): Estimated time of arrival.
    """
    progress = iteration / total
    arrow = char * int(round(progress * bar_length) - 1) + ">"
    spaces = fill_char * (bar_length - len(arrow))

    if eta:
        sys.stdout.write(f"\rUpdated {iteration}/{total} resources: [{arrow + spaces}] - ETA: {eta}")
    else:
        sys.stdout.write(f"\rUpdated {iteration}/{total} resources: [{arrow + spaces}]")
    sys.stdout.flush()

def compile_record_info(record: dict) -> dict:
    """Compile record info into a dictionary"""
    return {
        "resource_id": record.get("index_name"),
        "title": record.get("title"),
        "description": record.get("desc"),
        "org_type": record.get("org_type"),
        "fields": " | ".join(str(f.get("id", "")) for f in record.get("field", [])),
        "orgs": " | ".join(str(item) for item in flatten(record.get("org", []))),
        "source": record.get("source"),
        "sectors": " | ".join(str(item) for item in record.get("sector", [])),
        "date_created": format_date(record.get("created_date")),
        "date_updated": format_date(record.get("updated_date")),
    }


def init_worker():
    """Ignore SIGINT in worker processes to let the parent handle it."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def fetch_metadata_records(
    api_key: str, start: int = 0, end: int = 1000000, batch_size: int = 100, njobs: int = None
) -> list:
    """Retrieve records using multiple threads with graceful handling of KeyboardInterrupt."""
    njobs = max(1, mp.cpu_count() if njobs is None else njobs)
    pool = mp.Pool(njobs, initializer=init_worker)  # Initialize worker with SIGINT ignored

    try:
        data = pool.starmap(
            _fetch_metadata, [(api_key, i, min(end, i + batch_size)) for i in range(start, end, batch_size)]
        )
    except KeyboardInterrupt:
        # If interrupted, terminate the pool and wait for processes to finish
        logger.info("KeyboardInterrupt: Terminating workers...")
        pool.terminate()  # Terminate all running workers
        pool.join()  # Wait for workers to terminate
        logger.info("All workers terminated.")
        sys.exit(1)
    else:
        # Close the pool normally if no interruption occurs
        pool.close()
        pool.join()

    # Flatten the data after processing
    data = [item for sublist in data if sublist is not None for item in sublist]
    return data


def get_api_info(url) -> dict:
    """Get json data from url"""
    try:
        response = make_request_with_retry(url)
        response.raise_for_status()
    except RetryError as e:
        logger.error(f"Failed to fetch data: {e}")
        return {}
    data = response.json()

    skip_keys = [
        "message",
        "version",
        "status",
        "offset",
        "limit",
        "count",
        "records",
        "external_ws",
        "external_ws_url",
        "target_bucket",
    ]
    boolean_keys = ["visualizable", "active"]

    for key in boolean_keys:
        if key in data:
            try:
                data[key] = bool(int(data[key]))
            except (ValueError, TypeError):
                data[key] = data[key]
    data = {k: v for k, v in data.items() if k not in skip_keys}
    return data

def save_dataframe(df, filepath):
    """Save dataframe to filepath"""
    def get_file_extension(filepath) -> str:
        """Get file extension from filepath"""
        return os.path.splitext(filepath)[-1]
    file_extension = get_file_extension(filepath)
    if file_extension == ".csv":
        df.to_csv(filepath, index=False)
    elif file_extension == ".json":
        df.to_json(filepath, orient="records")
    elif file_extension == ".xlsx":
        df.to_excel(filepath, index=False)
    else:
        raise ValueError(f"Invalid file extension: {file_extension}")

def get_api_records(url: str, **kwargs) -> list:
    """Get json data from url"""
    response = make_request_with_retry(url, **kwargs)
    response.raise_for_status()
    data = response.json()
    if "records" not in data:
        return []
    else:
        return data["records"]

def get_data_njobs(url_list: list, njobs=None) -> list:
    """Get record data from url_list using njobs with graceful handling of KeyboardInterrupt."""
    if njobs is None:
        njobs = mp.cpu_count()
    
    pool = mp.Pool(njobs, initializer=init_worker)  # Initialize worker with SIGINT ignored
    
    try:
        data = pool.map(get_api_records, url_list)
    except KeyboardInterrupt:
        # If interrupted, log the event and terminate the pool
        logger.warning("Received KeyboardInterrupt, terminating workers...")
        pool.terminate()  # Terminate all running workers
        pool.join()  # Wait for workers to terminate
        logger.info("All workers terminated.")
        sys.exit(1)
    else:
        # Close the pool normally if no interruption occurs
        pool.close()
        pool.join()

    # Flatten the data after processing
    data = [item for sublist in data for item in sublist]
    return data

class DataGovIndia:
    """Python API-wrapper for Government of India’s [Open Government Data OGD platform](https://data.gov.in/)"""

    def __init__(self, api_key: str = None, db_path: str = None, validate_key: bool = False):
        """Initialize DataGovIndia object

        api_key: str
            API key for data.gov.in. If not provided, it will be read from the environment variable DATAGOVINDIA_API_KEY
            If not found, it will raise an error.

        db_path: str
            Required only for searching the database.
            Path to the database file. If not provided, it will be read from the environment variable DATAGOVINDIA_DB_PATH
            If not found, it will be set to ~/datagovindia.db
        
        """
        self.api_key = api_key or os.environ.get("DATAGOVINDIA_API_KEY")
        self.db_path = db_path or os.environ.get(
            "DATAGOVINDIA_DB_PATH", os.path.join(os.path.expanduser("~"), "datagovindia.db")
        )
        if validate_key:            
            self.validate_api_key()

    def validate_api_key(self):
        if not self.api_key:
            # Raise error if API key is not found
            raise ValueError(
                "API key not found. Please set it as an environment variable `DATAGOVINDIA_API_KEY` or pass it as an argument while initializing the DataGovIndia object."
            )        
        if not check_api_key(self.api_key):
            raise ValueError("Invalid API key. Please check if the API key is valid.")
        

    def connect(self, verify: bool = False):
        """Connect to datagovindia.db sqlite database using a context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.create_function("regexmatch", 2, regexmatch)
        if verify:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='resources'")
                if cursor.fetchone() is None:
                    raise ValueError(
                        f"""
                        Could not find tables in {self.db_path}.
                        If this is the first time you are using this package, please run the following commands:
                            >>> from datagovindia import DataGovIndia
                            >>> data_gov = DataGovIndia()
                            >>> data_gov.update_metadata()
                        """
                    )
        return conn

    def search(
        self, query: str, search_fields: list = ["title"], sort_by: str = None, ascending: bool = True
    ) -> pd.DataFrame:
        """Search for a query in the database."""
        with self.connect(verify=True) as conn:
            cursor = conn.cursor()
            sql_query = self.gen_sql_query(query, search_fields, sort_by, ascending)
            cursor.execute(sql_query)
            keys = [desc[0] for desc in cursor.description]
            values = cursor.fetchall()
            records = [dict(zip(keys, row)) for row in values]
            data = pd.DataFrame(records)
            if len(data) > 0:
                for col in ["fields", "orgs", "sectors"]:
                    data[col] = data[col].str.split(" | ", regex=False)
        return data

    def gen_sql_query(
        self, query: str, search_fields: list = ["title"], sort_by: str = None, ascending: bool = True
    ) -> str:
        """Construct SQL query for searching the database"""
        searchable_attributes = [
            "title",
            "description",
            "org_type",
            "fields",
            "orgs",
            "source",
            "sectors",
            "date_created",
            "date_updated",
        ]
        sql_query = "SELECT * FROM resources WHERE "
        for field in search_fields:
            if field not in searchable_attributes:
                raise ValueError(f"Invalid search field {field}, valid fields are {searchable_attributes}")
            sql_query += f"regexmatch({field}, '{query}') OR "
        sql_query = sql_query[:-4]  # Remove the last " OR "
        if sort_by:
            assert (
                sort_by in searchable_attributes
            ), f"Invalid sort_by field {sort_by}, valid fields are {searchable_attributes}"
            sql_query += f" ORDER BY {sort_by} {'ASC' if ascending else 'DESC'}"
        return sql_query

    def get_resource_info(self, resource_id: str) -> dict:
        """Fetches information about a resource."""
        url = build_url(
            api_key=self.api_key,
            resource_id=resource_id,
            filters={},
            fields=[],
            sort_by="",
            sort_order="asc",
            offset=0,
            limit=0,
        )
        api_info = get_api_info(url)
        return api_info

    def get_update_info(self) -> dict:
        """Fetches information about the last update of the database."""
        with self.connect(verify=True) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT last_updated, number_of_resources FROM metadata")
            info_ = dict(zip(["last_updated", "number_of_resources"], cursor.fetchone()))
        return info_

    def get_data(
        self,
        resource_id: str,
        sort_by: str = None,
        ascending: bool = True,
        offset: int = 0,
        batch_size: int = 2000,
        njobs: int = None,
        limit: int = None,
        filters: Dict[str, str] = None,
        fields: List = None,
    ) -> pd.DataFrame:
        """Returns requested data as a pandas dataframe.
            resource_id: (str) (required) - Unique identifier of the resource.

            sort_by: (str) - Field to sort results by. Defaults to None.

            ascending: (bool) - Whether to sort results in ascending order. Defaults to True. Only applicable if sort_by is not None.

            offset: (int) - Offset of the records to be fetched. Defaults to 0.

            batch_size: (int) - Number of records to be fetched in a single request. Defaults to 2000.
            Increasing batch_size will increase the speed of data collection but will also increase the memory usage. Reduce `batch_size` if you are facing memory issues or timeout errors.

            limit: (int) - Number of records to be fetched. Defaults to None. If None, it will be set to the total number of records available in the resource.

            filters: (dict) - Filters to be applied on the records, should be a dict of the form {<field>:<value>}.

            fields: (list) - Fields to be fetched. Defaults to []. Use `.get_resource_info` to get a list of all available fields for a resource.

            njobs: (int) - Number of threads to use for collecting data. Defaults to None. None will use the number of CPUs available on the system.

        
        Returns: pd.Dataframe        
        """
        
        if limit is None:
            limit = self.get_resource_info(resource_id)["total"]
        params_ = {
            "resource_id": resource_id,
            "sort_by": sort_by,
            "sort_order": "asc" if ascending else "desc",
            "filters": filters,
            "fields": fields,
        }
        param_list = [
            {**params_, **{"offset": i, "limit": min(batch_size, limit - i)}}
            for i in range(offset, limit, batch_size)
        ]

        url_list = [build_url(api_key=self.api_key, **params) for params in param_list]
        data = get_data_njobs(url_list, njobs=njobs)
        return pd.DataFrame(data)
    
    def create_tables(self):
        """Create tables in database if they don't exist."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS resources(
                    resource_id TEXT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    org_type TEXT,
                    fields TEXT,
                    orgs TEXT,
                    source TEXT,
                    sectors TEXT,
                    date_created TEXT,
                    date_updated TEXT
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS metadata(
                    id INTEGER PRIMARY KEY,
                    last_updated TEXT,
                    number_of_resources INTEGER
                )
            """
            )
            conn.commit()

    def upsert_records(self, table_name: str, data_dicts: list):
        """Insert or replace records in the database."""
        with self.connect(verify=True) as conn:
            cursor = conn.cursor()
            placeholders = ", ".join(["?"] * len(data_dicts[0]))
            columns = ", ".join(data_dicts[0].keys())
            sql = f"""INSERT OR REPLACE INTO {table_name} 
                      ({columns}) 
                      VALUES ({placeholders})"""

            def convert_value(value):
                if isinstance(value, (str, int, float, type(None))):
                    return value
                return str(value)  # Convert unsupported types to strings
            data_values = [tuple(convert_value(v) for v in data_dict.values()) for data_dict in data_dicts]
            cursor.executemany(sql, data_values)
            conn.commit()

    def _save_update_info(self, _num_updated: int):
        """Save info about last update to the database."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM metadata")
            sql = """INSERT INTO metadata (last_updated, number_of_resources) VALUES (?, ?)"""
            last_refreshed = current_datetime()
            cursor.execute(sql, (last_refreshed, _num_updated))
            conn.commit()

    def sync_metadata(self, batch_size=1000, njobs=None):
        """Updates metadata in datagovindia.db sqlite database"""
        start_time = time.time()

        _num_available = get_total_available_resources()
        _num_updated = 0

        self.create_tables()
        njobs = mp.cpu_count() if njobs is None else njobs
        _batch = njobs * batch_size

        display_progress_bar(_num_updated, _num_available)

        for start in range(0, _num_available, _batch):
            end = min(_num_available, start + _batch)
            records = fetch_metadata_records(self.api_key, start=start, end=end, batch_size=batch_size, njobs=njobs)
            self.upsert_records("resources", records)
            _num_updated += len(records)

            # Calculate ETA

            elapsed_time = time.time() - start_time
            avg_time = elapsed_time / (_num_updated if _num_updated else 1)
            _num_remaining = _num_available - _num_updated
            eta = avg_time * _num_remaining
            display_progress_bar(_num_updated, _num_available, eta=format_seconds(eta))
        total_time = time.time() - start_time
        logger.info(f"\nTotal time taken: {format_seconds(total_time)} to update {_num_updated} resources.")
        self._save_update_info(_num_updated)
