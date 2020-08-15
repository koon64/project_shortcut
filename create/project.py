import os
import pathlib
from github import Github


class Project:

    TYPE = "base"
    MARKDOWN_FILE_NAME = "README.md"

    @staticmethod
    def run_command(cmd: str, return_output: bool = False) -> str:
        """Run a system command

        Arguments
        ---------
            cmd (str): String of the OS command
            return_output (bool)=False: True to return the output of the command as a string

        Returns
        -------
            str: String of a command's output

        """
        if not return_output:
            return os.system(cmd)
        return os.popen(cmd).read()

    @classmethod
    def run_commands(cls, cmds: list, return_outputs: bool = False) -> list:
        """Runs a list of commands
        
        Arguments
        ---------
            cmds (list[str]): List of commands to run
            return_outputs (bool=False): True to return the output of the commands as a list of strings

        Returns
        -------
            list[str]: List of strings which are the outputs of the commands run

        """
        return [cls.run_command(cmd, return_output=return_outputs) for cmd in cmds]

    @classmethod
    def get_project_path(cls) -> str:
        """Returns an absolute project path

        Returns
        -------
            str: Project path
        
        """
        return f"{str(pathlib.Path(__file__).parent.absolute())}/projects/"

    @classmethod
    def get_template(cls, template: str) -> str:
        """Returns the template from a template path
        
        Arguments
        ---------
            template (str): Template path. ex: base/README.md

        Returns
        -------
            str: The content of the template

        """
        template_path = f"{cls.get_project_path()}{template}.template"
        if not os.path.exists(template_path):
            raise Exception(f"The {template} template does not exist")
        with open(template_path) as file:
            template = file.read()
            file.close()
            return template

    @classmethod
    def get_formatted_template(cls, file_name: str, **kwargs) -> str:
        """Formats a template from a template path

        Arguments
        ---------
            file_name (str): Template path. ex: base/README.md
            **kwargs: Arguments

        Returns
        -------
            str: Formatted template
        """
        return cls.get_template(file_name).format(**kwargs)

    @classmethod
    def create_file_from_template(
        cls, template: str, file_name: str = None, **kwargs
    ) -> bool:
        """Writes a formatted template to a given path

        Arguments
        ---------
            template (str): Template path. ex: base/README.md
            file_name (str=None): File to be written in the project. ex: "README.md"
            **kwargs: Arguments

        Returns
        -------
            bool: True if it was successful, False if not

        """
        # set the template to the file name if not exists
        if not file_name:
            file_name = template
        file_content = cls.get_formatted_template(template, **kwargs)
        # make sure the path to the file_name exists
        dir_name = os.path.dirname(file_name)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        # create the file
        with open(file_name, "w") as file:
            file.write(file_content)
            file.close()
        return True

    @classmethod
    def get_args(cls) -> dict:
        """Returns a merged dict of args to get a the start of the project generation

        Returns
        -------
            dict: Arguments to get

        """
        return {
            # add args
        }

    @classmethod
    def get_packages(cls) -> list:
        """Returns a merged list of packages to be interpreted 

        Returns
        -------
            list: Packages list

        """
        return []

    @classmethod
    def get_package_command(cls, **kwargs) -> str:
        """Returns the (install?) package command
        
        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            str: Package install command

        """
        return ""

    @classmethod
    def install_packages(cls, **kwargs) -> bool:
        """Installs the packages

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            bool: True if installed, False if any errors

        """
        cmd = cls.get_package_command(**kwargs)
        if not cmd:
            return False
        cls.run_command(cmd)
        return True

    @classmethod
    def get_markdown_lines(cls, **kwargs) -> list:
        """Returns a list of markdown lines

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            list[str]: Markdown lines

        """
        return [
            "# {display_name}",
            "### By {author}",
            "\n".join(
                [
                    f'[![{shield.get("txt")}]({shield.get("img")})]({shield.get("url")})'
                    for shield in cls.get_shields(**kwargs)
                ]
            ),
            "",
            "{description}",
            "",
            "--",
        ]

    @classmethod
    def get_markdown_format(cls, **kwargs) -> str:
        """Returns a merged markdown format

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            str: Markdown format

        """
        return "\n".join(cls.get_markdown_lines(**kwargs))

    @classmethod
    def get_markdown(cls, **kwargs) -> str:
        """Returns a formatted markdown string
        
        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            str: Markdown content

        """
        return cls.get_markdown_format(**kwargs).format(**kwargs)

    @classmethod
    def get_ignored(cls) -> list:
        """Get ignored files and folders to be used for .gitignore, dockerignore(?), etc

        Returns
        -------
            list: Ignored files and folders

        """
        return [
            # add .gitignore files
        ]

    @classmethod
    def create_files(cls, **kwargs) -> bool:
        """Creates a projects files

        The base project should not be overriden and this method should be called first.
        The base project creates two files

        1. README.md  -  project readme
        2. .gitignore -  github ignore file

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            bool: True if successful, False if any errors

        """

        # create the markdown
        with open(cls.MARKDOWN_FILE_NAME, "w",) as file:
            file.write(cls.get_markdown(**kwargs))
            file.close()

        # create the .gitignore
        ignore_content = "\n".join(cls.get_ignored())
        with open(".gitignore", "w") as file:
            file.write(ignore_content)
            file.close()

        return True

    @classmethod
    def get_shields(cls, **kwargs) -> list:
        """Get the README's shields

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            list[dict{"txt": str, "url": str, "img": str}]: List of shield dicts

        """
        return [
            {
                "txt": "License",
                "img": f'https://img.shields.io/github/license/{kwargs.get("repo_name")}',
                "url": f'https://github.com/{kwargs.get("repo_name")}',
            }
        ]

    @classmethod
    def get_github_templates(cls, **kwargs) -> dict:
        """Gets github templates
        
        This is only created for public projects
        TODO: add a change for this to be toggled in the config.yml

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            dict: Github templates. the key is the file to be created, the val is the template

        """
        return {
            "SECURITY": "base/SECURITY.md",
            "PULL_REQUEST_TEMPLATE": "base/PULL_REQUEST_TEMPLATE.md",
            "CODE_OF_CONDUCT": "base/CODE_OF_CONDUCT.md",
            "ISSUE_TEMPLATE/bug_report": "base/ISSUE_TEMPLATE/bug_report.md",
        }

    @classmethod
    def create_github_templates(cls, **kwargs) -> bool:
        """Creates the github templates

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            bool: True for success, False for errors

        """
        if not kwargs.get("public"):
            return
        templates = cls.get_github_templates(**kwargs)
        for name, template in templates.items():
            file_name = f"{name}.md"
            cls.create_file_from_template(
                template=template, file_name=file_name, **kwargs
            )
        return True

    @classmethod
    def get_github_workflows(cls, **kwargs) -> list:
        # TODO: implement this
        pass

    @classmethod
    def create_github_workflows(cls, **kwargs) -> bool:
        """Create github workflows
        
        This will create the workflows directory in the .github directory
        This will only happen if there are workflows to be created

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            bool: True for success, False for errors

        """
        workflows = cls.get_github_workflows(**kwargs)
        if not workflows:
            return False
        # create the workflows directory
        if not os.path.exists("workflows/"):
            os.mkdir("workflows")
        # change into the workflows dir
        os.chdir("workflows")
        # create the workflow
        cls.create_github_workflows(**kwargs)
        # exit the workflows dir
        os.chdir("..")
        return True

    @classmethod
    def create_github_files(cls, **kwargs) -> bool:
        """Create the github files
        
        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            bool: True for success, False for errors

        """
        # try to create the github folder
        if not os.path.exists(".github/"):
            os.mkdir(".github")
        # change into the .github folder
        os.chdir(".github")
        # create the github templates
        cls.create_github_templates(**kwargs)
        # create the workflows
        cls.create_github_workflows(**kwargs)
        # exit the .github dir
        os.chdir("..")

    @classmethod
    def run_init_commands(cls, **kwargs) -> bool:
        """Run initialization commands

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            bool: True for success, False for errors

        """
        # create the github files
        cls.create_github_files(**kwargs)

        # TODO: refactor this into the repo_generator??
        pass

    @classmethod
    def create_remote_reop(cls, **kwargs) -> object:
        """Creates a remote repository

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            Repository: Github repo object (see their docs)
        """
        # TODO: link github repo doc in doc

        access_token = kwargs.get("github_access_token")
        if not access_token:
            raise Exception("No github access token found")
        github = kwargs.get("github")
        user = kwargs.get("github_user")
        project_name = kwargs.get("project_name")
        repo_name = f"{user.login}/{project_name}"
        repo = github.get_repo(repo_name)
        if repo:
            return repo
        print(f"Creating new repo: {repo_name}")
        return user.create_repo(
            name=project_name,
            description=kwargs.get("description"),
            private=not kwargs.get("public"),
        )

    @classmethod
    def run_closure_commands(cls, **kwargs) -> bool:
        """Runs the finishing commands

        Arguments
        ---------
            **kwargs: Arguments

        Returns
        -------
            bool: True for success, False for errors

        """
        # TODO: figrure out the flow that is going to be created here
        # TODO: ex: adding methods for branches

        repo = cls.create_remote_reop(**kwargs)

        username = repo.owner.login

        cls.run_commands(
            [
                "git init",
                f'git remote add origin git@github.com:{username}/{kwargs.get("project_name")}.git',
                "git add .",
                'git commit -m "Initial Commit"',
                "git push -u origin master",
                "git branch dev",
                "git push origin dev:dev",
            ]
        )

        return True
