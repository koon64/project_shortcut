from create import ProjectCreater, Project


class ProjectCreaterMock(ProjectCreater):
    def __init__(self, *projects):
        super().__init__(*projects)
