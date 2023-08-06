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
    'version': '0.3.1',
    'description': 'CodeQA: Unleash the power of AI in your codebase. Ask questions & get insights from your document.',
    'long_description': '# CodeQA\n\n**CodeQA** is a **powerful command-line tool** designed to help **developers understand and navigate their codebase**\nmore efficiently. **By asking questions** directly about your project, you can **gain insights and deepen your\nunderstanding of the codebase** without the need for extensive manual exploration. CodeQA is built on top of LangChain,\nleveraging its capabilities to provide accurate and insightful responses.\n\n**Besides code,** CodeQA is engineered to be **universally applicable across various text documents**. It enables you to\neffortlessly navigate through:\n\n- PDF documents\n- Markdown files\n- And any other form of text-based documents.\n\n## Getting Started\n\nFollow these steps to install and set up CodeQA:\n\n1. **Install CodeQA**: Use pip to install CodeQA. Run the following command in your terminal:\n\n    ```bash\n    pip install code-qa\n    ```\n\n2. **Set up OpenAI Token**: CodeQA uses OpenAI\'s API to generate responses. You need to add your OpenAI token to your\n   virtual environment. Replace `YOUR_TOKEN` with your actual OpenAI token:\n\n    ```bash\n    export OPENAI_TOKEN=YOUR_TOKEN\n    ```\n\n3. **Navigate to your project folder**: Use the `cd` command to navigate to your project\'s directory:\n\n    ```bash\n    cd PATH/TO/MY/PROJECT\n    ```\n\n4. **Initialize CodeQA Index**: This will generate a `.code_qa` folder within your project. The folder contains your\n   project embeddings stored as parquet files. Run the following command:\n\n    ```bash\n    code_qa init\n    ```\n\n## Usage\n\nWith CodeQA, you can ask questions directly about your code. For example, if you want to know how to test a particular\npart of your code, you can ask:\n\n```bash\ncode_qa query "How can I test this?"\n```\n\n## Ignoring Files\n\nIf there are certain files or directories that you want CodeQA to ignore, you can specify them in a `.codeqaignore`\nfile. This file follows the same syntax and rules as the `.gitignore` file. Simply create a `.codeqaignore` file in your\nproject\'s root directory and list the files or directories you want to ignore.\n\n## License\n\nCodeQA is licensed under the Apache License Version 2.0. For more details, see the [LICENSE](LICENSE) file.\n',
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
