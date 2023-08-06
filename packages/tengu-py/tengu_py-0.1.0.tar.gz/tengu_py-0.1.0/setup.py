# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tengu']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'datargs>=0.11.0,<0.12.0',
 'gql[requests]>=3.4.0,<4.0.0',
 'rdkit-pypi>=2022.9.5,<2023.0.0']

setup_kwargs = {
    'name': 'tengu-py',
    'version': '0.1.0',
    'description': 'Python SDK for interacting with the QDX Tengu API',
    'long_description': '# Tengu-py: Python SDK for the QDX Tengu API\n\nThis package exposes a simple provider and CLI for the different tools exposed by the QDX Tengu GraphQL API.\n\n## Usage\n\n### As a library\n\n``` python\nimport json\nfrom pathlib import Path\n\nimport tengu\n\nTOKEN = "your qdx access token"\n\n# get our client to talk with the API\nclient = tengu.Provider(access_token=TOKEN)\n\n# get modules that can be run\nclient.modules()\n\n## running convert\n\n# path to protein pdb with correct charges and protonation\nprotein_pdb = Path("./examples/4w9f_prepared_protein.pdb")\n\n# get base64 encoded data\n\nfile_arg = provider.upload_arg(protein_pdb)\n\nclient.run("github:talo/tengu-prelude/f8e2e55d9bd428aa7f2bbe3f87c24775fa592b10#convert", [ \n{ "value": "PDB" }, file_arg\n])\n```\n',
    'author': 'Ryan Swart',
    'author_email': 'ryan@talosystems.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
