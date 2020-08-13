from .. import Project
import sys
import os


class PythonProject(Project):

    TYPE = "python"

    PYTHON_FORMAT_MAP = {
        "black": {
            "package": "black==19.10b0",
            "shield": {
                "img": "https://camo.githubusercontent.com/28a51fe3a2c05048d8ca8ecd039d6b1619037326/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667",
                "txt": "Format",
                "url": "https://github.com/psf/black",
            },
        }
    }

    @classmethod
    def get_args(cls):
        return {**super().get_args(), **{"formatter": "black"}}

    @classmethod
    def get_packages(cls, **kwargs):
        packages = ["requests==2.24.0", "pytest==6.0.1"]
        formatter = kwargs.get("formatter")
        if not formatter:
            return packages
        # get the formatter package
        formatter_package = cls.PYTHON_FORMAT_MAP.get(formatter)
        if not formatter_package:
            print(f"{formatter} formatter badge does not exist")
        else:
            packages.append(formatter_package.get("package"))
        return packages

    @classmethod
    def get_shields(cls, **kwargs):
        shields = super().get_shields(**kwargs)
        formatter = kwargs.get("formatter")
        if not formatter:
            return shields
        # get the formatter package
        formatter_package = cls.PYTHON_FORMAT_MAP.get(formatter)
        if not formatter_package:
            print(f"{formatter} formatter does not exist, not using formatter")
        return shields + [formatter_package.get("shield")]

    @classmethod
    def get_package_command(cls, **kwargs):
        packages = PythonProject.get_packages(**kwargs)
        if not packages:
            return
        return f'pip install {",".join(packages)}'

    @classmethod
    def get_markdown_lines(cls, **kwargs):
        markdown = super().get_markdown_lines(**kwargs)
        return markdown + [
            "## Setup",
            "### Install requirements",
            "`pip install -r requirements.txt`",
        ]

    @classmethod
    def get_ignored(cls):
        return ["venv/", "__pycache__",] + super().get_ignored()

    @classmethod
    def create_venv(cls):
        cls.run_command("python -m venv ./venv")

    @classmethod
    def create_requirements(cls, **kwargs):
        packages = cls.get_packages(**kwargs)
        packages_file_content = "\n".join(packages)
        with open("requirements.txt", "w") as f:
            f.write(packages_file_content)
            f.close()

    @classmethod
    def create_main(cls, **kwargs):
        ok = cls.create_file_from_template("python/main.py", **kwargs)

    @classmethod
    def create_python_program(cls, **kwargs):
        cls.create_main(**kwargs)

        cls.create_python_package(**kwargs)

    @classmethod
    def get_package_files(cls, **kwargs):
        return [
            {
                "file": kwargs.get("project_name") + ".py",
                "template": "python/program.py",
                "exports": [kwargs.get("class_name")],
            }
        ]

    @classmethod
    def create_package_files(cls, **kwargs):
        init_file_content = ""
        for file in cls.get_package_files(**kwargs):
            init_file_content += f'from .{file.get("file").replace(".py", "")} import '
            exports = file.get("exports")

            if exports == "*":
                init_file_content += "*"
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
                file_name=file.get("file"), template=file.get("template"), **kwargs
            )
        # write the init file
        with open("__init__.py", "w") as file:
            file.write(init_file_content)
            file.close()

    @classmethod
    def create_python_package(cls, **kwargs):
        package = kwargs.get("project_name", "project")

        # make the dir
        if not os.path.exists(package):
            os.mkdir(package)

        # go into the dir
        os.chdir(package)
        # create the package files
        cls.create_package_files(**kwargs)

        # exit the package dir
        os.chdir("..")
        return True

    @classmethod
    def run_init_commands(cls, **kwargs):
        super().run_init_commands()

        # create venv
        cls.create_venv()

        # create requirements
        cls.create_requirements(**kwargs)

        # creates the python programs
        cls.create_python_program(**kwargs)
