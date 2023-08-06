from globals.paths \
    import \
    set_path_to_library_folder, \
    set_path_to_output_folder,  \
    set_path_to_project_folder, \
    set_path_to_temporary_folder, \
    get_path_to_project_folder, \
    set_path_to_user_directory

from globals.constants \
    import zero


from os \
    import listdir

from os.path \
    import \
    split

from pathlib \
    import Path

from tempfile \
    import TemporaryDirectory


temporary_directories: list = []
project_file_name: str = '__project__.py'


def get_name_of_project_file() -> str:
    global project_file_name
    return project_file_name


def get_temporary_directories() -> list:
    global temporary_directories
    return temporary_directories


def set_temporary_directories(
        value: list
) -> None:
    global temporary_directories
    temporary_directories = value


def search_for_project_recursively(
        current_dir: str
):
    current_location = Path(current_dir)
    found_dirs = listdir(current_dir)

    for f in found_dirs:
        if f == get_name_of_project_file():
            return current_location

    return search_for_project_recursively(
        str(current_location.parent.absolute())
    )


def create_temp_directories():
    tmp_dirs = get_temporary_directories()

    output_folder = TemporaryDirectory()

    tmp_dirs.append(output_folder)
    set_path_to_output_folder(output_folder.name)

    temporary_folder = TemporaryDirectory()

    set_path_to_temporary_folder(temporary_folder.name)
    tmp_dirs.append(temporary_folder)


def search_for_library():
    project_location = Path(get_path_to_project_folder())
    set_path_to_library_folder(
        str(
            project_location.parent
                            .absolute()
        )
    )


def search_for_project():
    current_location = __file__
    current_location = split(current_location)[zero()]

    result = search_for_project_recursively(current_location)
    set_path_to_project_folder(result)


def search_for_user_directory():
    set_path_to_user_directory(
        str(
            Path.home().absolute()
        )
    )


# use
def setup_of_default_variables():
    search_for_project()
    search_for_library()

    search_for_user_directory()
    create_temp_directories()


def clean():
    directories = get_temporary_directories()

    for tmp_dir in directories:
        tmp_dir.cleanup()
