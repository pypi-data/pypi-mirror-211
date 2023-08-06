from .get_file import get_file

imports = get_file('imports.py')

exec(imports)