import sys
from create import (
    ProjectCreater,
    Project,
)
from create.projects import (
    PythonProject,
    FlaskProject,
    # add other projects here
)

if __name__ == "__main__":
    cmd_args = sys.argv

    directory = "." if len(cmd_args) < 2 else cmd_args[1]
    _type = "base" if len(cmd_args) < 3 else cmd_args[2]

    given_args = cmd_args[3:]

    project_creater = ProjectCreater(Project, PythonProject, FlaskProject,)

    project_creater.create(directory=directory, _type=_type, args=given_args)
