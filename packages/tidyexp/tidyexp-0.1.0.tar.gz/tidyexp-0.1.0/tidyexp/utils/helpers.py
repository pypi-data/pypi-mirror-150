import h5py
import pygit2
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import numpy as np
import pickle
import os
import glob
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload


def save_hdf5(name, path, data):
    """
    Saves data to a .hdf5 file.

    :param name: File name
    :param path: Path where the file is saved
    :param data: Data to save
    """

    try:
        hdf5 = h5py.File(name, "a")
        hdf5.create_dataset(name=path, data=data)
        hdf5.flush()
        hdf5.close()
    except ValueError:
        print("File already exists!")


def upload_gdrive(credential_path, folder_name, archive_name):
    """
    Helper function to upload data to Google Drive.

    :param credential_path: Google Drive credentials
    :param folder_name: Folder name
    :param archive_name: Archive name/path
    """

    # authenticate account
    service = get_gdrive_service(credential_path)

    if service == "":
        raise Exception("couldn't get Google Drive service.")

    if folder_name == "" or archive_name == "":
        raise Exception("folder name or archive name wasn't provided.")

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }

    # create the folder
    file = service.files().create(body=folder_metadata, fields="id").execute()
    folder_id = file.get("id")

    # upload file
    file_metadata = {"name": archive_name, "parents": [folder_id]}
    media = MediaFileUpload(archive_name, resumable=True)
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )


def commit(git_path, folder_path):
    """
    Commits experiment data to a git repository.

    :param git_path: Git repo path
    :param folder_path: Folder path
    """

    file_names = glob.glob(folder_path + "/**/*.*", recursive=True)

    # handle init
    try:
        repo = pygit2.Repository(git_path + "/.git")
        print("Loaded original:", repo)
    except pygit2.GitError:
        repo = pygit2.init_repository(git_path, False)
        print("Made a new repo:", repo)

    # add file
    index = repo.index
    for file in file_names:
        index.add(file)
    index.write()

    # commit
    author = pygit2.Signature("Tidyexp", "tidyexp@example.com")
    committer = pygit2.Signature("Tidyexp", "tidyexp@example.com")

    now = datetime.now()
    message = "Experiment update (" + now.strftime("%m/%d/%Y, %H:%M:%S") + ")"
    tree = index.write_tree()

    try:
        ref = "HEAD"
        parents = []
        repo.create_commit(ref, author, committer, message, tree, parents)
    except pygit2.GitError:
        ref = repo.head.name
        parents = [repo.head.target]
        repo.create_commit(ref, author, committer, message, tree, parents)


def plot(time, stats, x, y, return_fig=False, format_str="rx-"):
    try:
        import matplotlib.pyplot as plt

        # validate
        if x not in time.keys():
            raise Exception(f"{x} not found in time data.")
        if y not in stats.keys():
            raise Exception(f"{y} not found in stats data.")

        # plot
        fig, ax = plt.subplots()
        ax.plot(time[x], stats[y], format_str)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f"{x} vs {y}")
        if return_fig:
            return fig, ax
        plt.show()
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "matplotlib is not installed. Please install `matplotlib` to plot stats."
        )


def print_about():

    """
    Prints welcome message on calling Logger()
    """

    welcome = r"""
_    _
| \/ |
|    |
    """.splitlines()

    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="right")
    grid.add_row(welcome[0], "Tidyexp")
    grid.add_row(
        welcome[1],
        "Manage ML experiments easily :grin:",
    )
    grid.add_row(welcome[2], f"Made By: Aman, Aadhav, Animesh")
    panel = Panel(grid, expand=True)
    Console(width=80).print(panel)


def print_update(time_headers, stats_headers, time_dict, stats_dict):

    """
    Prints stats when log.update() is called
    """

    table = Table(show_header=True)

    for _, c_label in enumerate(time_headers):
        table.add_column(c_label, style="red")

    for _, c_label in enumerate(stats_headers):
        table.add_column(c_label)

    row_list = [str(time_dict[c]) for c in time_headers] + [
        str(np.round_(stats_dict[s], 3)) for s in stats_headers
    ]

    table.add_row(*row_list)

    Console(width=80).print(table, justify="center")


SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.file",
]


def get_gdrive_service(credential_path):
    # validate
    if credential_path == "":
        return ""

    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("drive", "v3", credentials=creds)
