import argparse
import os

parser = argparse.ArgumentParser(description="Docker Recipe File")
parser.add_argument('-r',
                    '--docker-recipe',
                    default=os.path.join(os.getcwd(), 'docker-recipe.yml'),
                    help='Path to the docker-recipe.yml file. ' +
                         'Default is `docker-recipe.yml` in the current working directory.')

parser.add_argument('-g',
                    '--gitlab-ci-template',
                    default=os.path.join(os.getcwd(), '.gitlab-ci.recipe.yml'),
                    help='Path to the .gitlab-ci.recipe.yml file. ' +
                         'Default is `.gitlab-ci.recipe.yml` in the current working directory.')

parser.add_argument('-o',
                    '--gitlab-ci-output-file',
                    default=os.path.join(os.getcwd(), '.gitlab-ci.yml'),
                    help='Path to the .gitlab-ci.yml file. ' +
                         'Default is `.gitlab-ci.recipe.yml` in the current working directory.')
