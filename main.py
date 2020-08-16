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
    # creates the project creater instance

    # TODO: check the types of the projects
    project_creater = ProjectCreater(Project, FlaskProject, PythonProject)

    # print a list of projects if the type is set to "list"
    if directory == "list":
        # import the inspect class, do this for speed?
        import inspect

        projects = project_creater.projects
        if len(projects) == 0:
            print("No projects loaded")
            exit()
        # print projects
        print(
            f'Total of {len(projects)} project type{"s" if len(projects) != 1 else ""}'
        )

        parent_map = {}
        for project in projects:
            parents = list(inspect.getmro(project))
            parents.reverse()
            parents.pop(0)
            last_parent = None
            for parent in parents:
                _type = parent.TYPE
                if _type not in parent_map:
                    parent_map[_type] = []

                if last_parent and _type not in parent_map.get(last_parent):
                    parent_map[last_parent].append(_type)

                last_parent = _type

        base = parent_map.get("base")

        def print_tree(children, depth=0):
            for child in children:
                padding = ""
                for d in range(depth + 2):
                    if d == depth + 1:
                        padding += "- "
                    else:
                        padding += "| "
                print(padding + child)
                print_tree(parent_map.get(child), depth + 1)

        print()
        print("base")
        print_tree(base)
        print()
        exit()

    given_args = cmd_args[3:]

    project_creater.create(directory=directory, _type=_type, args=given_args)
