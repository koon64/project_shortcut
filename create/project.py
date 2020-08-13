import os
import pathlib
from github import Github


class Project:
    
    TYPE = "base"
    MARKDOWN_FILE_NAME = "README.md"

    @staticmethod
    def run_command(cmd, return_output=False):
        if not return_output:
            return os.system(cmd)
        return os.popen(cmd).read()

    @classmethod
    def run_commands(cls, cmds, return_outputs=False):
        return [cls.run_command(cmd, return_output=return_outputs) for cmd in cmds]

    @classmethod
    def get_project_path(cls):
        return f'{str(pathlib.Path(__file__).parent.absolute())}/projects/'

    @classmethod
    def get_template(cls, template):
        template_path = f'{cls.get_project_path()}{template}.template'
        if not os.path.exists(template_path):
            raise Exception(f'The {template} template does not exist')
        with open(template_path) as file:
            template = file.read()
            file.close()
            return template

    @classmethod
    def get_formatted_template(cls, file_name, **kwargs):
        return cls.get_template(file_name).format(**kwargs)

    @classmethod
    def create_file_from_template(
            cls,
            template,
            file_name=None,
            **kwargs
        ):
        # set the template to the file name if not exists
        if not file_name:
            file_name = template
        
        file_content = cls.get_formatted_template(template, **kwargs)
        with open(file_name.split("/").pop(), "w") as file:
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
    def get_package_command(cls, **kwargs):
        return ""

    @classmethod
    def install_packages(cls, **kwargs):
        cmd = cls.get_package_command(**kwargs)
        if not cmd:
            return
        cls.run_command(
            cmd
        )

    @classmethod
    def get_markdown_lines(cls, **kwargs):
        return [
            '# {display_name}',
            '### By {author}',
            "\n".join(
                [
                    f'[![{shield.get("txt")}]({shield.get("img")})]({shield.get("url")})'
                    for shield in cls.get_shields(**kwargs)
                ]
            ),
            '',
            '{description}',
            '',
            '--'
        ]

    @classmethod
    def get_markdown_format(cls, **kwargs):
        return "\n".join(cls.get_markdown_lines(**kwargs))

    @classmethod
    def get_markdown(cls, **kwargs):
        return cls.get_markdown_format(**kwargs).format(**kwargs)

    @classmethod
    def get_ignored(cls):
        return [
            # add .gitignore files
        ]

    @classmethod
    def create_files(cls, **kwargs):
        # create the markdown
        with open(
            cls.MARKDOWN_FILE_NAME,
            "w",
        ) as file:
            file.write(
                cls.get_markdown(
                    **kwargs
                )
            )
            file.close()
        
        # create the .gitignore
        ignore_content = "\n".join(cls.get_ignored())
        with open('.gitignore', 'w') as file:
            file.write(ignore_content)
            file.close()
    
    @classmethod
    def get_shields(cls, **kwargs):
        return [
            {
                'txt': 'License',
                'img': f'https://img.shields.io/github/license/{kwargs.get("repo_name")}',
                'url': f'https://github.com/{kwargs.get("repo_name")}',
            }
        ]

    @classmethod
    def run_init_commands(cls, **kwargs):
        # TODO: refactor this into the repo_generator??
        pass

    @classmethod
    def create_remote_reop(cls, **kwargs):
        access_token = kwargs.get('github_access_token')
        if not access_token:
            raise Exception('No github access token found')
        github = kwargs.get('github')
        user = kwargs.get('github_user')
        project_name = kwargs.get('project_name')
        repo_name = f'{user.login}/{project_name}'
        repo = github.get_repo(repo_name)
        if repo:
            return repo
        print(f'Creating new repo: {repo_name}')
        return user.create_repo(
            name=project_name,
            description=kwargs.get('description'),
            private=not kwargs.get('public'),
        )

    @classmethod
    def run_closure_commands(cls, **kwargs):
        # TODO: figrure out the flow that is going to be created here
        # TODO: ex: adding methods for branches

        repo = cls.create_remote_reop(**kwargs)


        username = repo.owner.login

        cls.run_commands(
            [
                'git init',
               f'git remote add origin git@github.com:{username}/{kwargs.get("project_name")}.git',
                'git add .',
                'git commit -m "Initial Commit"',
                'git push -u origin master',
                'git branch dev',
                'git push origin dev:dev',
            ]
        )

        return True

