from dotenv import load_dotenv
import os
from datetime import datetime
from . import (
    LicenseGenerator,
)
# load the dotenv
load_dotenv()


class ProjectCreater:
    
    # used for defining an undefined arg state
    class Undefined:
        pass

    def __init__(
        self,
        *projects
    ):
        self.projects = projects
    
    def prompt_for_args(
            self,
            args: dict,
            defaults: dict
        ) -> dict:
        '''Prompt the user for fill in Undefined arguments
        
        Arguments
        ---------
            args (dict): User's pregiven args
            defaults (dict): Default values for values not given
        
        Returns
        -------
            dict: Filled in arguments
        
        '''
        for key, val in args.items():
            if val is not self.Undefined:
                continue
            if key not in defaults:
                raise Exception('default not given')
            default = defaults.get(key)
            value = input(f'{key} ({default}): ')
            # set to default if not given
            if value == '':
                value = default
            args[key] = value
        return args

    def get_non_project_specific_args(
        self,
    ):
        return {
            'description': 'My project',
            'public': False,
            'license': 'MIT'
        }

    def create_directory(self, directory):
        if os.path.exists(directory):
            return False
        # create the directory
        os.mkdir(directory)
        return True

    def enter_directory(self, directory):
        # change into the directory
        os.chdir(directory)
        return True

    def create_non_project_specific_files(
        self,
        **kwargs
    ):
        # name the args
        directory = kwargs.get('directory')
        # create the directory
        created = self.create_directory(
            directory
        )
        if created:
            print(f'Created the directory "{directory}"')
        self.enter_directory(
            directory
        )

        # create the license
        ok = LicenseGenerator.create(
            **kwargs
        )
        if not ok:
            return

        
        

    def get_project(self, _type: str):
        return next(filter(lambda proj: proj.TYPE == _type, self.projects), None)

    def get_global_args(self, directory) -> dict:
        # define the project name
        project_name = directory
        # change the proj name if the dir is the current dir
        if project_name == ".":
            project_name = os.getcwd().split("\\").pop()
        # define the display name
        display_name = " ".join([word[0].upper()+word[1:].lower() for word in project_name.split("_")])
        # combine all the args into 1
        # now timestamp
        now = datetime.now()
        return {
            'directory': directory,
            'project_name': project_name,
            'display_name': display_name,
            'class_name': display_name.replace(' ', ''),
            'github_access_token': os.environ.get('GITHUB_ACCESS_TOKEN'),
            'author': os.environ.get('AUTHOR'),
            'year': now.year,
            'month': now.month
        }

    def get_args(self, directory: dict, args: dict, project) -> dict:
        required_non_project_specific_args = self.get_non_project_specific_args()
        required_project_specific_args = project.get_args()
        # combine the req args
        required_args = {
            **required_non_project_specific_args,
            **required_project_specific_args,
        }
        # convert a list of args to a dict of kwargs
        kwargs = {key: (args[i] if i < len(args) else self.Undefined) for i, key in enumerate(required_args.keys())}

        # prompt the user for required args
        args = {
            **self.prompt_for_args(
                args=kwargs,
                defaults=required_args
            ), 
            **self.get_global_args(directory)
        }
        return args

    def create(
        self,
        directory,
        _type="base",
        args=[],
    ):
        # get the project from the type
        project = self.get_project(_type)
        # test if the project exists
        if not project:
            print("Project type not found")
            exit(1)
        # get the args
        kwargs = self.get_args(
            directory=directory,
            args=args,
            project=project
        )

        # create all non-project-specific files
        self.create_non_project_specific_files(
            **kwargs
        )


        # create all project-specific files
        project.create_files(
            **kwargs
        )

        # runs ps commands

        project.run_commands(
            **kwargs
        )

        # runs non-ps commands

        pass

