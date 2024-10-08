# test fncs for gtfs-csv-validator
import os
import fnmatch
import shutil
from tcat_gtfs_csv_validator import gcv_support as gcvsup
from tcat_gtfs_csv_validator import exceptions as gcvex
import sqlite3 as sql
from zipfile import is_zipfile
from zipfile import ZipFile
from pathlib import Path


def _find_directory_with_files(path: Path):
    """ Recursively find the deepest directory that contains files. """
    deepest_dir = None

    for item in path.iterdir():
        if item.is_file():
            # If a file is found, store the parent directory
            deepest_dir = path
        elif item.is_dir():
            # Check this subdirectory recursively
            result = _find_directory_with_files(item)
            if result:
                deepest_dir = result  # Update deepest directory found

    return deepest_dir


def test_release(data_type, schema_version, input_path):
    # input_path may be a zip file or a directory containting a release
    # directories can be easier for testing...
    try:
        dir_path = None
        extracted = False
        con = None
        temp_dir_path = None

        # extract from zip file
        if is_zipfile(input_path):
            zf = ZipFile(input_path)
            temp_dir_path = Path.cwd() / 'tempdir'

            # Clean the tempdir if it already exists
            if temp_dir_path.exists():
                shutil.rmtree(temp_dir_path)
            temp_dir_path.mkdir()

            zf.extractall(temp_dir_path)
            extracted = True

            contents = [item for item in temp_dir_path.iterdir() if item.name != '__MACOSX']

            if len(contents) == 1 and contents[0].is_dir():
                extracted_dir = contents[0]
                dir_with_files = _find_directory_with_files(extracted_dir)
                if dir_with_files:
                    dir_path = dir_with_files
                else:
                    raise gcvex.GCVError('No valid directory containing files found.')
            else:
                if not os.listdir(temp_dir_path):
                    raise gcvex.GCVError('No Files found inside the zip.')
                else:
                    dir_path = temp_dir_path
        else:
            # Assume input is a directory
            dir_path = Path(input_path)
        # set up sqlite connection
        # create a temp db in RAM
        # schemas are stored in csv files for clarity and ease of maintenance
        con = sql.connect(':memory:')

        gcvsup.gcv_debug("testing release in directory: " + str(dir_path))

        # create all tables for this particular data_type
        gcvsup.create_schema_tables(data_type, schema_version, con)

        gcvsup.gcv_debug("schema tables created")

        # read all files from directory test_files/data_schema/version
        # file_list = os.listdir(dir_path)

        # Do the schema checks
        fail = False
        error_log = ''
        for file_path in dir_path.iterdir():
            try:
                test_file(data_type, schema_version, file_path, con)
            except (gcvex.GCVSchemaTestError, gcvex.GCVGeoJsonCheckError) as err:
                # catch GCV schema test exception
                # add exception message to log with file name
                # continue as long as the exception is a gcv schema test exception
                error_log += str(err)
                fail = True

        # if schema check failed, pass backlog of errors
        if (fail):
            raise gcvex.GCVSchemaTestError(error_log)

            # else if schema check passed, now check rules
        gcvsup.gcv_debug("checking " + data_type + " rules on " + str(dir_path))

        gcvsup.check_rules(data_type, schema_version, con, dir_path)

    except gcvex.GCVError as err:
        clean_up(data_type, con, extracted, temp_dir_path)
        raise gcvex.GCVError(str(err))
    except Exception as err:
        clean_up(data_type, con, extracted, temp_dir_path)
        raise
    else:
        if temp_dir_path is not None:
            clean_up(data_type, con, extracted, temp_dir_path)


def clean_up(data_type, con, extracted, dir_path):
    if con is not None:
        gcvsup.drop_all_tables(data_type, con)
        con.close()
    if extracted:
        shutil.rmtree(dir_path)  # remove the temp directory


def test_file(data_type, schema_version, file_path, con):
    if fnmatch.fnmatch(file_path.name, "*.txt"):
        # check schema for csv files
        # loads file_name into schema_table checks for errors
        gcvsup.test_csv_file(data_type, file_path, con)
    elif (data_type == 'gtfs_flex' and fnmatch.fnmatch(file_path.name, "*.geojson")):
        # check the geojson file for flex
        gcvsup.check_locations_geojson(data_type, schema_version, file_path)
    elif (fnmatch.fnmatch(file_path.name, ".*")):
        gcvsup.gcv_log("skipping file: " + str(file_path))
    # ignore files with no extension
    elif (fnmatch.fnmatch(file_path.name, "__*")):
        gcvsup.gcv_log("skipping file: " + str(file_path))
    else:
        raise gcvex.GCVError(
            "unexpected file type - expect .txt or .geojson files (flex only), please be sure to specify the directory containing the release. error from:" + str(
                file_path))
