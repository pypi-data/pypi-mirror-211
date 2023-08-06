
from git_ling import PyLinguist
from git_ling.schemas import Language

def test_update_languages():
    pylinguist = pylinguist()
    assert isinstance(pylinguist.languages, dict), "Languages should be of dict type"
    for language in pylinguist.languages.values():
        assert isinstance(language, Language), "Language should be of Language type"

def test_get_language_group():
    pylinguist = PyLinguist()
    language_name = "Python" # assuming we have a language named Python
    language = pylinguist.get_language_info(language_name)
    group_id = language.group_id # assuming we have a language group with id 1
    languages = pylinguist.get_language_group(group_id)
    assert isinstance(languages, list), "Should return a list"
    for language in languages:
        assert language.language_id == group_id, "All languages should belong to the same group"

def test_file_belongs_to_group_id(mocker):
    mocker.patch('os.path.isfile', return_value=True)
    pylinguist = pylinguist()
    filename = "/path/to/file.py"
    language_name = "Python" # assuming we have a language named Python
    language = pylinguist.get_language_info(language_name)
    assert pylinguist.file_belongs_to_group_id(filename, language.group_id), "Should return True if file belongs to group"

def test_get_language_info():
    pylinguist = pylinguist()
    language_name = "Python" # assuming we have a language named Python
    language = pylinguist.get_language_info(language_name)
    assert isinstance(language, Language), "Should return a Language instance"
    assert language.name == language_name, "Should return the correct language"

def test_file_belongs_to_language(mocker):
    mocker.patch('os.path.isfile', return_value=True)
    pylinguist = pylinguist()
    filename = "/path/to/file.py"
    language = pylinguist.get_language_info("Python") # assuming Python is a valid language
    extra_filenames = ["file.py"]
    assert pylinguist.file_belongs_to_language(filename, language, extra_filenames), "Should return True if file belongs to language"
