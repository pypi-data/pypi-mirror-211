from uplink import Consumer, get, post, headers, Field

import yaml

with open("config.yml", "r") as file:
    api = yaml.safe_load(file)

key = api["key"]


@headers({"audiospotter-apikey": key})
class OrganizationClient(Consumer):
    @get("/api/v1/organizations/")
    def get_organization(self):
        """Get organization information"""

    @get("/api/v1/file-sources/{id}/")
    def get_file_source(self, id):
        """Get file source information"""

    @post("/api/v1/file-sources/{id}/signed-path/")
    def get_signed_path(self, id, path: Field, checksum: Field):
        """Get file source information"""

    @post("/api/v1/file-sources/{id}/ingest-source-file/")
    def ingest_file_source(self, id, path: Field, checksum: Field):
        """Get file source information"""
