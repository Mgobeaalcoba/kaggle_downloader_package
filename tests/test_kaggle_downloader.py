import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from kaggle_downloader_package.kaggle_downloader import KaggleDownloader

class TestKaggleDownloader(unittest.TestCase):
    """Test suite for the KaggleDownloader class."""

    def setUp(self):
        """Set up a KaggleDownloader instance before each test."""
        self.kaggle_downloader = KaggleDownloader()

    def test_get_api_token_path(self):
        """Test that the API token path is returned correctly."""
        self.assertEqual(self.kaggle_downloader.get_api_token_path(), os.path.expanduser("./kaggle.json"))

    def test_get_alternative_token_path(self):
        """Test that the alternative API token path is returned correctly."""
        self.assertEqual(self.kaggle_downloader.get_alternative_token_path(), os.path.expanduser("~/.kaggle/kaggle.json"))

    def test_get_path_downloads(self):
        """Test that the default download path is returned correctly."""
        self.assertEqual(self.kaggle_downloader.get_path_downloads(), ".")

    def test_set_api_token_path(self):
        """Test setting a new API token path."""
        new_path = "/new/kaggle.json"
        self.kaggle_downloader.set_api_token_path(new_path)
        self.assertEqual(self.kaggle_downloader.get_api_token_path(), new_path)

    def test_set_alternative_token_path(self):
        """Test setting a new alternative API token path."""
        new_path = "/new/alternative/kaggle.json"
        self.kaggle_downloader.set_alternative_token_path(new_path)
        self.assertEqual(self.kaggle_downloader.get_alternative_token_path(), new_path)

    def test_set_path_downloads(self):
        """Test setting a new download path."""
        new_path = "/new/download/path"
        self.kaggle_downloader.set_path_downloads(new_path)
        self.assertEqual(self.kaggle_downloader.get_path_downloads(), new_path)

    @patch("builtins.open", new_callable=mock_open, read_data='{"username": "testuser", "key": "testkey"}')
    @patch("os.path.exists")
    @patch("os.environ", {})
    def test_authenticate_kaggle_success(self, mock_exists, mock_open_file):
        """Test successful Kaggle authentication by loading credentials from file."""
        mock_exists.side_effect = [True, False]
        self.kaggle_downloader.authenticate_kaggle()
        self.assertEqual(os.environ['KAGGLE_USERNAME'], 'testuser')
        self.assertEqual(os.environ['KAGGLE_KEY'], 'testkey')

    @patch("builtins.input", side_effect=["my_username", "my_password"])
    @patch("os.path.exists", return_value=False)  # Simula que no existe el archivo kaggle.json
    @patch("os.environ", new_callable=MagicMock)  # Mock para os.environ
    def test_authenticate_with_credentials_success(self, mock_environ, mock_exists, mock_input):
        """Test authentication using manual input for username and password."""
        
        # Llama al método de autenticación
        self.kaggle_downloader.authenticate_kaggle()
        
        # Verifica que las variables de entorno se hayan configurado correctamente
        mock_environ.__setitem__.assert_any_call('KAGGLE_USERNAME', 'my_username')
        mock_environ.__setitem__.assert_any_call('KAGGLE_KEY', 'my_password')
        print("Manual authentication test passed.")

    @patch("subprocess.run")
    def test_search_datasets(self, mock_subprocess):
        """Test searching for datasets using the Kaggle API."""
        self.kaggle_downloader.search_datasets("data")
        mock_subprocess.assert_called_with(["kaggle", "datasets", "list", "-s", "data"], check=True, stdout=-1, stderr=-1, text=True)

    @patch("subprocess.run")
    @patch("os.path.exists", return_value=True)
    def test_download_dataset_directory_exists(self, mock_exists, mock_subprocess):
        """Test downloading a dataset when the download directory already exists."""
        self.kaggle_downloader.download_dataset("test-dataset")
        mock_subprocess.assert_called_with(
            ["kaggle", "datasets", "download", "-d", "test-dataset", "-p", ".", "--unzip"],
            check=True, stdout=-1, stderr=-1, text=True
        )

    @patch("subprocess.run")
    @patch("os.path.exists", return_value=False)
    @patch("os.makedirs")
    @patch.object(KaggleDownloader, "get_path_downloads", return_value=".")
    def test_download_dataset_directory_created(self, mock_get_path_downloads, mock_makedirs, mock_exists, mock_subprocess):
        """Test downloading a dataset when the download directory is created."""
        self.kaggle_downloader.download_dataset("test-dataset")
        mock_makedirs.assert_called_with(".")
        mock_subprocess.assert_called_with(
            ["kaggle", "datasets", "download", "-d", "test-dataset", "-p", ".", "--unzip"],
            check=True, stdout=-1, stderr=-1, text=True
        )

    @patch("zipfile.ZipFile.extractall")
    @patch("zipfile.ZipFile", autospec=True)
    @patch("zipfile.is_zipfile", return_value=True)
    @patch("os.path.exists", side_effect=lambda path: path == "test.zip")
    @patch.object(KaggleDownloader, "get_path_downloads", return_value=".")
    def test_extract_zip_success(self, mock_get_path_downloads, mock_exists, mock_is_zipfile, mock_zip_file_class, mock_extractall):
        """Test successful extraction of a zip file."""
        mock_zip_file = MagicMock()
        mock_zip_file_class.return_value.__enter__.return_value = mock_zip_file
        self.kaggle_downloader.extract_zip("test.zip")
        mock_zip_file.extractall.assert_called_once_with(".")

    @patch("os.path.exists", return_value=False)
    def test_extract_zip_file_not_found(self, mock_exists):
        """Test extraction failure when the zip file is not found."""
        with self.assertRaises(FileNotFoundError):
            self.kaggle_downloader.extract_zip("non_existent.zip")

    @patch("os.path.exists", return_value=True)
    @patch("zipfile.is_zipfile", return_value=False)
    def test_extract_zip_invalid_zip(self, mock_exists, mock_is_zipfile):
        """Test extraction failure when the zip file is invalid."""
        with self.assertRaises(ValueError):
            self.kaggle_downloader.extract_zip("invalid.zip")

    @patch("os.path.exists", side_effect=[True, False])
    def test_check_kaggle_json_primary_exists(self, mock_exists):
        """Test that the primary kaggle.json token exists."""
        result = self.kaggle_downloader.check_kaggle_json()
        self.assertEqual(result, os.path.expanduser("./kaggle.json"))

    @patch("os.path.exists", side_effect=[False, True])
    def test_check_kaggle_json_alternative_exists(self, mock_exists):
        """Test that the alternative kaggle.json token exists."""
        result = self.kaggle_downloader.check_kaggle_json()
        self.assertEqual(result, os.path.expanduser("~/.kaggle/kaggle.json"))

    @patch("os.path.exists", return_value=False)
    def test_check_kaggle_json_not_found(self, mock_exists):
        """Test failure when neither kaggle.json file exists."""
        with self.assertRaises(FileNotFoundError):
            self.kaggle_downloader.check_kaggle_json()

    @patch("os.makedirs")
    @patch("os.path.exists", return_value=False)
    def test_create_download_directory(self, mock_exists, mock_makedirs):
        """Test that the download directory is created if it doesn't exist."""
        self.kaggle_downloader.create_download_directory("/new/path")
        mock_makedirs.assert_called_with("/new/path")

    @patch("os.path.exists", return_value=True)
    def test_create_download_directory_exists(self, mock_exists):
        """Test that no directory is created if it already exists."""
        with patch.object(self.kaggle_downloader, "set_path_downloads") as mock_set_path_downloads:
            self.kaggle_downloader.create_download_directory("/existing/path")
            mock_set_path_downloads.assert_called_with(new_path="/existing/path")
    
    @patch('kaggle_downloader_package.kaggle_downloader.KaggleDownloader.authenticate_kaggle')
    @patch('kaggle_downloader_package.kaggle_downloader.KaggleDownloader.download_dataset')
    @patch('sys.argv', ['kaggle_downloader', 'test-dataset'])
    def test_main_with_custom_path(self, mock_download, mock_authenticate):
        """Test main() function with custom download path."""
        KaggleDownloader.main()
        mock_authenticate.assert_called_once()
        mock_download.assert_called_once_with('test-dataset')

    @patch('kaggle_downloader_package.kaggle_downloader.KaggleDownloader.authenticate_kaggle')
    @patch('kaggle_downloader_package.kaggle_downloader.KaggleDownloader.download_dataset')
    @patch('sys.argv', ['kaggle_downloader', 'test-dataset'])
    def test_main_with_default_path(self, mock_download, mock_authenticate):
        """Test main() function with default download path."""
        KaggleDownloader.main()
        mock_authenticate.assert_called_once()
        mock_download.assert_called_once_with('test-dataset')


if __name__ == "__main__":
    unittest.main()
