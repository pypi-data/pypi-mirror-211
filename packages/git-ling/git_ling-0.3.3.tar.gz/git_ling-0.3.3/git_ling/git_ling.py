import logging
import os
from .schemas import *
from .language_fetcher import fetch_languages

class GitLing:
    """
    git_ling class
    This class is the main class of the library. It is used to get information about languages and files.
    """
    logger= logging.getLogger(__name__)
    
    def __init__(self):
        self.languages: Languages = {}
        self.groups: Groups = {}
        self.update_languages()

    def update_languages(self):
        self.logger.info("Updating languages")
        # Get languages from yaml file
        fetched_langs = fetch_languages()

        # Update Languages with Language objects
        for key, val in fetched_langs.items():
            try:
                language_object = Language(name=key,**val)
                language_name=language_object.name.lower()
                self.languages[language_name] = language_object  
                if language_object.aliases and isinstance(language_object.aliases, list):
                    for alias in language_object.aliases:
                        self.languages[alias] = language_object
                self.groups.setdefault(language_object.group, []).append(language_object)
            except ValueError:
                self.logger.warning(f"Language {key} has invalid value")


    def get_language_group(self, group: str)->List[Language]:
        """
        Returns a list of languages that belong to a language group (e.g. Shell)
        """
        if group in self.groups:
            return self.groups[group]
        else:
            return []
    
    def get_language_info(self, language_name:str)->Language:
        """
        Returns a Language object for a given language name
        """
        # Check if language exists in languages dict ignore case
        language_name = language_name.lower()
        if language_name in self.languages:
            return self.languages[language_name]
        else:
            return None
    

    def file_belongs_to_language(self, filename, language: Language, extra_filenames:List[str]=[])->bool:
        """
        Checks if a file belongs to a language
        """
        # Get the base name of the file (file name with extension)
        base_name = os.path.basename(filename)
        if not base_name:
            return False
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
    
    def get_supported_languages(self, filename: str, languages: List[str])->List[Language]:  # Renamed from get_supported_langauges
            """
            Checks if a file belongs to a language from a list of languages
            """
            for lang in languages:
                lang = self.get_language_info(lang)
                if lang:
                    if self.file_belongs_to_language(filename, lang):
                        yield lang
    
    def file_belongs_to_group(self, filename, group: str)->bool:
        """
        Checks if a file belongs to a language group (e.g. Shell)

        """
        group_languages = self.get_language_group(group)
        for language in group_languages:
            if self.file_belongs_to_language(filename, language):
                return True
        return False # File does not belong to group
            
