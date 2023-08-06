# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gs_reminder',
 'gs_reminder.github',
 'gs_reminder.github.models',
 'gs_reminder.slack']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['gs_reminder = gs_reminder.notifier:main']}

setup_kwargs = {
    'name': 'gs-reminder',
    'version': '0.1.0',
    'description': 'Notify Slack of a review of Pull Requests in the GitHub repository.',
    'long_description': '# github-pr-slack-reminder\n\nNotify Slack of a review of Pull Requests in the GitHub repository.\n\n## Environments\n\n- Python 3.10\n  - Pipenv\n\n## Usage\n\n```shell\npip install gs-reminder\ngs_reminder -r nnsnodnb/github-pr-slack-reminder -u examples/username.json\n```\n\n### Environment variables\n\n- `GITHUB_TOKEN`\n  - Required\n  - Your GitHub Personal Access Token.\n    - Create https://github.com/settings/tokens\n- `SLACK_URL`\n  - Required\n  - Incoming webhook\'s url of Slack app.\n\n### Options\n\n- `-r` or `--repo`\n  - Required\n  - Your GitHub repository name. (ex. `nnsnodnb/github-pr-slack-reminder`)\n- `--file-username` or `-u`\n  - Required \n  - Corresponding files for GitHub and Slack usernames. (ex. `examples/username.json`)\n    ```json\n    [\n      {\n        "github": "nnsnodnb",\n        "slack": "yuya.oka"    \n      }\n    ]\n    ```\n\n## Example Result\n\n<img src="https://user-images.githubusercontent.com/9856514/168425744-bcfd0510-3ec3-433e-82c1-4d8d2d1940d8.png" alt="example result" width="500px">\n\n## License\n\nThis software is licensed under the MIT License.\n',
    'author': 'Yuya Oka',
    'author_email': 'nnsnodnb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nnsnodnb/github-pr-slack-reminder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
