import shutil
import fnmatch
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from tcat_gtfs_csv_validator import gcv_test_release
from tcat_gtfs_csv_validator import exceptions as gcvex
from tcat_gtfs_csv_validator import gcv_support as gcvsup

TEST_FILES_PATH = f'{Path.cwd()}/tests/test_files'

PATHWAYS_SUCCESS_FILE = f'{TEST_FILES_PATH}/gtfs_pathways/v1.0/success_1_all_attrs.zip'
PATHWAYS_FAILURE_FILE = f'{TEST_FILES_PATH}/gtfs_pathways/v1.0/fail_rules_1.zip'
MAC_GENERATED_FILE = f'{TEST_FILES_PATH}/gtfs_flex/v2.0/success_2_mac_issue.zip'
FLEX_SUCCESS_FILE = f'{TEST_FILES_PATH}/gtfs_flex/v2.0/success_1_all_attrs.zip'
FLEX_FAILURE_FILE = f'{TEST_FILES_PATH}/gtfs_flex/v2.0/fail_schema_1.zip'


class TestGVCTestRelease(unittest.TestCase):
    def test_gtfs_pathways_success(self):
        data_type = 'gtfs_pathways'
        schema_version = 'v1.0'
        input_path = PATHWAYS_SUCCESS_FILE
        with patch('tcat_gtfs_csv_validator.gcv_test_release.test_release') as mock_test_release:
            try:
                gcv_test_release.test_release(data_type, schema_version, input_path)
            except gcvex.GCVError as err:
                self.fail(f"test_release raised an exception: {err}")

                # Verify test_release was called once
            mock_test_release.assert_called_once_with(data_type, schema_version, input_path)

    @patch('tcat_gtfs_csv_validator.gcv_test_release.test_release')
    def test_gtfs_pathways_fail(self, mock_test_release):
        data_type = 'gtfs_pathways'
        schema_version = 'v1.0'
        input_path = PATHWAYS_FAILURE_FILE

        mock_test_release.side_effect = gcvex.GCVError('Test exception')
        with self.assertRaises(gcvex.GCVError):
            gcv_test_release.test_release(data_type, schema_version, input_path)

        # Verify test_release was called once
        mock_test_release.assert_called_once_with(data_type, schema_version, input_path)

    @patch('tcat_gtfs_csv_validator.gcv_test_release.test_release')
    def test_gtfs_pathways_fail_with_wrong_schema(self, mock_test_release):
        data_type = 'gtfs_pathways'
        schema_version = 'v2.0'
        input_path = PATHWAYS_FAILURE_FILE

        mock_test_release.side_effect = gcvex.GCVError('Schema exception')
        with self.assertRaises(gcvex.GCVError):
            gcv_test_release.test_release(data_type, schema_version, input_path)

        # Verify test_release was called once
        mock_test_release.assert_called_once_with(data_type, schema_version, input_path)

    def test_gtfs_mac_generated_file_success(self):
        data_type = 'gtfs_pathways'
        schema_version = 'v1.0'
        input_path = MAC_GENERATED_FILE
        with patch('tcat_gtfs_csv_validator.gcv_test_release.test_release') as mock_test_release:
            try:
                gcv_test_release.test_release(data_type, schema_version, input_path)
            except gcvex.GCVError as err:
                self.fail(f"test_release raised an exception: {err}")

                # Verify test_release was called once
            mock_test_release.assert_called_once_with(data_type, schema_version, input_path)

    def test_gtfs_flex_success(self):
        data_type = 'gtfs_flex'
        schema_version = 'v2.0'
        input_path = FLEX_SUCCESS_FILE
        with patch('tcat_gtfs_csv_validator.gcv_test_release.test_release') as mock_test_release:
            try:
                gcv_test_release.test_release(data_type, schema_version, input_path)
            except gcvex.GCVError as err:
                self.fail(f"test_release raised an exception: {err}")

                # Verify test_release was called once
            mock_test_release.assert_called_once_with(data_type, schema_version, input_path)

    @patch('tcat_gtfs_csv_validator.gcv_test_release.test_release')
    def test_gtfs_flex_failure(self, mock_test_release):
        data_type = 'gtfs_flex'
        schema_version = 'v2.0'
        input_path = FLEX_FAILURE_FILE
        mock_test_release.side_effect = gcvex.GCVError('Schema exception')
        with self.assertRaises(gcvex.GCVError):
            gcv_test_release.test_release(data_type, schema_version, input_path)

        # Verify test_release was called once
        mock_test_release.assert_called_once_with(data_type, schema_version, input_path)

    @patch('shutil.rmtree')
    @patch('tcat_gtfs_csv_validator.gcv_support.drop_all_tables')
    def test_clean_up_con_not_none_extracted_true(self, mock_drop_all_tables, mock_rmtree):
        con = MagicMock()
        data_type = 'gtfs_pathways'
        dir_path = 'tempdir'
        extracted = True

        gcv_test_release.clean_up(data_type, con, extracted, dir_path)

        mock_drop_all_tables.assert_called_once_with(data_type, con)
        con.close.assert_called_once()
        mock_rmtree.assert_called_once_with(dir_path)

    @patch('shutil.rmtree')
    @patch('tcat_gtfs_csv_validator.gcv_support.drop_all_tables')
    def test_clean_up_con_not_none_extracted_false(self, mock_drop_all_tables, mock_rmtree):
        con = MagicMock()
        data_type = 'gtfs_pathways'
        dir_path = 'tempdir'
        extracted = False

        gcv_test_release.clean_up(data_type, con, extracted, dir_path)

        mock_drop_all_tables.assert_called_once_with(data_type, con)
        con.close.assert_called_once()
        mock_rmtree.assert_not_called()

    @patch('shutil.rmtree')
    @patch('tcat_gtfs_csv_validator.gcv_support.drop_all_tables')
    def test_clean_up_con_none_extracted_true(self, mock_drop_all_tables, mock_rmtree):
        con = None
        data_type = 'gtfs_pathways'
        dir_path = 'tempdir'
        extracted = True

        gcv_test_release.clean_up(data_type, con, extracted, dir_path)

        mock_drop_all_tables.assert_not_called()
        mock_rmtree.assert_called_once_with(dir_path)

    @patch('shutil.rmtree')
    @patch('tcat_gtfs_csv_validator.gcv_support.drop_all_tables')
    def test_clean_up_con_none_extracted_false(self, mock_drop_all_tables, mock_rmtree):
        con = None
        data_type = 'gtfs_pathways'
        dir_path = 'tempdir'
        extracted = False

        gcv_test_release.clean_up(data_type, con, extracted, dir_path)

        mock_drop_all_tables.assert_not_called()
        mock_rmtree.assert_not_called()

    @patch('tcat_gtfs_csv_validator.gcv_support.test_csv_file')
    def test_txt_file(self, mock_test_csv_file):
        data_type = 'gtfs_pathways'
        schema_version = 'v1'
        file_path = Path('dummy.txt')
        con = MagicMock()

        gcv_test_release.test_file(data_type, schema_version, file_path, con)

        mock_test_csv_file.assert_called_once_with(data_type, file_path, con)

    @patch('tcat_gtfs_csv_validator.gcv_support.check_locations_geojson')
    def test_geojson_file_flex(self, mock_check_locations_geojson):
        data_type = 'gtfs_flex'
        schema_version = 'v1'
        file_path = Path('dummy.geojson')
        con = MagicMock()

        gcv_test_release.test_file(data_type, schema_version, file_path, con)

        mock_check_locations_geojson.assert_called_once_with(data_type, schema_version, file_path)

    @patch('tcat_gtfs_csv_validator.gcv_support.gcv_log')
    def test_hidden_file(self, mock_gcv_log):
        data_type = 'gtfs_pathways'
        schema_version = 'v1'
        file_path = Path('.hiddenfile')
        con = MagicMock()

        gcv_test_release.test_file(data_type, schema_version, file_path, con)

        mock_gcv_log.assert_called_once_with("skipping file: " + str(file_path))

    @patch('tcat_gtfs_csv_validator.gcv_support.gcv_log')
    def test_no_extension_file(self, mock_gcv_log):
        data_type = 'gtfs_pathways'
        schema_version = 'v1'
        file_path = Path('__noextension')
        con = MagicMock()

        gcv_test_release.test_file(data_type, schema_version, file_path, con)

        mock_gcv_log.assert_called_once_with("skipping file: " + str(file_path))

    def test_unexpected_file_type(self):
        data_type = 'gtfs_pathways'
        schema_version = 'v1'
        file_path = Path('unexpected.xyz')
        con = MagicMock()

        with self.assertRaises(gcvex.GCVError) as context:
            gcv_test_release.test_file(data_type, schema_version, file_path, con)

        self.assertTrue("unexpected file type" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
