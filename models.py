from pydantic import BaseModel, ConfigDict, Field


class StudentIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    group: str = Field(default="", max_length=20)
