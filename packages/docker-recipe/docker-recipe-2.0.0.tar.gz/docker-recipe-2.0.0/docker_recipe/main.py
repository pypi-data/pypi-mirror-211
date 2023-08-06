import os

import jinja2
import yaml

from docker_recipe.cli import parser
from docker_recipe.data_structure import DockerRecipe
from docker_recipe.filters import filter_basename, filter_dirname


def load_recipe(path: str) -> DockerRecipe:
    with open(path) as f_recipe:
        config_contents = f_recipe.read()

    return DockerRecipe(**yaml.load(config_contents, Loader=yaml.FullLoader))


def render_file(path: str, recipe: DockerRecipe) -> str:
    fsl = jinja2.FileSystemLoader(os.path.dirname(path))
    env = jinja2.Environment(loader=fsl)
    env.filters['basename'] = filter_basename
    env.filters['dirname'] = filter_dirname
    tpl = env.get_template(os.path.basename(path))
    output = tpl.render({"recipe": recipe})

    return output if output.endswith("\n") else output + "\n"


def main():
    args = parser.parse_args()

    with open(args.output, 'w+') as f_gitlab_ci:
        f_gitlab_ci.write(render_file(args.template,
                                      load_recipe(args.docker_recipe)))


if __name__ == '__main__':
    main()
