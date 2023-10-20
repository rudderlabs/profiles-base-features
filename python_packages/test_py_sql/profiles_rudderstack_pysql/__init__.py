from profiles_rudderstack.project import WhtProject
from .model import SqlTemplateModel

def register_extensions(project: WhtProject):
    project.register_model_type(SqlTemplateModel)
