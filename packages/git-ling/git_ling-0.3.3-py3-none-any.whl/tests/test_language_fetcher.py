import datetime
import pytest
from git_ling.language_fetcher import fetch_languages, update_cache

def test_fetch_languages(mocker):
    # Mocking os.path.exists to always return True
    mocker.patch('os.path.exists', return_value=True)
    # Mocking os.path.getmtime to return a timestamp older than CACHE_MAX_AGE
    mocker.patch('os.path.getmtime', return_value=(datetime.now() - datetime.timedelta(days=31)).timestamp())
    # Mocking the update_cache function to do nothing
    mocker.patch('language_fetcher.update_cache')
    # Mocking the built-in open function to return a dict when reading the file
    mocker.patch('builtins.open', mocker.mock_open(read_data='Python: {}'))
    languages = fetch_languages()
    assert languages == {'Python': {}}, "Should return a dictionary with languages"

def test_update_cache(mocker):
    # Mocking urllib.request.urlretrieve to return a tuple where the first element is the filename
    mocker.patch('urllib.request.urlretrieve', return_value=('languages.yml', None))
    update_cache()

@pytest.mark.parametrize("file_exists,timestamp,should_update", [
    (False, None, True),  # Case where the file does not exist
    (True, (datetime.now() - datetime.timedelta(days=31)).timestamp(), True),  # Case where the file is older than CACHE_MAX_AGE
    (True, datetime.now().timestamp(), False)  # Case where the file is up to date
])
def test_fetch_languages_update_logic(file_exists, timestamp, should_update, mocker):
    mocker.patch('os.path.exists', return_value=file_exists)
    mocker.patch('os.path.getmtime', return_value=timestamp)
    update_cache_mock = mocker.patch('language_fetcher.update_cache')
    fetch_languages()
    if should_update:
        update_cache_mock.assert_called_once()
    else:
        update_cache_mock.assert_not_called()
