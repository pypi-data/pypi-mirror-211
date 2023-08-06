# Copyright 2023 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import zipfile
from tempfile import TemporaryDirectory
from urllib.parse import unquote

from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.helper import generate_identifier
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.records import Record


def import_eln(manager, file_path):
    """Import an RO-Crate file following the "ELN" file specification.

    :param file_path: The path of the file.
    :type file_path: str
    :raises KadiAPYInputError: If the structure of the RO-Crate is not valid.
    :raises KadiAPYRequestError: If any request was not successful while importing the
        data and metadata.
    """
    with zipfile.ZipFile(file_path) as ro_crate, TemporaryDirectory() as tempdir:
        namelist = ro_crate.namelist()

        if not namelist:
            raise KadiAPYInputError("Archive is empty.")

        # We assume the first path contains the root directory of the crate.
        root_dir = namelist[0].split("/")[0]
        metadata_file_path = os.path.join(root_dir, "ro-crate-metadata.json")

        if metadata_file_path not in namelist:
            raise KadiAPYInputError("Missing metadata file in RO-Crate.")

        ro_crate.extractall(tempdir)

        try:
            metadata = json.loads(ro_crate.read(metadata_file_path))
        except json.JSONDecodeError as e:
            raise KadiAPYInputError(f"Error parsing metadata file: {e}") from e

        # Collect all entities in the JSON-LD graph.
        graph = metadata.get("@graph", [])
        entities = {}

        for node in graph:
            if "@id" in node:
                entities[node["@id"]] = node

        if "./" not in entities:
            raise KadiAPYInputError("Missing root dataset in metadata file.")

        root_dataset = entities["./"]

        if not isinstance(root_dataset, dict):
            _raise_invalid_structure()

        root_parts = root_dataset.get("hasPart", [])

        if not isinstance(root_parts, list):
            _raise_invalid_structure()

        collection_id = None

        # Create a collection if we have multiple entries in the root dataset.
        if len(root_parts) > 1:
            response = _create_resource(
                manager, Collection.base_path, {"title": root_dir}
            )
            collection_id = response.json()["id"]

        # Import all datasets as records.
        for root_part in root_parts:
            if not isinstance(root_part, dict):
                _raise_invalid_structure()

            dataset = entities[root_part.get("@id")]

            if dataset is None:
                _raise_invalid_structure()

            if dataset.get("@type") != "Dataset":
                continue

            record_metadata = {
                "title": dataset.get("name", root_part["@id"].split("/")[-1]),
                "tags": dataset.get("keywords", []),
                "description": dataset.get("text", ""),
            }

            response = _create_resource(manager, Record.base_path, record_metadata)
            record = manager.record(id=response.json()["id"])

            # Add the record to the collection, if applicable.
            if collection_id is not None:
                record.add_collection_link(collection_id)

            file_parts = dataset.get("hasPart", [])

            if not isinstance(file_parts, list):
                _raise_invalid_structure()

            # Import all files of the dataset.
            for file_part in file_parts:
                if not isinstance(file_part, dict):
                    _raise_invalid_structure()

                file = entities[file_part.get("@id")]

                if file is None:
                    _raise_invalid_structure()

                if file.get("@type") != "File":
                    continue

                file_id = file_part["@id"].split("/", 1)[-1]
                file_path = os.path.join(tempdir, root_dir, unquote(file_id))
                file_name = file.get("name", file_path)
                file_description = file.get("text", "")

                record.upload_file(file_path, file_name, file_description)


def _raise_invalid_structure():
    raise KadiAPYInputError("Invalid structure of metadata file.")


def _create_resource(manager, base_path, metadata):
    base_identifier = generate_identifier(metadata["title"])
    metadata["identifier"] = base_identifier

    index = 1

    while True:
        response = manager._post(base_path, json=metadata)

        if response.status_code == 201:
            return response

        errors = response.json().get("errors", {})

        # Check if only the identifier was the problem and attempt to fix it.
        if "identifier" in errors and len(errors) == 1:
            suffix = f"-{str(index)}"
            metadata["identifier"] = f"{base_identifier[:50-len(suffix)]}{suffix}"

            index += 1
        else:
            raise KadiAPYRequestError(response.json())

        # Just in case, to make sure we never end up in an endless loop.
        if index > 100:
            break

    raise KadiAPYRequestError("Error attempting to create resource.")
