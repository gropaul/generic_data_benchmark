from src.utils.config import SEARCH_SPACES_DIR
import os


def get_dir_from_name(name: str) -> str:
    name = name.replace(" ", "_").lower()

    # remove all special characters but _ and - from the name
    name = ''.join(e for e in name if e.isalnum() or e == '_' or e == '-')
    return name


def get_search_space_dir(search_space_name: str) -> str:
    return os.path.join(SEARCH_SPACES_DIR, get_dir_from_name(search_space_name))


def get_search_space_results_dir(search_space_name: str) -> str:
    return os.path.join(get_search_space_dir(search_space_name), 'results')


def get_search_space_elements_dir(search_space_name: str) -> str:
    return os.path.join(get_search_space_dir(search_space_name), 'elements')
