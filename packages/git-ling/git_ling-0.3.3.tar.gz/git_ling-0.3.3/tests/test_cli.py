import unittest
from unittest.mock import patch, MagicMock
from git_ling import cli, language_fetcher
from git_ling import Language, GitLing


class MockLanguage(Language):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name")
        self.extensions = kwargs.get("extensions")
        self.group = kwargs.get("group")
        self.aliases = kwargs.get("aliases")

class TestCLI(unittest.TestCase):

    @patch("argparse.ArgumentParser.parse_args")
    @patch.object(GitLing, "file_belongs_to_language")
    @patch.object(GitLing, "__init__", return_value=None)  # This is required to avoid calling the actual constructor
    @patch.object(language_fetcher, "fetch_languages", return_value={
           "python": MockLanguage(name="Python", extensions=['.py'], group="Scripting", aliases=['py'])

    })
    def test_main(self, mock_fetch_languages, mock_init, mock_file_belongs_to_language, mock_args):
        mock_args.return_value = MagicMock(file_path="test.py")
        mock_file_belongs_to_language.return_value = True

        git_ling = GitLing()  # This will not call the actual constructor due to the mock
        git_ling.languages = mock_fetch_languages.return_value  # Set the languages attribute manually

        with patch("builtins.print") as mocked_print, \
            patch("git_ling.cli.GitLing", return_value=git_ling):  # Mock the git_ling instance in cli module

            cli.main()

            # Check if the correct prints were made
            mocked_print.assert_any_call("File: test.py is supported in python")
            mocked_print.assert_any_call("Details about the language:")
            mocked_print.assert_any_call("Name: Python")
            mocked_print.assert_any_call("Extensions: ['.py']")
            mocked_print.assert_any_call("Group: Scripting")
            mocked_print.assert_any_call("Aliases: ['py']")

if __name__ == "__main__":
    unittest.main()
