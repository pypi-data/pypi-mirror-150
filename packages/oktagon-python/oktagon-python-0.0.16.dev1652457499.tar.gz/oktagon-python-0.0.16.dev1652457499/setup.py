# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oktagon_python']

package_data = \
{'': ['*']}

install_requires = \
['okta-jwt-verifier', 'starlette']

setup_kwargs = {
    'name': 'oktagon-python',
    'version': '0.0.16.dev1652457499',
    'description': 'Python utility package for verifying & decoding OKTA tokens',
    'long_description': '# oktagon-python\n\n[![PyPI](https://img.shields.io/pypi/v/oktagon-python?logo=pypi&logoColor=white&style=for-the-badge)](https://pypi.org/project/oktagon-python/)\n\nThis python package is a tiny utility for verifying & decoding OKTA tokens in python\nbackend services.\n\n## Installation\n\n```shell\npip install oktagon-python\n```\n\n## Getting Started\n\nLet\'s say you have /consignments REST API endpoint which you\'d like to make accessible\nonly by logistics OKTA group. Then you would write something like this:\n\n```pyhton\nimport os\n\nfrom oktagon_python.authorisation import AuthorisationManager\nfrom starlette.requests import Request\n\nauth_manager = AuthorisationManager(\n    service_name="your_service_name",\n    okta_issuer=os.environ.get("OKTAGON_OKTA_ISSUER"),\n    okta_audience=os.environ.get("OKTAGON_OKTA_AUDIENCE"),\n)\n\nasync def is_authorised(request: Request):\n    return await auth_manager.is_user_authorised(\n        allowed_groups=["logistics"],\n        resource_name="consignments",\n        cookies=request.cookies\n    )\n```\n\nThis will create an `AuthorisationManager` instance that will check user\'s\nauthorisation.\n\n## Contributing\n\n```shell\ngit clone https://github.com/madedotcom/oktagon-python.git\ncd oktagon-python\nmake install\nmake tests\n```\n\nThis will install all the dependencies (including dev ones) and run the tests.\n\n### Run the formatters/linters\n\n```shell\nmake pretty\n```\n\nWill run all the formatters and linters (`black`, `isort` and `pylint`) in write mode.\n\n```shell\nmake pretty-check\n```\n\nWill run the formatters and linters in check mode.\n\nYou can also run them separtly with `make black`, `make isort`, `make pylint`.\n\n## Realeses\n\nMerging a PR into the `main` branch will trigger the GitHub `release` workflow. \\\nThe following GitHub actions will be triggered:\n\n- [github-tag-action](https://github.com/anothrNick/github-tag-action) will bump a new\n  tag with `patch` version by default. Add `#major` or `#minor` to the merge commit\n  message to bump a different tag;\n- [gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) will push the\n  newly built package on PyPI;\n- [action-automatic-releases](https://github.com/marvinpinto/action-automatic-releases)\n  will create the GitHub release and tag it with `latest` as well.\n',
    'author': 'Made.com Tech Team',
    'author_email': 'tech@made.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/madedotcom/oktagon-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
