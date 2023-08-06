path_to_project_folder: None | str = None
path_to_library_folder: None | str = None

path_to_temporary_folder: None | str = None
path_to_output_folder: None | str = None

path_to_user_directory: None | str = None


# Accessors
# * Getters
def get_path_to_project_folder() -> None | str:
    global path_to_project_folder
    return path_to_project_folder


def get_path_to_output_folder() -> None | str:
    global path_to_output_folder
    return path_to_output_folder


def get_path_to_library_folder() -> None | str:
    global path_to_library_folder
    return path_to_library_folder


def get_path_to_temporary_folder() -> None | str:
    global path_to_temporary_folder
    return path_to_temporary_folder


def get_path_to_user_directory() -> None | str:
    global  path_to_user_directory
    return path_to_user_directory


# * Setters
def set_path_to_project_folder(
        value: str
) -> None:
    global path_to_project_folder
    path_to_project_folder = value


def set_path_to_output_folder(
        value: str
) -> None:
    global path_to_output_folder
    path_to_output_folder = value


def set_path_to_library_folder(
        value: str
) -> None:
    global path_to_library_folder
    path_to_library_folder = value


def set_path_to_temporary_folder(
        value: str
) -> None:
    global path_to_temporary_folder
    path_to_temporary_folder = value


def set_path_to_user_directory(
        value: str
) -> None:
    global path_to_user_directory
    path_to_user_directory = value

