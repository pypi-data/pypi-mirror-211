#! /usr/bin/env python

import os
import sys


def main():
    current_dir = os.getcwd()
    dir_name = "models"
    file_name = "models.py"

    dir_path = os.path.join(current_dir, dir_name)
    file_path = os.path.join(dir_path, file_name)

    if not os.path.exists(dir_path):
        os.makedirs(dir_name)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(f'from sqlcrafty import models'  # noqa: F541
                       f'\n\n'
                       f'# Create your models here\n'
                       f'\n\n'
                       f'class MyModel(models.BaseModel):\n'
                       f'    ...\n'
                       )


if __name__ == '__main__':
    if sys.argv[1] == 'start':
        main()
