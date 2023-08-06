# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resoto_plugins']

package_data = \
{'': ['*']}

install_requires = \
['resoto-plugin-aws==2.2.0',
 'resoto-plugin-cleanup-aws-alarms==2.2.0',
 'resoto-plugin-cleanup-aws-loadbalancers==2.2.0',
 'resoto-plugin-cleanup-aws-vpcs==2.2.0',
 'resoto-plugin-cleanup-expired==2.2.0',
 'resoto-plugin-cleanup-untagged==2.2.0',
 'resoto-plugin-cleanup-volumes==2.2.0',
 'resoto-plugin-digitalocean==2.2.0',
 'resoto-plugin-example-collector==2.2.0',
 'resoto-plugin-gcp==2.2.0',
 'resoto-plugin-github==2.2.0',
 'resoto-plugin-k8s==2.2.0',
 'resoto-plugin-onelogin==2.2.0',
 'resoto-plugin-onprem==2.2.0',
 'resoto-plugin-protector==2.2.0',
 'resoto-plugin-slack==2.2.0',
 'resoto-plugin-tagvalidator==2.2.0',
 'resoto-plugin-vsphere==2.2.0']

setup_kwargs = {
    'name': 'resoto-plugins',
    'version': '2.2.0',
    'description': 'Resoto plugins collection',
    'long_description': 'Meta package containing all resoto plugins.\n\nInstallation:\n\n```\npip install resoto-plugins\n```',
    'author': 'Some Engineering Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/someengineering/resoto-plugins',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
