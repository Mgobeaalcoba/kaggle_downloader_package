# KaggleDownloader

`KaggleDownloader` is a Python class designed to interact with Kaggle, enabling users to authenticate, search, download, and extract datasets. The class can be used both interactively in Jupyter Notebooks or via the command line.

## Prerequisites

Before using the `KaggleDownloader` class, make sure you have:

- A Kaggle API token, available from your Kaggle account under "API" (https://www.kaggle.com/settings).
- Python 3.x installed.

## Section 1: Using KaggleDownloader in a Jupyter Notebook

You can import and use `KaggleDownloader` directly within a Jupyter Notebook. Below is a step-by-step guide to authenticate and download datasets using the class methods.

### 1.1 Example Code

```python
import kaggle_downloader as kd  # Assuming you've saved the class in kaggle_downloader.py
import pandas as pd

# Initialize KaggleDownloader
downloader = kd.KaggleDownloader(api_token_path="./kaggle.json")

# Authenticate with Kaggle API
downloader.authenticate_kaggle()

# Search for datasets related to a theme
downloader.search_datasets("netflix")

# Download a specific dataset by its slug
downloader.download_dataset("shivamb/netflix-shows")

df = pd.read_csv("./netflix_titles.csv", delimiter=',', encoding="utf-8", encoding_errors="replace")
df.head()
```

### 1.2 Available Methods

- **`get_api_token_path()`**: Returns the path to the primary Kaggle API token file.
- **`get_alternative_token_path()`**: Returns the path to the alternative Kaggle API token file.
- **`get_path_downloads()`**: Returns the download directory path.
- **`set_api_token_path(new_path)`**: Sets a new path for the Kaggle API token.
- **`set_alternative_token_path(new_path)`**: Sets a new path for the alternative Kaggle API token.
- **`set_path_downloads(new_path)`**: Sets a new path for downloaded datasets.
- **`authenticate_kaggle()`**: Authenticates with the Kaggle API by loading credentials from the token file.
- **`authenticate_with_credentials()`**: Prompts the user to manually enter Kaggle credentials and saves them to a file.
- **`search_datasets(dataset_theme)`**: Searches Kaggle for datasets matching a given keyword or theme.
- **`download_dataset(dataset_slug)`**: Downloads a dataset from Kaggle to the specified directory.
- **`extract_zip(zip_file)`**: Extracts a downloaded zip file to the download directory.
- **`check_kaggle_json()`**: Checks if the Kaggle API token file exists at either the primary or alternative path.
- **`create_download_directory(path)`**: Creates the directory where datasets will be saved, if it doesn't already exist.

## Section 2: Using KaggleDownloader via Command-Line Interface (CLI)

Alternatively, you can use the `KaggleDownloader` class via the command line. The `main()` method allows users to run the class and download datasets by specifying the dataset slug as an argument.

### 2.1 Example CLI Usage

1. First, make sure your script is executable:
   ```bash
   chmod +x kaggle_downloader.py
   ```

2. Use the following command to download a dataset from Kaggle:
   ```bash
   python kaggle_downloader_package/kaggle_downloader.py benroshan/ecommerce-data
   ```

This will authenticate with Kaggle (based on your `kaggle.json` token file) and download the dataset to the directory specified in `path_downloads` (or the current working directory by default).

### 2.2 CLI Arguments

- **`dataset_slug`**: The Kaggle dataset identifier (slug) that you want to download, e.g., `benroshan/ecommerce-data`.

## Notes

- Ensure you have a Kaggle API token in place (`kaggle.json`).
- You can specify alternative token paths in case the default one isn't used.
- If you prefer to manually upload your Kaggle username and key, our KaggleDownloader will ask for them as it cannot find the kaggle.json file.
- Large datasets will be automatically unzipped if downloaded as zip files.
- The CLI interface will parse arguments and invoke necessary functions for a seamless experience.

### Customization:
- Replace `kaggle_downloader.py` with the actual file name if different.
- Adjust the class import path (`from kaggle_downloader import KaggleDownloader`) if you organize your code differently.

## Contributing

Feel free to contribute to this project by submitting issues, feature requests, or pull requests on GitHub.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

**Mariano Gobea Alcoba**  
Email: gobeamariano@gmail.com
