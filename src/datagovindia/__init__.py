"""Python API-wrapper for Government of India’s [Open Government Data OGD platform](https://data.gov.in/)
`datagovindia` is an API wrapper for APIs available at Government of India’s [Open Government Data OGD platform](https://data.gov.in/ogpl_apis)"""

import os
import re
import sys
import time
import requests
import sqlite3
import pandas as pd
import multiprocessing as mp
from typing import List, Dict
from urllib.parse import urlencode
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
from dateutil.parser import parse as dateutil_parse
from collections.abc import Iterable
from urllib.parse import urlencode
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

__version__ = "0.1.0"

def flatten(lst):
    """Flatten a nested list"""
    for item in lst:
        if isinstance(item, Iterable) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item
def construct_url(params: dict) -> str:
    """
    Construct URL with query parameters.
    """
    base_url = "https://api.data.gov.in/lists"
    query_string = urlencode(params)
    return f"{base_url}?{query_string}"

def remove_special_chars(s: str) -> str:
    """
    Remove special characters from string.
    """
    return re.sub("[^a-zA-Z0-9\.]", "", s).strip().lower() # type: ignore

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

def get_total_available_resources() -> int:
    """
    Retrieve total number of available records.
    """
    params = {
        "format": "json",
        "notfilters[source]": "visualize.data.gov.in",
        "filters[active]": 1,
        "offset": 0,
        "limit": 0,
    }
    api_url = construct_url(params)
    api_response = requests.get(api_url, timeout=(5, 10))
    return api_response.json()["total"]

def _fetch_metadata(api_key: str, start: int = 0, end: int = 1000) -> list:
    """
    Retrieve records using single thread.
    """
    params = {
        "api-key": api_key,
        "notfilters[source]": "visualize.data.gov.in",
        "filters[active]": 1,
        "sort[updated]": "desc",
        "format": "json",
        "offset": start,
        "limit": end - start,
    }
    api_url = construct_url(params)

    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        resp = session.get(api_url, timeout=(30, 60))
        resp.raise_for_status()
        logger.info(f"Successfully fetched data for range ({start}-{end}")
        return [compile_record_info(record) for record in resp.json().get("records", [])]
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for range ({start}-{end}): {e}")
        return []
    
def fetch_metadata_records(
    api_key: str, start: int = 0, end: int = 1000000, batch_size: int = 100, njobs: int = None
) -> list:
    """Retrieve records using multiple threads."""
    with mp.Pool(njobs) as pool:
        data = pool.starmap(
            _fetch_metadata, [(api_key, i, min(end, i + batch_size)) for i in range(start, end, batch_size)]
        )
    # Filter out None results
    data = [item for sublist in data if sublist is not None for item in sublist]
    return data

def get_api_info(url) -> dict:
    """Get json data from url"""
    response = requests.get(url, timeout=(5, 10)).json()
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
        response[key] = True if response[key] == "1" else False
    response = {k: v for k, v in response.items() if k not in skip_keys}
    return response

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

def get_api_records(url:str, **kwargs) -> list:
    """Get json data from url"""
    response = requests.get(url, **kwargs)
    response.raise_for_status()
    data = response.json()
    if "records" not in data:
        return []
    else:
        return data["records"]

def get_data_njobs(url_list: list, njobs=None) -> list:
    """Get record data from url_list using njobs"""
    if njobs is None:
        njobs = mp.cpu_count()
    with mp.Pool(njobs) as pool:
        data = pool.map(get_api_records, url_list)
    # Flatten list of lists
    data = [item for sublist in data for item in sublist]
    return data

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

    Parameters
    ----------

    api_key: (str) (required)
        API key for data.gov.in

    resource_id: (str) (required)
        Unique identifier of the resource.

    offset: (int) (optional)
        Offset of the records to be fetched. Defaults to 0.

    limit: (int) (optional)
        Number of records to be fetched. Defaults to 1000.

    filters: (dict) (optional)
        Filters to be applied on the records, should be a list of dicts of the form {<field>:<value>}.
        Defaults to {}.

    fields: (list) (optional)
        Fields to be fetched. Defaults to [].

    sort_by: (str) (optional)
        Field to sort results by. Defaults to None.

    sort_order: (str) (optional)
        Order of sorting. Defaults to "asc". Only applicable if sort_by is not None.

    Returns
    -------

    url: str
        Url to fetch data from data.gov.in
    """
    params = {"api-key": api_key, "format": "json", "offset": offset, "limit": limit}
    if fields:
        params["fields"] = ",".join(fields)
    if sort_by:
        params[f"sort[{sort_by}]"] = sort_order or "asc"
    if filters:
        params.update({f"filters[{k}]": v for k, v in filters.items()})
    url = f"https://api.data.gov.in/resource/{resource_id}" + "?" + urlencode(params, doseq=True, safe="\],\[")
    return url

class DataGovIndia:
    """Python API-wrapper for Government of India’s [Open Government Data OGD platform](https://data.gov.in/)"""
    def __init__(self, api_key:str=None, db_path:str=None) -> None:
        """
        Initialize DataGovIndia object

        Parameters
        ----------

        api_key: str (optional)
            API key for data.gov.in. If not provided, it will be read from the environment variable DATAGOVINDIA_API_KEY
            If not found, it will raise an error.

        db_path: str (optional)
            Required only for searching the database.
            Path to the database file. If not provided, it will be read from the environment variable DATAGOVINDIA_DB_PATH
            If not found, it will be set to ~/datagovindia.db
        """
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.environ.get("DATAGOVINDIA_API_KEY")

        if db_path:
            self.db_path = db_path
        else:
            self.db_path = os.environ.get(
                "DATAGOVINDIA_DB_PATH", os.path.join(os.path.expanduser("~"), "datagovindia.db")
            )
        self.connect(verify=False)
        

    def validate_api_key(self):
        if not self.api_key:
            raise ValueError("API key not found. Please set it as an environment variable `DATAGOVINDIA_API_KEY` or pass it as an argument while initializing the DataGovIndia object.")

    def connect(self, verify:bool=False):
        """Connect to datagovindia.db sqlite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.create_function("regexmatch", 2, regexmatch)
        self.cursor = self.conn.cursor()
            # check whether the table exists
        if verify:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='resources'")
            if (self.cursor.fetchone() is None):
                raise ValueError(f"""
                    Could not find tables in {self.db_path}.
                    If this is the first time you are using this package, please run the following commands:
                        >>> from datagovindia import DataGovIndia                    
                        >>> data_gov = DataGovIndia()
                        >>> data_gov.update_metadata()
                        """
                )
    def close(self):
        """Close connection to datagovindia.db sqlite database"""
        self.conn.close()

    def search(self, query:str, search_fields: list=["title"], sort_by:str=None, ascending:bool=True) -> pd.DataFrame:
        """Search for a query in the database.

        Parameters
        ----------

        query: str (required)
            Search query to be searched in the database.

        search_fields: list (optional)
            List of fields to search in. Defaults to ['title'].
            Valid fields are: ['title', 'description', 'org_type', 'fields', 'orgs', 'source', 'sectors', 'date_created', 'date_updated']

        sort_by: str (optional)
            Field to sort results by. Defaults to None.
            Valid fields are: ['title', 'description', 'org_type', 'fields', 'orgs', 'source', 'sectors', 'date_created', 'date_updated']

        ascending: bool (optional)
            Sort results in ascending order. Defaults to True.
            Set to False to sort in descending order. Only applicable if sort_by is not None.

        Returns
        -------
        df: pd.DataFrame
            Dataframe of search results.

        Examples
        --------
        >>> from datagovindia import DataGovIndia
        >>> datagovin = DataGovIndia()

        ### Simple search
        >>> datagovin.search("covid") 

        ### Search in specific fields
        >>> datagovin.search("pollution", search_fields=['title', 'description'])
        
        ### Search and sort results by date_created in descending order
        >>> datagovin.search("MGNREGA", search_fields=['title', 'description'], sort_by='date_created', ascending=False)        
        """
        self.connect(verify=True)
        sql_query = self.gen_sql_query(query, search_fields, sort_by, ascending)
        self.cursor.execute(sql_query)
        keys = list(map(lambda x: x[0], self.cursor.description))
        values = self.cursor.fetchall()
        records = list(map(lambda x: dict(zip(keys, x)), values))
        data = pd.DataFrame(records)
        if len(data) > 0:
            for col in ["fields", "orgs", "sectors"]:
                data[col] = data[col].str.split(" | ", regex=False)
        self.close()
        return data

    def gen_sql_query(self, query : str, search_fields:list=["title"], sort_by:str=None, ascending:bool=True) -> str:
        """Construct sql query for searching the database"""
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
                # Raise error and print statement
                raise ValueError(
                    f"Invalid search field {field}, valid fields are {searchable_attributes}"
                )
            sql_query += f"regexmatch({field}, '{query}') OR "
        sql_query = sql_query[:-4]  # Remove the last " OR "
        if sort_by:
            assert sort_by in searchable_attributes, f"Invalid sort_by field {sort_by}, valid fields are {searchable_attributes}"
            sql_query += f" ORDER BY {sort_by} {'ASC' if ascending else 'DESC'}"
        return sql_query

    def get_resource_info(self, resource_id: str) -> dict:
        """Fetches information about a resource.

        Parameters
        ----------
        resource_id: (str) (required)
            Unique identifier of the resource.

        Returns
        -------
        info: dict
            Dictionary containing information about the resource.
        """
        self.validate_api_key()
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

        Parameters
        ----------

        resource_id: (str) (required)
            Unique identifier of the resource.

        sort_by: (str) (optional)
            Field to sort results by. Defaults to None.

        ascending: (bool) (optional)
            Whether to sort results in ascending order. Defaults to True.
            Only applicable if sort_by is not None.

        offset: (int) (optional)
            Offset of the records to be fetched. Defaults to 0.

        batch_size: (int) (optional)
            Number of records to be fetched in a single request. Defaults to 2000.
            Increasing batch_size will increase the speed of data collection but will also increase the memory usage.
            reduce batch_size if you are facing memory issues or timeout errors.

        limit: (int) (optional)
            Number of records to be fetched. Defaults to None.
            If None, it will be set to the total number of records available in the resource.

        filters: (dict) (optional)
            Filters to be applied on the records, should be a dict of the form {<field>:<value>}.

        fields: (list) (optional)
            Fields to be fetched. Defaults to []. Use `.get_resource_info` to get a list of all available fields for a resource.

        njobs: (int) (optional)
            Number of threads to use for collecting data. Defaults to None.
            None will use all available threads.

        Returns
        -------

        df: pd.DataFrame
            Dataframe with requested data.
        """
        self.validate_api_key()
        
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

    def get_update_info(self):
        """Fetches information about the last update of the database.

        Returns
        -------
        info: dict
            Dictionary containing information about the metadata in the database.
        """
        self.connect(verify=True)

        self.cursor.execute("""
            SELECT last_updated, number_of_resources FROM metadata
        """)
        info_ = dict(zip(["last_updated", "number_of_resources"], self.cursor.fetchone()))
        self.close()
        return info_

    def create_tables(self):
        """Create tables in database if they don't exist. 
        Tables: resources, metadata
        """
        
        self.connect()        
        self.cursor.execute("""
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
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata(
                id INTEGER PRIMARY KEY,
                last_updated TEXT,
                number_of_resources INTEGER
            )
        """)
        self.conn.commit()
        self.close()

    def _save_update_info(self , _num_updated:int):
        """Save info about last update to database"""
        self.connect()
        self.cursor.execute("""
            DELETE FROM metadata
        """)
        sql = """
            INSERT INTO metadata 
            (last_updated, number_of_resources) 
            VALUES (?, ?)
        """
        last_refreshed = current_datetime()
        self.cursor.execute(sql, (last_refreshed, _num_updated))
        self.conn.commit()
        self.close()

    def upsert_records(self, table_name, data_dicts):
        """Insert or replace records in database"""
        self.connect(verify=True)
        placeholders = ", ".join(["?"] * len(data_dicts[0]))
        columns = ", ".join(data_dicts[0].keys())
        sql = f"""INSERT OR REPLACE INTO {table_name} 
                ({columns}) 
                VALUES ({placeholders})"""
        
        # Convert all values to supported types and log them
        def convert_value(value):
            if isinstance(value, (str, int, float, type(None))):
                return value
            return str(value)  # Convert unsupported types to strings
        
        data_values = []
        for data_dict in data_dicts:
            converted_values = tuple(convert_value(v) for v in data_dict.values())
            logger.debug(f"Inserting values: {converted_values}")
            data_values.append(converted_values)
        
        self.cursor.executemany(sql, data_values)
        self.conn.commit()
        self.close()
        

    def sync_metadata(self, batch_size=1000, njobs=None): # Reducing batch_size to 1000 to avoid timeout errors
        """Updates metadata in datagovindia.db sqlite database

        Parameters
        ----------

        batch_size: int (optional)
            Number of records to be fetched in a single request. Defaults to 2500.

        njobs: int (optional)
            Number of threads to use for collecting data. Defaults to None.
            None will use all available threads.
        """
        self.validate_api_key()

        start_time = time.time()

        _num_available = get_total_available_resources()
        _num_updated = 0

        self.create_tables()
        njobs  = mp.cpu_count() if njobs is None else njobs
        _batch = njobs * batch_size

        display_progress_bar(_num_updated, _num_available)

        for start in range(0, _num_available, _batch):
            end     = min(_num_available, start + _batch)
            records = fetch_metadata_records(
                self.api_key, start=start, end=end, batch_size=batch_size, njobs=njobs
            )
            self.upsert_records("resources", records)
            _num_updated += len(records)

            # Calculate ETA
            elapsed_time   = time.time() - start_time
            avg_time       = elapsed_time / _num_updated
            _num_remaining = (_num_available - _num_updated) 
            eta = avg_time * _num_remaining
            display_progress_bar(_num_updated, _num_available, eta=format_seconds(eta))

        total_time = time.time() - start_time
        logger.info(f"\nTotal time taken: {format_seconds(total_time)} to update {_num_updated} resources.")
        self._save_update_info(_num_updated)