from typing import Tuple
from profiles_rudderstack.material import WhtMaterial
from profiles_rudderstack.model import BaseModelType
from profiles_rudderstack.contract import build_contract, Contract
from profiles_rudderstack.recipe import PyNativeRecipe
from profiles_rudderstack.logger import Logger

class SqlTemplateModel(BaseModelType):
    TypeName = "py_sql_model"
    BuildSpecSchema = {
        "type": "object",
        "properties": {
            "entity_key": {"type": "string"},
        },
        "required": ["entity_key"],
        "additionalProperties": False
    }

    template = """
            {% macro selector_sql() %}
                {% with input_material = this.DeRef("inputs/tbl_a") %}
                    select num from {{input_material}}
                {% endwith %}
            {% endmacro %}
            {% exec %}{{ warehouse.CreateReplaceTableAs(this.Name(), selector_sql()) }}{% endexec %}
        """

    def __init__(self, build_spec: dict, schema_version: int, pb_version: str) -> None:
         super().__init__(build_spec, schema_version, pb_version)

    def get_contract(self) -> Contract:
        return build_contract('{ "is_event_stream": false, "with_columns":[{"name":"num"}] }')
    
    def get_entity_key(self):
        return self.build_spec.get("entity_key")
    
    def get_material_recipe(self) -> PyNativeRecipe:
        return SqlTemplateRecipe(self.template)
    
    def validate(self):
        return super().validate()


class SqlTemplateRecipe(PyNativeRecipe):
    def __init__(self, template: str):
        self.template = template
        self.text = ""
        self.logger = Logger("SqlTemplateRecipe")

    def describe(self, this: WhtMaterial) -> Tuple[str, str]:
        return self.text, ".sql"
    
    def prepare(self, this: WhtMaterial):
        text = this.execute_text_template(self.template)
        self.text = text

    def execute(self, this: WhtMaterial):
        this.wht_ctx.client.query_sql_without_result(self.text)
        
