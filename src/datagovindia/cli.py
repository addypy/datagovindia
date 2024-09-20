import os
import sys
import json
import click
from datagovindia import DataGovIndia, save_dataframe, __version__, check_api_key
import functools

# Decorator for common parameters
def common_options(func):
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
        help="Path to the SQLite database. Optional if already set in environment variable 'DATAGOVINDIA_DB_PATH'.",
    )
    @functools.wraps(func)  # Ensure the original function signature is preserved
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

################## datagovindia cli ##################

@click.group()
def cli():
    """Command-line interface for the DataGovIndia API wrapper."""
    pass

# Version
@cli.command(name="version", context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
def version():
    """Displays the version of the DataGovIndia API wrapper."""
    click.echo(f"datagovindia v{__version__}")

# Validate API Key
@cli.command(name="validate-api-key")
@click.option("--api-key", default=None, type=str, help="API key for the OGD platform. Uses 'DATAGOVINDIA_API_KEY' environment variable if not provided.",)
def validate_api_key_cli(api_key):
    """Validate the API key for the OGD platform."""
    if not api_key:
        api_key = os.getenv("DATAGOVINDIA_API_KEY")
        if not api_key:
            click.echo("API key not provided in arguments or environment variable 'DATAGOVINDIA_API_KEY'.", err=True)
            sys.exit(1)     
    if check_api_key(api_key=api_key):
        click.echo("Your API key is valid.")
    else:
        click.echo("Your API key is invalid. Please check if you have a valid key.", err=True)
        sys.exit(1)

# Sync Metadata
@cli.command(name="sync-metadata")
@common_options
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
    """Fetch and sync metadata from the OGD platform into the SQLite database."""
    click.echo("Syncing latest metadata from the OGD platform...")
    try:
        datagovin = DataGovIndia(api_key=api_key, db_path=db_path, validate_key=True)
    except Exception as e:
        click.echo(f"Error initializing DataGovIndia: {str(e)}", err=True)
        sys.exit(1)
    datagovin.sync_metadata(batch_size=batch_size, njobs=njobs)
    click.echo("Metadata updated successfully.")

# Get Update Info
@cli.command(name="get-update-info")
@common_options
def get_update_info_cli(api_key, db_path):
    """Fetch info for the last metadata update from the OGD platform."""
    datagovin = DataGovIndia(api_key=api_key, db_path=db_path, validate_key=False)
    click.echo("Fetching info for the last metadata update...")
    info = datagovin.get_update_info()
    click.echo(json.dumps(info, indent=4))

# Search
@cli.command(name="search")
@common_options
@click.argument("query", required=True)
@click.option("-o", "--output", default=None, type=str, help="Path to the output file if you want to save the results.")
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
    """Search the metadata database based on a query and display or save the results."""
    datagovin = DataGovIndia(api_key=api_key, db_path=db_path, validate_key=False)
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

# Get Resource Info
@cli.command(name="get-resource-info")
@common_options
@click.argument("resource_id", required=True, type=str)
def get_resource_info_cli(resource_id, api_key, db_path):
    """Fetch info for a given resource ID from the OGD platform and display it in the terminal."""
    datagovin = DataGovIndia(api_key=api_key, db_path=db_path, validate_key=True)
    click.echo(f"Fetching info for resource_id '{resource_id}'...")
    info = datagovin.get_resource_info(resource_id)
    click.echo(json.dumps(info, indent=4))

# Get Data
@cli.command(name="get-data")
@common_options
@click.argument("resource_id", required=True, type=str)
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
@click.option("--limit", default=None, type=int, help="Number of records to be fetched. (default is all records)")
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
    """Fetch data for a given resource ID and save it to a specified file."""
    datagovin = DataGovIndia(api_key=api_key, db_path=db_path, validate_key=True)
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
