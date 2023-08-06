# git_ling

git_ling is a small library to detect programming languages from file names and extensions.
It uses the [GitHub linguist](https://github.com/github-linguist/linguist) library to detect languages.

## Installation

```bash
pip install git_ling
```

## Usage

```python
from git_ling import GitLing
git_ling = GitLing()

# Get language info
language = git_ling.get_language_info("Python")
print(language)

# Check if a file belongs to a language
filename = "/path/to/file.py"
print(git_ling.file_belongs_to_language(filename, language.name))
print(git_ling.file_belongs_to_group_id(filename, language.group_id))
```

To use the cli, from bash run: `git_ling --help`.

## Running Tests

```bash
python -m unittest discover -s tests
```

## License

This project is licensed under the terms of the MIT license.
Please see [LICENSE](LICENSE) for more details.
