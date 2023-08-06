# Purpose: Defines the schemas for the data returned by the git_ling API.
from pydantic import BaseModel
from typing import Dict, Optional, List

class Language(BaseModel):
    """
    Represents a programming language.
    """
    name: str  # The name of the language as it should be displayed to users.
    fs_name: Optional[str] = None  # Optional field. Only necessary as a replacement for the sample directory name if the language name is not a valid filename under the Windows filesystem (e.g., if it contains an asterisk).
    language_type: Optional[str] = None  # Either data, programming, markup, prose, or nil
    aliases: Optional[List[str]] = None  # An Array of additional aliases (implicitly includes name.downcase)
    ace_mode: Optional[str] = None  # A String name of the Ace Mode used for highlighting whenever a file is edited. This must match one of the filenames in https://gh.io/acemodes. Use "text" if a mode does not exist.
    codemirror_mode: Optional[str] = None  # A String name of the CodeMirror Mode used for highlighting whenever a file is edited. This must match a mode from https://git.io/vi9Fx
    codemirror_mime_type: Optional[str] = None  # A String name of the file mime type used for highlighting whenever a file is edited. This should match the `mime` associated with the mode from https://git.io/f4SoQ
    wrap: Optional[bool] = None  # Boolean wrap to enable line wrapping (default: false)
    extensions: Optional[List[str]] = None  # An Array of associated extensions (the first one is considered the primary extension, the others should be listed alphabetically)
    filenames: Optional[List[str]] = None  # An Array of filenames commonly associated with the language
    interpreters: Optional[List[str]] = None  # An Array of associated interpreters
    language_id: Optional[int] = None  # Integer used as a language-name-independent indexed field so that we can rename languages in git_ling without reindexing all the code on GitHub. Must not be changed for existing languages without the explicit permission of GitHub staff.
    color: Optional[str] = None  # CSS hex color to represent the language. Only used if type is "programming" or "markup".
    tm_scope: Optional[str] = None  # The TextMate scope that represents this programming language. This should match one of the scopes listed in the grammars.yml file. Use "none" if there is no grammar for this language.
    group: Optional[str] = None  # Name of the parent language. Languages in a group are counted in the statistics as the parent language.

    class Config:
        arbitrary_types_allowed = True

Languages = Dict[str, Language]
Groups = Dict[str, List[Language]]