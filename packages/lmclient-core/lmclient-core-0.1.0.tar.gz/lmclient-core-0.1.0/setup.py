# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lmclient', 'lmclient.completions']

package_data = \
{'': ['*']}

install_requires = \
['asyncer==0.0.2', 'openai>=0.27.7,<0.28.0', 'typing-extensions>=4.6.2,<5.0.0']

setup_kwargs = {
    'name': 'lmclient-core',
    'version': '0.1.0',
    'description': 'LM Async Client, openai client, azure openai client ...',
    'long_description': "# lmclient\n\nLM Async Client, OpenAI, Azure ...\n\n\n## Install\n\n```shell\npip install lmclient-core\n```\n\n## Usage\n\n```python\nfrom lmclient import LMClient, AzureCompletion, OpenAICompletion\n\nopenai_completion = OpenAICompletion(model='gpt-3.5-turbo')\n# azure_completion = AzureCompletion()\nclient = LMClient(openai_completion, async_capacity=5, max_requests_per_minute=20)\nprompts = [\n    'Hello, my name is',\n    'can you please tell me your name?',\n    'i want to know your name',\n    'what is your name?',\n]\nvalues = client.async_run(prompts=prompts)\nprint(values)\n```\n",
    'author': 'wangyuxin',
    'author_email': 'wangyuxin@mokahr.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
