import os
import pathlib


class Project:
    
    TYPE = "base"
    MARKDOWN_FILE_NAME = "README.md"

    @staticmethod
    def run_command(cmd, return_output=False):
        if not return_output:
            return os.system(cmd)
        return os.popen(cmd).read()

    @classmethod
    def get_project_path(cls):
        return f'{str(pathlib.Path(__file__).parent.absolute())}/projects/{cls.TYPE}/'

    @classmethod
    def get_template(cls, file_name):
        if not os.path.exists(f'{cls.get_project_path()}/{file_name}.template'):
            raise Exception(f'The {file_name} template does not exist')
        with open(f'{cls.get_project_path()}/{file_name}.template') as file:
            template = file.read()
            file.close()
            return template

    @classmethod
    def get_formatted_template(cls, file_name, **kwargs):
        return cls.get_template(file_name).format(**kwargs)

    @classmethod
    def create_file_from_template(
            cls,
            file_name,
            template=None,
            **kwargs
        ):
        # set the template to the file name if not exists
        if not template:
            template = file_name
        
        file_content = cls.get_formatted_template(template.split('/').pop(), **kwargs)
        with open(file_name, "w") as file:
            file.write(file_content)
            file.close()
        return True

    @classmethod
    def get_args(cls):
        return {
            # add args
        }

    @classmethod
    def get_packages(cls):
        return []

    @classmethod
    def get_package_command(cls):
        return ""

    @classmethod
    def install_packages(cls):
        cmd = cls.get_package_command()
        if not cmd:
            return
        cls.run_command(
            cmd
        )

    @classmethod
    def get_markdown_lines(cls):
        return [
            '# {project_name}',
            '### By {author}',
            '{description}',
            '--'
        ]

    @classmethod
    def get_markdown_format(cls):
        return "\n".join(cls.get_markdown_lines())

    @classmethod
    def get_markdown(cls, **kwargs):
        return cls.get_markdown_format().format(**kwargs)

    @classmethod
    def get_ignored(cls):
        return [
            # add .gitignore files
        ]

    @classmethod
    def create_files(cls, **kwargs):
        with open(
            cls.MARKDOWN_FILE_NAME,
            "w",
        ) as file:
            file.write(
                cls.get_markdown(
                    **kwargs
                )
            )

    @classmethod
    def run_commands(cls, **kwargs):
        pass
