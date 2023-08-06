import os
import json
import shutil
import tarfile
import jupytext
from os import devnull
from zipfile import ZipFile
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from .notebook import read_nb, tag_code_cells


@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, "w") as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


def tag_notebook(path) -> None:
    """Adds 'graded' tag to all code cells of a notebook.

    Args:
        path (str): Path to the notebook.
    """
    nb = read_nb(path)
    nb = tag_code_cells(nb)
    jupytext.write(nb, path)


def extract_tar(file_path: str, destination: str, post_cleanup: bool = True) -> None:
    """Extracts a tar file unto the desired destination.

    Args:
        file_path (str): Path to tar file.
        destination (str): Path where to save uncompressed files.
        post_cleanup (bool, optional): If true, deletes the compressed tar file. Defaults to True.
    """
    with tarfile.open(file_path, "r") as my_tar:
        my_tar.extractall(destination)

    if post_cleanup and os.path.exists(file_path):
        os.remove(file_path)


def extract_zip(file_path, destination, post_cleanup: bool = True) -> None:
    """Extracts a zip file unto the desired destination.

    Args:
        file_path (str): Path to zip file.
        destination (str): Path where to save uncompressed files.
        post_cleanup (bool, optional): If true, deletes the compressed zip file. Defaults to True.
    """
    with ZipFile(file_path, "r") as zip:
        zip.extractall(destination)

    if post_cleanup and os.path.exists(file_path):
        os.remove(file_path)


def send_feedback(
    score: float,
    msg: str,
    feedback_path: str = "/shared/feedback.json",
    err: bool = False,
) -> None:
    """Sends feedback to the learner.
    Args:
        score (float): Grading score to show on Coursera for the assignment.
        msg (str): Message providing additional feedback.
        feedback_path (str): Path where the json feedback will be saved. Defaults to /shared/feedback.json
        err (bool, optional): True if there was an error while grading. Defaults to False.
    """

    post = {"fractionalScore": score, "feedback": msg}
    print(json.dumps(post))

    with open(feedback_path, "w") as outfile:
        json.dump(post, outfile)

    if err:
        exit(1)

    exit(0)


def copy_submission_to_workdir(
    dir_origin: str = "/shared/submission/",
    dir_destination: str = "./submission/",
    file_name: str = "submission.ipynb",
) -> None:
    """Copies submission file from bind mount directory into working directory.
    Args:
        dir_origin (str): Origin directory.
        dir_destination (str): Target directory.
        file_name (str): Name of the file.
    """

    file_initial_path = os.path.join(dir_origin, file_name)
    file_final_path = os.path.join(dir_destination, file_name)

    shutil.copyfile(file_initial_path, file_final_path)
