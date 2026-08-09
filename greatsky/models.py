from pydantic import BaseModel, ConfigDict


class Item(BaseModel):
     name: str

     model_config = ConfigDict(extra='forbid')