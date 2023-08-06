import argparse
import os

parser = argparse.ArgumentParser(description="Docker Recipe File")
parser.add_argument('-r',
                    '--docker-recipe',
                    default=os.path.join(os.getcwd(), 'docker-recipe.yml'),
                    help='Path to the docker-recipe.yml file. ' +
                         'Default is `docker-recipe.yml` in the current working directory.')

parser.add_argument('-t',
                    '--template',
                    required=True,
                    help='Path to the template file.')

parser.add_argument('-o',
                    '--output',
                    required=True,
                    help='Path to the output file.')
