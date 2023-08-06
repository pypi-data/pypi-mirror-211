import argparse
from .git_ling import GitLing

def create_arg_parser():
    """Creates and returns an ArgumentParser object."""
    parser = argparse.ArgumentParser(description='Detect programming language of a file.')
    parser.add_argument('file_path',
                        help='The path to the file.')
    return parser

def main():
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args()
    file_path = parsed_args.file_path

    # Instantiate git_ling
    linguist = GitLing()

    # Determine the language of the file
    for language_name, language in linguist.languages.items():
        if linguist.file_belongs_to_language(file_path, language):
            print(f'File: {file_path} is supported in {language_name}')
            print(f'Details about the language:')
            print(f'Name: {language.name}')
            print(f'Extensions: {language.extensions}')
            print(f'Group: {language.group}')
            print(f'Aliases: {language.aliases}')
            # print a line break
            print()
            
    if len(linguist.languages) == 0:
        print(f'Could not determine the language of the file: {file_path}')

if __name__ == "__main__":
    main()
