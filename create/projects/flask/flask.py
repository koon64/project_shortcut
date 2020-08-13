from .. import PythonProject


class FlaskProject(PythonProject):
    
    TYPE = "flask"

    @classmethod
    def get_packages(cls):
        return super().get_packages() + [
            'Flask==1.1.2'
        ]
