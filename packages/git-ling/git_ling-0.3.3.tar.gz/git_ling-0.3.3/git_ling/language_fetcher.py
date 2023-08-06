"""
The file stores the YAML file in a local cache and returns the content of the file as a dictionary.
"""
import logging
import os
import urllib.request
from datetime import datetime, timedelta

import yaml
logger = logging.getLogger(__name__)
CACHE_FILE = "languages.yml"
CACHE_MAX_AGE = timedelta(days=30)  # Change this to set the cache validity

def fetch_languages():
    if not os.path.exists(CACHE_FILE):
        update_cache()
    elif datetime.now() - datetime.fromtimestamp(os.path.getmtime(CACHE_FILE)) > CACHE_MAX_AGE:
        update_cache()

    with open(CACHE_FILE, 'r') as f:
        content = f.read()
        try:
            content = yaml.safe_load(content)
            logger.debug("Successfully parsed YAML file")
            return content
        except yaml.YAMLError as e:
            logger.error("Error while parsing YAML file: %s", e)
            return {}

def update_cache():
    url = 'https://raw.githubusercontent.com/github-linguist/linguist/master/lib/linguist/languages.yml'
    result=urllib.request.urlretrieve(url, CACHE_FILE)
    # Check if file was downloaded successfully
    if result[0] == CACHE_FILE:
        logger.info("Successfully updated cache")
if __name__ == "__main__":
    # Pretty print the result
    import json
    result=fetch_languages()
    print(json.dumps(result, indent=4, sort_keys=True))