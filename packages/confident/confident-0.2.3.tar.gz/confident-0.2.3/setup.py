# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confident', 'confident.loaders']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'confident',
    'version': '0.2.3',
    'description': 'Loading configurations from multiple sources into a data model.',
    'long_description': '# Confident\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/confident?style=plastic)](https://github.com/limonyellow/confident)\n[![PyPI](https://img.shields.io/pypi/v/confident?style=plastic&color=%2334D058)](https://pypi.org/project/confident/)\n[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/limonyellow/confident/Python%20package/main?style=plastic)](https://github.com/limonyellow/confident/actions)\n[![GitHub](https://img.shields.io/github/license/limonyellow/confident?style=plastic)](https://github.com/limonyellow/confident)\n---\n\n**Documentation**: [https://confident.readthedocs.io/en/latest/](https://confident.readthedocs.io/en/latest/)\n\n---\n\nConfident helps you create configuration objects from multiple sources such as files and environment variables.  \nConfident config objects are data models that enforce validation and type hints by using [pydantic](https://pydantic-docs.helpmanual.io/) library.\n\nWith Confident you can manage multiple configurations depend on the environment your code is deployed.\nWhile having lots of flexibility how to describe your config objects, Confident will provide visibility of the process \nand help you expose misconfiguration as soon as possible.\n\nFor simple configuration loading from environment variables, you might want to check pydantic\'s [`BaseSettings`](https://pydantic-docs.helpmanual.io/usage/settings/) model.\n\n## Example\n```python\nimport os\n\nfrom confident import Confident\n\n\n# Creating your own config class by inheriting from `Confident`.\nclass MyAppConfig(Confident):\n    port: int = 5000\n    host: str = \'localhost\'\n    labels: list\n\n\n# Illustrates some environment variables.\nos.environ[\'host\'] = \'127.0.0.1\'\nos.environ[\'labels\'] = \'["FOO", "BAR"]\'  # JSON strings can be used for more types.\n\n\n# Creating the config object. `Confident` will load the values of the properties.\nconfig = MyAppConfig()\n\nprint(config.host)\n#> 127.0.0.1\nprint(config.json())\n#> {"port": 5000, "host": "127.0.0.1", "labels": ["FOO", "BAR"]}\nprint(config)\n#> port=5000 host=\'127.0.0.1\' labels=[\'FOO\', \'BAR\']\nprint(config.full_fields())\n#> {\n# \'port\': ConfigProperty(name=\'port\', value=5000, origin_value=5000, source_name=\'MyAppConfig\', source_type=\'class_default\', source_location=PosixPath(\'~/confident/readme_example.py\')),\n# \'host\': ConfigProperty(name=\'host\', value=\'127.0.0.1\', origin_value=\'127.0.0.1\', source_name=\'host\', source_type=\'env_var\', source_location=\'host\'),\n# \'labels\': ConfigProperty(name=\'labels\', value=[\'FOO\', \'BAR\'], origin_value=\'["FOO", "BAR"]\', source_name=\'labels\', source_type=\'env_var\', source_location=\'labels\')\n# }\n\n```\n\n## Installation\n```pip install confident```\n\n## Capabilities\nConfident object can load config fields from multiple sources:\n- Environment variables.\n- Config files such as \'json\' and \'yaml\'.\n- \'.env\' files.\n- Explicitly given fields.\n- Default values.\n- Deployment configs. (See documentation)\n\nLoading capabilities can be customized easily.\nConfident handles the loading and then provides ways to understand which value was loaded from what source.   \n\nConfident object core functionality is based on [pydantic](https://pydantic-docs.helpmanual.io/) library. \nThat means the Confident config object has all the benefits of pydantic\'s [`BaseModel`](https://pydantic-docs.helpmanual.io/usage/models/) including\nType validation, [object transformation](https://pydantic-docs.helpmanual.io/usage/exporting_models/) and many more features.\n\n## Examples\nMore examples can be found in the project\'s [repository](https://github.com/limonyellow/confident).\n\n## Contributing\nTo contribute to Confident, please make sure any new features or changes to existing functionality include test coverage.\n',
    'author': 'limonyellow',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/limonyellow/confident',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
