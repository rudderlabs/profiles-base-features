from profiles_rudderstack.model import BaseModelType
from profiles_rudderstack.contract import build_contract
from profiles_rudderstack.recipe import PyNativeRecipe
from profiles_rudderstack.material import WhtMaterial
from profiles_rudderstack.logger import Logger
from typing import List
import pandas as pd


class NewCommonColumnUnionModel(BaseModelType):
    TypeName = "common_column_union_new"
    BuildSpecSchema = {
        "type": "object",
        "properties": {
            "inputs": { "type": "array", "items": { "type": "string" } },            
        },
        "required": ["inputs"],
        "additionalProperties": False
    }

    def __init__(self, build_spec: dict, schema_version: int, pb_version: str) -> None:
        super().__init__(build_spec, schema_version, pb_version)

    #  Specify the output contract for the model (optional)
    # def get_contract(self) -> Contract:
    #     return build_contract('{ "is_event_stream": false, "with_columns":[{"name":"num"}] }')
    
    #  Specify the entity key for the model (optional)
    # def get_entity_key(self):
    #     return self.build_spec.get("entity_key") # getting it from model spec
    #     or
    #     return "entity_key"
    
    def get_material_recipe(self)-> PyNativeRecipe:
        return NewCommonColumnUnionRecipe(self.build_spec["inputs"])

    def validate(self):
        # Model Validate
        if self.build_spec.get("inputs") is None or len(self.build_spec["inputs"]) == 0:
            return False, "inputs are required"
        
        return super().validate()


class NewCommonColumnUnionRecipe(PyNativeRecipe):
    def __init__(self, inputs: List[str]) -> None:
        self.inputs = inputs
        self.logger = Logger("CommonColumnUnionRecipe")

    def describe(self, this: WhtMaterial):
        material_name = this.name()
        return f"""Material - {material_name}\nInputs: {self.inputs}""", ".txt"

    def prepare(self, this: WhtMaterial):
        for in_model in self.inputs:
            contract = build_contract('{ "is_event_stream": true, "with_columns":[{"name":"num"}] }')
            this.de_ref(in_model, contract)

    def execute(self, this: WhtMaterial):
        self.logger.info("Executing CommonColumnUnionRecipe:New")
        tables : List[pd.DataFrame] = []
        for in_model in self.inputs:
            input_material = this.de_ref(in_model)
            df = input_material.get_table_data()
            tables.append(df)

            # read data in batches, only supported in case of snowflake currently
            # dfIter = input_material.get_table_data_batches()
            # for batch in dfIter:
            #     self.logger.info("Batch: {0}".format(batch))

            # Get model's entity, entity will be none if no entity_key is provided
            # entity = input_material.entity()
            # if entity is not None:
            #     name = entity.get("Name")
            #     id_types = entity.get("IdTypes")
            #     main_id_type = entity.get("MainIdType")
            #     id_column_name = entity.get("IdColumnName")

            # If you want to get only the columns that are required, you can use the following code
            # df = input_material.get_table_data(select_columns=["num"])

            # you can also query with result using
            # df = this.wht_ctx.client.query_sql_with_result("select num as col1 from {0}".format(input_material.name()))
        # Get output folder path
        # folder = this.get_output_folder()
        
        merged_df = pd.concat(tables, join="inner")
        this.write_output(merged_df)
        self.logger.info("Finished executing CommonColumnUnionRecipe:New")

        
