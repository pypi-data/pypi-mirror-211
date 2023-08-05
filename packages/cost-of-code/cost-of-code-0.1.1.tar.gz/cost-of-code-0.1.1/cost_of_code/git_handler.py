import difflib
import os
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

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
        for diff in diffs.iter_change_type("M"):
            if any(diff.a_path.endswith(ext) for ext in extension_whitelist):
                # Get the content of the file before and after the changes
                a_data = diff.a_blob.data_stream.read().decode()
                b_data = diff.b_blob.data_stream.read().decode()

                # Generate the diff using difflib.unified_diff
                diff_lines = difflib.unified_diff(
                    a_data.splitlines(), b_data.splitlines()
                )

                # Extract the added lines
                for line in diff_lines:
                    if line.startswith("+") and not line.startswith("+++"):
                        added_lines.append(line[1:])

    return added_lines


def get_code_files(directory, extension_whitelist):
    try:
        repo = Repo(directory)
    except InvalidGitRepositoryError:
        print("Error: The provided directory is not a git repository.")
        exit(1)

    matches = []

    # Read .gitignore file and create a PathSpec (pattern)
    with open(os.path.join(directory, ".gitignore"), "r") as f:
        gitignore = f.read()
    pathspec = PathSpec.from_lines(GitWildMatchPattern, gitignore.splitlines())

    # Get all files in the current commit
    files = [
        item.path for item in repo.head.commit.tree.traverse() if item.type == "blob"
    ]

    # Filter files by extension and by whether they are ignored
    for file in files:
        filename = os.path.basename(file)
        relpath = os.path.relpath(file, directory)
        if any(filename.endswith(ext) for ext in extension_whitelist):
            if not pathspec.match_file(relpath):
                matches.append(relpath)

    return matches
