from ..project import Project
import sys


class PythonProject(Project):

    TYPE = "python"

    @classmethod
    def get_args(cls):
        return {
            **super().get_args(),
        }

    @classmethod
    def get_packages(cls):
        return [
            'requests==2.24.0'
        ]

    @classmethod
    def get_package_command(cls):
        packages = PythonProject.get_packages()
        if not packages:
            return
        return f'pip install {",".join(packages)}'

    @classmethod
    def get_markdown_lines(cls):
        markdown = super().get_markdown_lines()
        return markdown + [
            '## Setup',
            '### Install requirements',
            '`pip install -r requirements.txt`'
        ]

    @classmethod
    def get_ignored(cls):
        return [
            'venv/',
            '__pycache__',
        ] + super().get_ignored()

    @classmethod
    def create_venv(cls):
        cls.run_command("python -m venv ./venv")

    @classmethod
    def create_requirements(cls):
        packages = cls.get_packages()
        packages_file_content = "\n".join(packages)
        with open("requirements.txt", "w") as f:
            f.write(packages_file_content)
            f.close()

    @classmethod
    def run_commands(cls, **kwargs):
        super().run_commands()

        # create venv
        cls.create_venv()

        # create requirements
        cls.create_requirements()



        pass

