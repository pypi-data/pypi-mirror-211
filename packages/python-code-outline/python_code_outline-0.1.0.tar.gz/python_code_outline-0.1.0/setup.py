# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_code_outline']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-code-outline',
    'version': '0.1.0',
    'description': 'Takes a folder path and outputs a text outline of the code, supports ignore files.',
    'long_description': "# Python Code Structure Report Generator\n\n![Test](https://github.com/seandearnaley/python-code-outline/workflows/Run%20pytest/badge.svg)\n\nThis Python script generates a text-based report of the code structure for all Python files in a given folder. It's useful for getting a quick overview of the code structure of a Python project. This can be particularly helpful for ChatGPT/Large Language Model (LLM) applications where you need to ask high-level questions about your codebase.\n\n[Example Report](example_report.txt?raw=true)\n\n## Usage\n\nTo use this script, run the `python_report_generator.py` file and provide the path to the folder containing the Python files you want to analyze. You can also optionally specify a name for the report file, which defaults to `report.txt` if not provided, and a path to the ignore file. The ignore file should be a `.gitignore` file or a file with the same format as a `.gitignore` file. If provided, the script will parse the ignore patterns from the file and exclude the matching files and folders from the report.\n\n```bash\npython python_report_generator.py /path/to/folder --report_file_path custom_report.txt --ignore_file_path /path/to/folder/.gitignore\n```\n\nIf the `--report_file_path` option is not specified, the report will be written to `report.txt` by default.\n\n```bash\npython python_report_generator.py /path/to/folder\n```\n\n## Output\n\nThe script will generate a text-based report of the code structure for each Python file in the specified folder. The report includes information about imports, classes, functions, and variables in each file.\n\n## Optional Parameters\n\n- `--report_file_path`: The name of the report file. Defaults to `report.txt` if not provided.\n- `--ignore_file_path`: The path to the ignore file. If provided, the script will parse the ignore patterns from the file and exclude the matching files and folders from the report.\n\n## Requirements\n\nThis script requires Python 3.x to run.\n\n## Installation\n\nThis project uses [Poetry](https://python-poetry.org/) for dependency management. To install the dependencies, first install Poetry by following the [official installation guide](https://python-poetry.org/docs/#installation), and then run the following command in the project directory:\n\n```bash\npoetry install\n```\n\nThis will create a virtual environment and install the required dependencies.\n\n## Running Tests\n\nThis project uses `pytest` for testing. To run the tests, first activate the virtual environment created by Poetry:\n\n```bash\npoetry shell\n```\n\nThen, run the tests using the following command:\n\n```bash\npytest\n```\n\n## Checking Test Coverage\n\nThis project uses the `coverage` package to generate test coverage reports. To check the test coverage, run the following command:\n\n```bash\ncoverage run -m pytest\n```\n\nThis will generate a `.coverage` file with the coverage data. To view the coverage report, run:\n\n```bash\ncoverage report\n```\n\nTo generate an HTML report, run:\n\n```bash\ncoverage html\n```\n\nThis will create an `htmlcov` directory containing the HTML report.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.",
    'author': 'Sean Dearnaley',
    'author_email': 'SeanDearnaley@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
