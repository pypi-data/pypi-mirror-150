# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbup']

package_data = \
{'': ['*']}

install_requires = \
['b2sdk>=1.14.0,<2.0.0',
 'colorama>=0.4.4,<0.5.0',
 'requests>=2.27.1,<3.0.0',
 'typer[all]>=0.4.0,<0.5.0',
 'validators>=0.18.1,<0.19.0']

entry_points = \
{'console_scripts': ['bbup = bbup.main:app']}

setup_kwargs = {
    'name': 'bbup',
    'version': '1.1.0',
    'description': '',
    'long_description': "# Backblaze Uploader\n\nBackblaze Uploader is a Python package that you can use in order to upload files to a Backblaze bucket from a remote URL or a local path.\n\n### Install\n```bash\npip install bbup\n```\n\n### Configure a Bucket\nSign in to your Backblaze account, create a bucket, create application keys and then configure **bbup**:\n\n```bash\nbbup configure\n```\n\nYou can add as many buckets as you want. Beware that app keys are stored in plain text, so don't use this software on a shared computer.\n\n### Upload Remote Files\nUpload a remote file to the default bucket:\n```bash\nbbup remote-upload\n```\n\nUpload a remote file to a selected bucket:\n\n```bash\nbbup remote-upload --bucket mybucket\n```\n\n### Upload Local Files\nUpload a local file to the default bucket:\n```bash\nbbup local-upload\n```\n\nUpload a remote file to a selected bucket:\n\n```bash\nbbup local-upload --bucket mybucket\n```\n\n### Uninstall\n```bash\npip uninstall bbup\n```",
    'author': 'Rehmat Alam',
    'author_email': 'contact@rehmat.works',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
