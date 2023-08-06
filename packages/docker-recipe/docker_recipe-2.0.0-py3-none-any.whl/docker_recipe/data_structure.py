import typing
import pydantic


class DockerRecipeImage(pydantic.BaseModel):
    name: str
    Dockerfile: str
    arguments: typing.Dict[str, str] = {}
    depends_on: typing.List[str] = []
    extra_tags: typing.List[str] = []


class DockerRecipe(pydantic.BaseModel):
    images: typing.List[DockerRecipeImage]
