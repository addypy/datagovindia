import json
import click
from datagovindia import DataGovIndia, save_dataframe

################## datagovindia cli ##################
@click.group()
def cli():
    """Command-line interface for the DataGovIndia API wrapper.

        `sync-metadata`: Fetches and syncs metadata from the OGD platform into an SQLite database.

        `get-update-info`: Fetches info for the last database update from the OGD platform.

        `search`: Searches the database based on a query and displays or saves the results.

        `get-resource-info`: Fetches info for a given resource ID from the OGD platform and displays it in the terminal.
        
        `get-data`: Fetches data for a given resource ID from the OGD platform and saves it to a specified file.

    """    

@cli.command(name="version")
def version():
    """Displays the version of the DataGovIndia API wrapper."""
    from datagovindia import __version__

    click.echo(f"datagovindia v{__version__}")

################## sync-metadata ##################
@cli.command(name="sync-metadata")
@click.option(
    "--api-key",
    default=None,
    type=str,
    help=(
        "API key to be used for fetching data. Optional if already set in environment variable"
        " 'DATAGOVINDIA_API_KEY'."
    ),
)
@click.option(
    "--db-path",
    default=None,
    type=str,
    help=(
        "Path to the SQLite database. Optional if already set in environment variable"
        " 'DATAGOVINDIA_DB_PATH'."
    ),
)
@click.option(
    "--batch-size",
    default=5000,
    type=int,
    help="Number of records to be fetched in a single request. Increase this value to improve performance.",
)
@click.option(
    "--njobs",
    default=None,
    type=int,
    help="Number of threads to use for collecting data. (default is all cores)",
)
def sync_metadata_cli(api_key, db_path, batch_size, njobs):
    """Fetches and syncs metadata from the OGD platform into the SQLite database.

    usage: `datagovindia sync-metadata [--api-key <API_KEY>] [--db-path <DB_PATH>] [--batch-size <BATCH_SIZE>] [--njobs <NJOBS>`]

    optional arguments:

        - `api-key`: `API key for the OGD platform. Uses 'DATAGOVINDIA_API_KEY' environment variable if not provided.`

        - `db-path`: `Path to the SQLite database. Defaults to 'DATAGOVINDIA_DB_PATH' environment variable or '~/datagovindia.db'.`

        - `batch-size`: `Number of records to fetch in one request. Increase for better performance but be wary of potential memory issues.`

        - `njobs`: `Number of parallel threads for fetching data. Defaults to using all available cores.`

    """
    click.echo("Syncing latest metadata from the OGD platform...")
    datagovin = DataGovIndia(api_key=api_key, db_path=db_path)
    datagovin.sync_metadata(batch_size=batch_size, njobs=njobs)
    click.echo("Metadata updated successfully.")

################## get-update-info ##################
@cli.command(name="get-update-info")
@click.option(
    "--api-key",
    default=None,
    type=str,
    help="API key for the OGD platform. Uses 'DATAGOVINDIA_API_KEY' environment variable if not provided.",
)
@click.option(
    "--db-path",
    default=None,
    type=str,
    help=(
        "Path to the SQLite database. Optional if already set in environment variable"
        " 'DATAGOVINDIA_DB_PATH'."
    ),
)
def get_update_info_cli(api_key, db_path):
    """Fetches info for the last metadata update from the OGD platform.

    usage: `datagovindia get-update-info [--api-key <API_KEY>] [--db-path <DB_PATH>]`

    optional arguments:

        - `api-key`: `API key for the OGD platform. Uses 'DATAGOVINDIA_API_KEY' environment variable if not provided.`

        - `db-path`: `Path to the SQLite database. Defaults to 'DATAGOVINDIA_DB_PATH' environment variable or '~/datagovindia.db'.`
    """
    datagovin = DataGovIndia(api_key=api_key, db_path=db_path)
    click.echo("Fetching info for the last metadata update...")
    info = datagovin.get_update_info()
    click.echo(json.dumps(info, indent=4))

################## search ##################
@cli.command(name="search")
@click.argument("query", required=True)
@click.option(
    "--api-key",
    default=None,
    type=str,
    help=(
        "API key to be used for fetching data. Optional if already set in environment variable"
        " 'DATAGOVINDIA_API_KEY'."
    ),
)
@click.option(
    "--db-path",
    default=None,
    type=str,
    help=(
        "Path to the SQLite database. Optional if already set in environment variable"
        " 'DATAGOVINDIA_DB_PATH'."
    ),
)
@click.option(
    "-o", "--output", default=None, type=str, help="Path to the output file if you want to save the results."
)
@click.option("--preview", is_flag=True, help="Display the results in the terminal.", default=False)
@click.option("-n", "--limit", default=5, type=int, show_default=True, help="Number of results to show.")
@click.option(
    "-f",
    "--fields",
    default=["title"],
    multiple=True,
    type=str,
    show_default=True,
    help="List of fields to search in.",
)
@click.option("-s", "--sort-by", default=None, type=str, help="Field to sort results by.")
@click.option("--asc", is_flag=True, help="Sort results in ascending order.")
def search_cli(query, api_key, db_path, output, preview, limit, fields, sort_by, asc):
    """Searches the metadata database based on a query and displays or saves the results.

    usage: `datagovindia search <QUERY> [--api-key <API_KEY>] [--db-path <DB_PATH>] [--output <OUTPUT>] [--show] [--limit <LIMIT>] [--fields <FIELDS>] [--sort-by <SORT_BY>] [--asc]`

    positional arguments:

        - `query`: `Search term or phrase for querying the metadata database.`

    optional arguments:

        - `api-key`: `API key for the OGD platform. Uses 'DATAGOVINDIA_API_KEY' environment variable if not provided.`

        - `db-path`: `Path to the SQLite database. Defaults to 'DATAGOVINDIA_DB_PATH' environment variable or '~/datagovindia.db'.`

        - `output`: `File path to save the search results in CSV format. If not provided, results will be displayed.`

        - `preview`: `Display the search results in the terminal.`

        - `limit`: `Limit the number of displayed results.`

        - `fields`: `Database fields to search in. Multiple fields can be specified.`

        - `sort-by`: `Field to sort the search results by.`

        - `asc`: `Sort the results in ascending order. If not provided, defaults to ascending.`
    """
    datagovin = DataGovIndia(api_key=api_key, db_path=db_path)
    click.echo(f"Searching for '{query}' in fields {fields}...")
    search_df = datagovin.search(query, search_fields=fields, sort_by=sort_by, ascending=asc)

    if preview:
        click.echo(search_df.head(limit))
        click.echo(f"{len(search_df)} results found.")

    if output:
        save_dataframe(search_df, output)
        click.echo(f"{len(search_df)} results saved to '{output}'.")

    else:
        click.echo(f"{len(search_df)} results found.")

################## resource-info ##################
@cli.command(name="get-resource-info")
@click.argument("resource_id", required=True, type=str)
@click.option(
    "--api-key",
    default=None,
    type=str,
    help=(
        "API key to be used for fetching data. Optional if already set in environment variable"
        " 'DATAGOVINDIA_API_KEY'."
    ),
)
@click.option(
    "--db-path",
    default=None,
    type=str,
    help=(
        "Path to the SQLite database. Optional if already set in environment variable"
        " 'DATAGOVINDIA_DB_PATH'."
    ),
)
def get_resource_info_cli(resource_id, api_key, db_path):
    """Fetches info for a given resource ID from the OGD platform and displays it in the terminal.

    usage: `datagovindia resource-info <RESOURCE_ID> [--api-key <API_KEY>] [--db-path <DB_PATH>]`

    positional arguments:

        - `resource_id`: `Unique identifier for the data resource to be fetched.`

    optional arguments:

        - `api-key`: `API key for the OGD platform. Uses 'DATAGOVINDIA_API_KEY' environment variable if not provided.`

        - `db-path`: `Path to the SQLite database. Defaults to 'DATAGOVINDIA_DB_PATH' environment variable or '~/datagovindia.db'.`

    """
    datagovin = DataGovIndia(api_key=api_key, db_path=db_path)
    click.echo(f"Fetching info for resource_id '{resource_id}'...")
    info = datagovin.get_resource_info(resource_id)
    click.echo(json.dumps(info, indent=4))

################## get-data ##################

@cli.command(name="get-data")
@click.argument("resource_id", required=True, type=str)
@click.option(
    "--api-key",
    default=None,
    type=str,
    help=(
        "API key to be used for fetching data. Optional if already set in environment variable"
        " 'DATAGOVINDIA_API_KEY'."
    ),
)
@click.option(
    "--db-path",
    default=None,
    type=str,
    help=(
        "Path to the SQLite database. Optional if already set in environment variable"
        " 'DATAGOVINDIA_DB_PATH'."
    ),
)
@click.option("-o", "--output", default=None, type=str, help="Path to the output file.", required=True)
@click.option("--filters", default={}, type=dict, help="Filters to be applied on the records.")
@click.option(
    "--fields",
    default=[],
    multiple=True,
    type=str,
    help="Fields to be fetched. Keep empty to fetch all fields.",
)
@click.option("--offset", default=0, type=int, help="Offset of the records to be fetched.")
@click.option(
    "--limit", default=None, type=int, help="Number of records to be fetched. (default is all records)"
)
@click.option(
    "--batch-size",
    default=2000,
    type=int,
    help="Number of records to be fetched in a single request. Increase this value to improve performance.",
)
@click.option("--sort-by", default=None, type=str, help="Field to sort results by.")
@click.option("--asc", is_flag=True, help="Sort results in ascending order (default is ascending).")
@click.option(
    "--njobs",
    default=None,
    type=int,
    help="Number of threads to use for collecting data. (default is all cores)",
)
def get_data_cli(
    resource_id, api_key, db_path, output, sort_by, asc, offset, batch_size, limit, filters, fields, njobs
):
    """Fetches data for a given resource ID from the OGD platform and saves it to a specified file.

    usage: `datagovindia get-data <RESOURCE_ID> [--api-key <API_KEY>] [--db-path <DB_PATH>] [--output <OUTPUT>] [--filters <FILTERS>] [--fields <FIELDS>] [--offset <OFFSET>] [--limit <LIMIT>] [--batch-size <BATCH_SIZE>] [--sort-by <SORT_BY>] [--asc] [--njobs <NJOBS>]`

    positional arguments:

        - `resource_id`: `Unique identifier for the data resource to be fetched.`

    optional arguments:

        - `api-key`: `API key for the OGD platform. Uses 'DATAGOVINDIA_API_KEY' environment variable if not provided.`

        - `db-path`: `Path to the SQLite database. Defaults to 'DATAGOVINDIA_DB_PATH' environment variable or '~/datagovindia.db'.`

        - `output`: `File path to save the fetched data in CSV format.`

        - `filters`: `Filter the fetched records based on specified criteria in the format field:value.`

        - `fields`: `Specific fields to fetch from the data resource. Multiple fields can be specified.`

        - `offset`: `Starting offset for fetching the records.`

        - `limit`: `Maximum number of records to fetch. If not specified, fetches all available records.`

        - `batch-size`: `Number of records to fetch in one request. Adjust based on performance and memory considerations.`

        - `sort-by`: `Field to sort the fetched records by.`

        - `asc`: `Sort the fetched records in ascending order. If not provided, defaults to ascending.`

        - `njobs`: `Number of parallel threads for fetching data. Defaults to using all available cores.`

    """
    datagovin = DataGovIndia(api_key=api_key, db_path=db_path)
    click.echo(f"Fetching data for resource_id '{resource_id}'...")
    data = datagovin.get_data(
        resource_id,
        sort_by=sort_by,
        ascending=asc,
        offset=offset,
        batch_size=batch_size,
        limit=limit,
        filters=filters,
        fields=fields,
        njobs=njobs,
    )
    save_dataframe(data, output)
    click.echo(f"{len(data)} records fetched and saved to '{output}'.")

if __name__ == "__main__":
    cli()
    