import click
from audiospotter_cli.client import OrganizationClient
from audiospotter_cli.utils import upload_file, get_files_by_extensions
from rich.console import Console
from rich.progress import track
import hashlib

console = Console()

import yaml

with open("config.yml", "r") as file:
    api = yaml.safe_load(file)

base_url = api["server"]


@click.group()
def run():
    pass


@run.command()
@click.argument("file_source")
@click.argument("path", default=".")
@click.option("--extensions", default="flac,mp3")
@click.option("--omit-duplicates", default=True)
def upload(file_source, path, extensions, omit_duplicates):
    # console.print(f"{file_source}, {path}, {extensions}")
    console.print("Finding file source ...")
    client = OrganizationClient(base_url)

    console.print("Walking the file path ...")
    extensions = extensions.split(",")
    dir_list = get_files_by_extensions(path, extensions)

    # prints all files
    console.print(dir_list)

    duplicates_skipped = 0
    files_uploaded = 0

    for file_name in track(dir_list, description="Uploading..."):
        checksum = hashlib.md5(open(file_name, "rb").read()).hexdigest()
        response = client.get_signed_path(
            file_source, path=file_name, checksum=checksum
        )
        data = response.json()
        if data["checksum_exists_in_project"]:
            # console.print("Checksum already exists!")
            if omit_duplicates:
                duplicates_skipped = duplicates_skipped + 1
                continue

        presigned_url = data["url"]
        presigned_fields = data["fields"]
        response = upload_file(presigned_url, presigned_fields, f"{path}/{file_name}")

        response = client.ingest_file_source(
            file_source, path=file_name, checksum=checksum
        )

        files_uploaded = files_uploaded + 1

    console.print(f"Files uploaded: {files_uploaded}")
    if duplicates_skipped > 0:
        console.print(f"Duplicates skipped: {duplicates_skipped}")


@run.command()
def connect():
    client = OrganizationClient(base_url)
    response = client.get_organization()
    console.print(response.json())


if __name__ == "__main__":
    run()
