from unittest import TestCase
from unittest.mock import MagicMock, patch
from git_ling import GitLing
from git_ling.schemas import Language

class TestGitLing(TestCase):

    def test_update_languages(self):
        git_ling = GitLing()
        self.assertIsInstance(git_ling.languages, dict, "Languages should be of dict type")
        for language in git_ling.languages.values():
            self.assertIsInstance(language, Language, "Language should be of Language type")

    def test_get_language_group(self):
            git_ling = GitLing()
            language_name = "tcsh" # assuming we have a language named Tcsh
            language = git_ling.get_language_info(language_name)
            group = language.group # assuming we have a language group "Shell"
            self.assertIsInstance(group, str, "Should return a string")
            languages = git_ling.get_language_group(group)
            self.assertIsInstance(languages, list, "Should return a list")
            self.assertTrue(len(languages) > 0, "Should return a list with at least one language")
            for language in languages:
                self.assertEqual(language.group, group, "All languages should belong to the same group")


    @patch('os.path.isfile', return_value=True)
    def test_file_belongs_to_group(self, mock_isfile):
        git_ling = GitLing()
        filename = "/path/to/file.tcsh"
        language = git_ling.get_language_info(language_name="tcsh")
        self.assertTrue(git_ling.file_belongs_to_group(filename, language.group), "Should return True if file belongs to group")

    def test_get_language_info(self):
        git_ling = GitLing()
        language_name = "Python" # assuming we have a language named Python
        language = git_ling.get_language_info(language_name)
        self.assertIsInstance(language, Language, "Should return a Language instance")
        self.assertEqual(language.name, language_name, "Should return the correct language")

    @patch('os.path.isfile', return_value=True)
    def test_file_belongs_to_language(self, mock_isfile):
        git_ling = GitLing()
        filename = "/path/to/file.py"
        language = git_ling.get_language_info("Python") # assuming Python is a valid language
        extra_filenames = ["file.py"]
        self.assertTrue(git_ling.file_belongs_to_language(filename, language, extra_filenames), "Should return True if file belongs to language")

    @patch('os.path.isfile', return_value=True)
    def test_get_supported_languages(self, mock_isfile):
        git_ling = GitLing()
        filename = "/path/to/file.py"
        language_names = ["Python", "Java"]  # assuming these are valid languages
        supported_languages = list(git_ling.get_supported_languages(filename, language_names))
        self.assertIsInstance(supported_languages, list, "Should return a list")
        self.assertTrue(len(supported_languages) > 0, "Should return a list with at least one language")
        for language in supported_languages:
            self.assertIsInstance(language, Language, "Should return a Language instance")
            self.assertIn(language.name, language_names, "Returned language should be in the original list")
