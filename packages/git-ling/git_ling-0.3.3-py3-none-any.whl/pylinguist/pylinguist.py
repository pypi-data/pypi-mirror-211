import logging
import os
from .schemas import *
from .language_fetcher import fetch_languages

class PyLinguist:
    """
    PyLinguist class
    This class is the main class of the library. It is used to get information about languages and files.
    """
    logger= logging.getLogger(__name__)
    
    def __init__(self):
        self.languages: Languages = {}
        self.update_languages()

    def update_languages(self):
        self.logger.info("Updating languages")
        # Get languages from yaml file
        self.languages = fetch_languages()

        # Update Languages with Language objects
        for language in self.languages:
            try:
                language_object = Language(name=language,**self.languages[language])
                self.languages[language] = language_object
            except ValueError:
                self.logger.warning(f"Language {language} has invalid value")


    def get_language_group(self, group_id: int)->List[Language]:
        """
        Returns a list of languages that belong to a language group
        """
        return [language for language in self.languages.values() if language.language_id == group_id]
    
    def get_language_info(self, language_name:str)->Language:
        """
        Returns a Language object for a given language name
        """
        if language_name in self.languages:
            return self.languages[language_name]
        else:
            return None

    def file_belongs_to_language(self, filename, language: Language, extra_filenames:List[str]=[])->bool:
        """
        Checks if a file belongs to a language
        """
        # Check if file exist and is a file
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File {filename} does not exist")
        # Get the base name of the file (file name with extension)
        base_name = os.path.basename(filename)
        # To get the file name and extension separately, you can use os.path.splitext
        file_name, file_extension = os.path.splitext(base_name)
        self.logger.debug(f"Checking  if File name: {base_name} belongs to language {language.name}")
        # Check if file belongs to language
        if language.extensions:
            if file_extension in language.extensions: # Check if extension is in list of extensions
                self.logger.debug(f"File extension {file_extension} is in list of extensions for language {language.name}")
                return True
        if language.filenames: # Check if file name is in list of common filenames for language
            if base_name in language.filenames:
                self.logger.debug(f"File name {base_name} is in list of common filenames for language {language.name}")
                return True
        if extra_filenames:
            if base_name in extra_filenames:
                self.logger.debug(f"File name {base_name} is in list of extra filenames for language {language.name}")
                return True
        return False # File does not belong to language
    
    def file_belongs_to_group_id(self, filename, group_id: int)->bool:
        """
        Checks if a file belongs to a language group
        """
        languages = self.get_language_group(group_id)
        for language in languages:
            if self.file_belongs_to_language(filename, language):
                return True
        return False
            
