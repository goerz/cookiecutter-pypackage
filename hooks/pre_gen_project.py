import re
import sys
import shutil

if not sys.version_info >= (3, 3):
    print('ERROR: You must be running Python >= 3.3')
    sys.exit(1)  # cancel project

MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.project_slug}}'

if not re.match(MODULE_REGEX, module_name):
    print('ERROR: The project slug (%s) is not a valid Python module name. '
          'Please do not use a - and use _ instead' % module_name)
    sys.exit(1)  # cancel project

executables = ['flake8', 'pep8', 'pip', 'twine']
if "{{ cookiecutter.environment_manager }}" == 'conda':
    executables.append('conda')
if "{{ cookiecutter.environment_manager }}" == 'tox':
    executables.append('tox')
for executable in executables:
    if not shutil.which(executable):
        print('WARNING: You do not have the %s executable. You should '
              'install it now through pip/conda' % executable)
