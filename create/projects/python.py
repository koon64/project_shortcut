from ..project import Project
import sys


class PythonProject(Project):

    TYPE = "python"

    @classmethod
    def get_args(cls):
        return {
            **super().get_args(),
            **{
                'python_version': 3.7
            }
        }

    @classmethod
    def get_packages(cls):
        return [
            'requests'
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
    def in_venv(cls):
        result = cls.run_command("pip -V", return_output=True)
        return '\\venv\\lib' not in result or '/venv/lib' not in result

    @classmethod
    def deactivate_current_venv(cls):
        if not cls.in_venv():
            return

        if sys.platform == "win32":
            print('wahte hte fic')
            cls.run_command("venv\\Scripts\\deactivate")
            return
        
        cls.run_command("deactivate")

    @classmethod
    def activate_venv(cls):
        cls.deactivate_current_venv()

        cls.run_command("pip freeze")

        exit()

        if sys.platform == "win32":
            cls.run_command("venv\\Scripts\\activate")
            return
        
        cls.run_command("source venv/Scripts/activate")

    @classmethod
    def create_requirements(cls):
        cls.run_command("pip freeze > requirements.txt")

    @classmethod
    def run_commands(cls, **kwargs):
        super().run_commands()

        # create venv
        cls.create_venv()

        # activate
        cls.activate_venv()

        # install requirements
        cls.install_packages()

        # create requirements
        cls.create_requirements()

        pass

