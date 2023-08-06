# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_qa']

package_data = \
{'': ['*']}

install_requires = \
['chromadb>=0.3.25,<0.4.0',
 'fire>=0.5.0,<0.6.0',
 'langchain>=0.0.187,<0.0.188',
 'openai>=0.27.7,<0.28.0',
 'pathspec>=0.11.1,<0.12.0',
 'tiktoken>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['code_qa = code_qa.cli:main']}

setup_kwargs = {
    'name': 'code-qa',
    'version': '0.1.0',
    'description': '',
    'long_description': "# CodeQA\n\nCodeQA is a command-line tool that allows you to ask questions about a project. Gain insights and deepen your\nunderstanding of a repository's codebase effortlessly. It is built on top of LangChain.\n\n## Getting Started\n\nInstall Code QA:\n\n```bash\npip install code-qa\n```\n\nAdd your OpenAI token as virtual environment:\n\n```bash\nexport OPENAI_TOKEN=YOUR_TOKEN\n```\n\nGo to your project folder:\n\n```bash\ncd PATH/TO/MY/PROJECT\n```\n\nInitialise Code QA Index. This will generate an `code_qa` folder within your project:\n\n```\ncode_qa init\n```\n\nAsk questions about my code:\n\n```\ncode_qa query How can I test this?\n```\n\n## Ignoring Files\n\nIf you want to ignore certain files, then create an `.codeqaignore` file and specify them. The file follows the same\nstandard as `.gitignore`\n\n## License\nApache License Version 2.0, see `LICENSE`",
    'author': 'Steven Mi',
    'author_email': 'steven.mi@getyourguide.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
