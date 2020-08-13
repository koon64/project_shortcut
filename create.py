import sys
import os
from datetime import datetime
from dotenv import load_dotenv
from github import Github

load_dotenv()

DEFAULT_ARGS = {"description": "", "public": "no", "license": "MIT"}

LICENSES = {
    "MIT": 'Copyright <YEAR> <AUTHOR>\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
}


def create_markdown(display_name, author, description=""):
    """
    Creates the markdown
    """
    # does not create README if already exists
    if os.path.exists("README.md"):
        return False

    markdown = f"# {display_name}\n#### By {author}\n{description}"
    with open("README.md", "w") as f:
        f.write(markdown)
        f.close()
    return True


def create_license(_type, author):
    """
    Creates a license
    """
    # does not create LICENSE if already exists
    if os.path.exists("LICENSE"):
        return False
    # get the given license from type
    license = LICENSES.get(_type)
    if not license:
        raise Exception(_type + " license is not supported")
    # set some vars in the license
    license = license.replace("<YEAR>", str(datetime.now().year))
    license = license.replace("<AUTHOR>", author)
    # create the file
    with open("LICENSE", "w") as f:
        f.write(license)
        f.close()
    return True


def create_directory(directory):
    if os.path.exists(directory):
        return False

    # create the directory
    os.mkdir(directory)
    # change into the directory
    os.chdir(directory)
    print(f'Created the directory "{directory}"')
    return True


def create_repo(repo_name, description="", public=False):
    access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
    return (
        Github(access_token)
        .get_user()
        .create_repo(name=repo_name, description=description, private=not public,)
    )


def initialize_repo(repo_name, description="", public=False):

    repo = create_repo(repo_name=repo_name, description=description, public=public,)
    username = repo.owner.login

    os.system("git init")
    os.system(f"git remote add origin git@github.com:{username}/{repo_name}.git")
    os.system("git add .")
    os.system('git commit -m "Initial Commit"')
    os.system("git push -u origin master")
    return True


def open_editor():
    os.system("code .")


def create(directory, public=False, description="", license="MIT"):
    # create and move into directory if not exist
    create_directory(directory=directory)

    if directory == ".":
        directory = os.getcwd().split("\\").pop()

    # display name for markdown
    display_name = " ".join(
        [word[0].upper() + word[1:].lower() for word in directory.split("_")]
    )

    author = os.getenv("AUTHOR")

    create_markdown(display_name=display_name, author=author, description=description)

    create_license(_type=license, author=author)

    initialize_repo(repo_name=directory, description=description, public=public)

    open_editor()


if __name__ == "__main__":
    cmd_args = sys.argv

    directory = "." if len(cmd_args) < 2 else cmd_args[1]

    args = cmd_args[2:]

    request_args = list(DEFAULT_ARGS.keys())[len(args) :]
    # prompt the user for the
    for arg in request_args:
        default = DEFAULT_ARGS.get(arg)
        value = input(f"{arg} ({default}): ")
        # set to default if not given
        if value == "":
            value = default
        args.append(value)

    description = args[0]
    public = args[1].lower() == "yes"
    license = args[2]

    create(directory=directory, description=description, public=public, license=license)
