import pydantic


class BaseModel(pydantic.BaseModel):
    """Class to represent the database model."""

    def __str__(self) -> str:
        return self.json()
