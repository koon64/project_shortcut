import os


class Project:
    
    TYPE = "base"
    MARKDOWN_FILE_NAME = "README.md"

    @staticmethod
    def run_command(cmd, return_output=False):
        if not return_output:
            return os.system(cmd)
        return os.popen(cmd).read()

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
