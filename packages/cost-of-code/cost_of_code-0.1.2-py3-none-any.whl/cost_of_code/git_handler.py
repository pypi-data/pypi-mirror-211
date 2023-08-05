import difflib
from pathlib import Path

from git import GitCommandError, Repo, InvalidGitRepositoryError


def get_added_lines(directory, extension_whitelist, branch_name):
    try:
        repo = Repo(directory)
    except InvalidGitRepositoryError:
        print("Error: The provided directory is not a git repository.")
        exit(1)

    if repo.is_dirty():
        print("Error: There are uncommitted changes in the repository.")
        exit(1)

    added_lines = []

    # getting commits in chronological order
    try:
        # getting commits in chronological order
        commits = list(repo.iter_commits(branch_name))[::-1]
    except GitCommandError:
        print(f"Error: The branch '{branch_name}' does not exist in the repository.")
        exit(1)

    # Handle the initial commit separately
    initial_commit = commits.pop(0)
    for item in initial_commit.tree.traverse():
        if item.type == "blob" and any(
            item.path.endswith(ext) for ext in extension_whitelist
        ):
            added_lines.extend(item.data_stream.read().decode().splitlines())

    for i in range(len(commits) - 1):
        diffs = commits[i].diff(commits[i + 1])
        for diff in diffs.iter_change_type("A"):
            if diff.a_blob is None:  # The file was created in this commit
                added_lines.extend(diff.b_blob.data_stream.read().decode().splitlines())
        for diff in diffs.iter_change_type("M"):
            if any(diff.a_path.endswith(ext) for ext in extension_whitelist):
                a_data = diff.a_blob.data_stream.read().decode() if diff.a_blob else ""
                b_data = diff.b_blob.data_stream.read().decode() if diff.b_blob else ""

                # Generate the diff using difflib.unified_diff
                diff_lines = difflib.unified_diff(
                    a_data.splitlines(), b_data.splitlines()
                )

                # Extract the added lines
                for line in diff_lines:
                    if line.startswith("+") and not line.startswith("+++"):
                        added_lines.append(line[1:])

    return added_lines


def get_current_lines(directory, extension_whitelist):
    lines_of_code = []

    try:
        repo = Repo(directory)
    except InvalidGitRepositoryError:
        print("Error: The provided directory is not a git repository.")
        exit(1)

    # Get a list of all files in the repository
    files_in_repo = repo.git.ls_files().splitlines()

    # Filter the list of files based on the extension whitelist
    files_to_check = [
        file
        for file in files_in_repo
        if any(file.endswith(ext) for ext in extension_whitelist)
    ]

    # For each file, read its content and split it into lines
    for file_path in files_to_check:
        with open(Path(directory) / file_path, "r") as file:
            lines_of_code.extend(file.readlines())

    return lines_of_code
