from .. import Project
import sys
import os


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
    def create_main(cls, **kwargs):
        ok = cls.create_file_from_template('main.py', **kwargs)

    @classmethod
    def create_python_program(cls, **kwargs):
        cls.create_main(**kwargs)

        cls.create_python_package(**kwargs)
    
    @classmethod
    def get_package_files(cls, **kwargs):
        return [
            {
                'file': kwargs.get('project_name') + '.py',
                'template': 'program.py',
                'exports': [
                    kwargs.get('class_name')
                ]
            }
        ]

    @classmethod
    def create_package_files(cls, **kwargs):
        init_file_content = ""
        for file in cls.get_package_files(**kwargs):
            init_file_content += f'from .{file.get("file").replace(".py", "")} import '
            exports = file.get('exports')
            
            if exports == '*':
                init_file_content += '*'
            elif type(exports) is str:
                init_file_content += exports
            elif len(exports) == 1:
                init_file_content += exports[0]
            else:
                init_file_content += "(\n"
                for export in exports:
                    init_file_content += "  " + export
                init_file_content += ")"

            init_file_content += "\n"

            cls.create_file_from_template(
                file_name=file.get('file'),
                template=file.get('template'),
                **kwargs
            )
        # write the init file
        with open('__init__.py', 'w') as file:
            file.write(init_file_content)
            file.close()

    @classmethod
    def create_python_package(cls, **kwargs):
        package = kwargs.get('project_name', 'project')
    
        # make the dir
        if not os.path.exists(package):
            os.mkdir(package)
    
        # go into the dir
        os.chdir(package)
        # create the package files
        cls.create_package_files(**kwargs)

        # exit the package dir
        os.chdir('..')
        return True

    @classmethod
    def run_commands(cls, **kwargs):
        super().run_commands()

        # create venv
        # cls.create_venv()

        # create requirements
        cls.create_requirements()

        # creates the python programs
        cls.create_python_program(**kwargs)


        pass

