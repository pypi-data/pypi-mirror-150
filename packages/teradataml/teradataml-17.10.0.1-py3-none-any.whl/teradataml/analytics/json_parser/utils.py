"""
Unpublished work.
Copyright (c) 2021 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: pradeep.garre@teradata.com, gouri.patwardhan@teradata.com
Secondary Owner: PankajVinod.Purandare@teradata.com

This file implements the helper methods and classes which are required to
process In-DB Functions.
"""

from teradataml.options.configure import configure
from teradataml.analytics.json_parser.json_store import _JsonStore
from teradataml.analytics.json_parser.metadata import _AnlyFuncMetadata
from teradataml.common.constants import TeradataAnalyticFunctionTypes
import json, os
from teradataml import _version


def _get_json_data_from_tdml_repo():
    """
    DESCRIPTION:
        An internal function to parse the json files stored in teradataml repo. This function,
        first checks whether the version of json store is same as database version.
        If both versions are same, it then returns an empty list, i.e., the framework
        will neither parse the json files nor generate the SQLE functions. Otherwise cleans
        the json store and parses the json files in the corresponding directory and adds
        the json data to json store.

    PARAMETERS:
        None.

    RAISES:
        None.

    RETURNS:
        An iterator of _AnlyFuncMeta object OR list

    EXAMPLES:
        >>> _get_json_data_from_tdml_repo()
    """

    # Check if the json store version is matched with Vantage database version. If
    # both versions are matched, then the json store has data available so no need
    # to parse again.
    if configure.database_version != _JsonStore.version:

        # Json store version is different from database version. So, json's should
        # be parsed again. Before parsing the json, first clean the json store.
        _JsonStore.clean()

        # Set the json store version to current database version.
        _JsonStore.version = configure.database_version

        json_file_directories = __get_json_files_directory(_JsonStore.version)

        # For the corresponding database version, if teradataml does not have any json
        # files, then return an empty list. So framework will not attach any SQLE function
        # to teradataml.
        if not json_file_directories:
            return []

        # Read the directory, parse the json file and add the _AnlyFuncMeta object to json store
        # and yield the same.
        for json_file_directory in json_file_directories:
            for json_file in os.listdir(json_file_directory):

                file_path = os.path.join(json_file_directory, json_file)
                with open(file_path) as fp:
                    json_data = json.load(fp)
                    metadata = _AnlyFuncMetadata(json_data, file_path)

                    # Functions which do not need to participate in IN-DB Framework
                    # should not be stored in _JsonStore.
                    if metadata.func_name in _JsonStore._functions_to_exclude:
                        continue
                    _JsonStore.add(metadata)
                    yield metadata

    # If both database version and json store version are same, return an empty list so that
    # framework will not attach any SQLE function to teradataml.
    else:
        return []


def __get_json_files_directory(database_version):
    """
    DESCRIPTION:
        An internal function to get the corresponding directory name, which
        contains the json files.

    PARAMETERS:
        database_version:
            Required Argument.
            Specifies the database version.
            Types: str

    RAISES:
        None.

    RETURNS:
        list

    EXAMPLES:
        >>> __get_json_files_directory("15.10.00.00")
    """
    # Get the directory of teradataml module.
    module_directory = os.path.dirname(_version.__file__)

    # Get the sqle json files directory.
    sqle_directory = os.path.join(os.path.dirname(module_directory), "teradataml", "analytics", "jsons", "sqle")

    # Get the table operator json files directory
    table_operators_directory = os.path.join(os.path.dirname(module_directory), "teradataml", "table_operators", "jsons")

    directories = [sqle_directory, table_operators_directory]
    version_directories = []
    for directory in directories:
        for dir_version in os.listdir(directory):

            # Database version will always be similar to NN.nn.nn.nn where NN.nn.nn.nn
            # is equal to the number of the current release. For example, 15.10.00.00.
            # teradataml stores the json files in directories similar to NN.nn. For example,
            # 17.20 . So, get the first matched directory. If no match found, return None.
            if dir_version in database_version:
                yield os.path.join(directory, dir_version)