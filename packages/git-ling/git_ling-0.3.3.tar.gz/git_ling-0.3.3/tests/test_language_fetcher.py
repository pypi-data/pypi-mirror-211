from unittest import TestCase
from unittest import mock
from unittest.mock import patch
from datetime import datetime, timedelta
from git_ling.language_fetcher import fetch_languages

class TestLanguageFetcher(TestCase):
    def setUp(self):
        self.mock_exists_patch = patch('os.path.exists')
        self.mock_getmtime_patch = patch('os.path.getmtime')
        self.mock_update_cache_patch = patch('git_ling.language_fetcher.update_cache')
        self.mock_open_patch = patch('builtins.open', new_callable=mock.mock_open, read_data='Python: {}\n')

        self.mock_exists = self.mock_exists_patch.start()
        self.mock_getmtime = self.mock_getmtime_patch.start()
        self.mock_update_cache = self.mock_update_cache_patch.start()
        self.mock_open = self.mock_open_patch.start()

    def tearDown(self):
        self.mock_exists_patch.stop()
        self.mock_getmtime_patch.stop()
        self.mock_update_cache_patch.stop()
        self.mock_open_patch.stop()

    def test_fetch_languages(self):
        # Mocking os.path.exists to always return True
        self.mock_exists.return_value = True
        # Mocking os.path.getmtime to return a timestamp older than CACHE_MAX_AGE
        self.mock_getmtime.return_value = (datetime.now() - timedelta(days=31)).timestamp()
        # Mocking the update_cache function to do nothing
        self.mock_update_cache.return_value = None
        # Mocking the built-in open function to return a dict when reading the file
        self.mock_open.return_value.__enter__.return_value = self.mock_open.return_value
        languages = fetch_languages()
        self.assertEqual(languages, {'Python': {}}, "Should return a dictionary with languages")
