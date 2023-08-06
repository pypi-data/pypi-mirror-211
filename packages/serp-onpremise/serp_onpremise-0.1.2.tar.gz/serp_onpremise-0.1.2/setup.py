# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serp_onpremise',
 'serp_onpremise.asm',
 'serp_onpremise.auth',
 'serp_onpremise.compare',
 'serp_onpremise.entries',
 'serp_onpremise.groups_profiles',
 'serp_onpremise.licenses',
 'serp_onpremise.liveness',
 'serp_onpremise.origins',
 'serp_onpremise.profiles',
 'serp_onpremise.spaces',
 'serp_onpremise.statistics',
 'serp_onpremise.tokens',
 'serp_onpremise.tokens.access',
 'serp_onpremise.tokens.streams',
 'serp_onpremise.users',
 'serp_onpremise.whoami']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0', 'sphinx>=7.0.1,<8.0.0', 'websockets>=10.0,<11.0']

setup_kwargs = {
    'name': 'serp-onpremise',
    'version': '0.1.2',
    'description': 'A Python package for interacting with SERP on-premise API',
    'long_description': '# Python API client for SERP on-premise API\n\n---\n\nThis library is mirror of official SERP on-premise API in terms of methods and interfaces.\n\nFor your convenience, you can make API calls using sync or async (asyncio) interface.\n\n## Installation\n\n```sh\npip install serp_onpremise\n```\n\nNote that it is always recommended pinning version of your installed packages.\n\n## Usage example (sync)\n\nAn example of how to create an origin:\n\n```python\nfrom serp_onpremise import Client\n\n\nif __name__ == \'__main__\':\n    # api_token is just str with your API token\n    api_token = "abcd012345"\n    # Now create instance of Client. There should be only one per process.\n    client = Client(base_url="http://localhost:8080", api_token=api_token)\n    # Issue API request to create an origin\n    client.origins.create(name="test_name")\n\n```\n\nNow that we have our origin created, we can create profile inside that origin:\n\n```python\nfrom serp_onpremise import Client\n\n\ndef create_profiles_example(client: Client):\n    origin_id = 1  # you can inspect response from `client.origins.create`\n    with open("image.png", "rb") as f:\n        response = client.profiles.create(\n            image=f,\n            origin_id=origin_id\n        )\n    print("Profiles Create Response:\\n", response.json(), flush=True)\n\n\nif __name__ == \'__main__\':\n    # api_token is just str with your API token\n    api_token = "abcd012345"\n    # Now create instance of Client. There should be only one per process.\n    client = Client(base_url="http://localhost:8080", api_token=api_token)\n    # Issue API request to create a profile\n    create_profiles_example(client)\n\n```\n\nNow that we have our origin & profile created, we can search for profile:\n\n```python\nfrom serp_onpremise import Client\n\n\ndef search_profiles_example(client: Client):\n    with open("image.png", "rb") as f:\n        response = client.profiles.search(\n            image=f,\n            identify_asm=True\n        )\n    print("Profiles Search Response:\\n", response.json(), flush=True)\n\n\nif __name__ == \'__main__\':\n    # api_token is just str with your API token\n    api_token = "abcd012345"\n    # Now create instance of Client. There should be only one per process.\n    client = Client(base_url="http://localhost:8080", api_token=api_token)\n    # Issue API request to search profiles\n    search_profiles_example(client)\n\n```\n\n_For more examples and usage, please refer to the [docs](./docs)._\n\n## Development setup\n\nTo install all the development requirements:\n\n```sh\npip install --upgrade pip\npip install poetry\npoetry install --no-root\n```\n\nTo run linters & test suite:\n\n```sh\n./scripts/test.sh\n```\n\n## How to release\n\n1. Update version in:\n   - `CHANGELOG.md`\n   - `__init__.py`\n   - `pyproject.toml`\n2. Lock deps to update version in poetry: `poetry lock`\n3. Get API Token from account settings in [PyPI](https://pypi.org/manage/account/)\n4. `poetry config pypi-token.pypi YOUR_API_TOKEN`\n5. `poetry build`\n6. `poetry publish`\n\n## Release History\n\n- 0.1.1\n  - Fixed types of custom Enum classes and in corresponding methods\n- 0.1.0\n  - Initial version of package\n\n## License\n\nDistributed under the MIT license. See `LICENSE` for more information.\n\n## Contributing\n\n1. Create your feature branch (`git checkout -b feature/fooBar`)\n2. Commit your changes (`git commit -am \'Add some fooBar\'`)\n3. Push to the branch (`git push origin feature/fooBar`)\n4. Create a new Pull Request\n',
    'author': 'serptech.ru',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
