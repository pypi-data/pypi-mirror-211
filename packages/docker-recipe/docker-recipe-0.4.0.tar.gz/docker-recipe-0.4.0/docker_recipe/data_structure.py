import typing
import pydantic


class DockerRecipeImage(pydantic.BaseModel):
    name: str
    Dockerfile: str
    latest: bool = False
    arguments: typing.Dict[str, str] = {}
    depends_on: typing.List[str] = []


class DockerRecipe(pydantic.BaseModel):
    images: typing.List[DockerRecipeImage]
