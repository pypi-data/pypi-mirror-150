# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djpaypal',
 'djpaypal.management',
 'djpaypal.management.commands',
 'djpaypal.migrations',
 'djpaypal.models']

package_data = \
{'': ['*'], 'djpaypal': ['templates/djpaypal/admin/*']}

install_requires = \
['django>=3.1', 'paypalrestsdk>=1.13.1', 'python-dateutil>=2.6.1']

setup_kwargs = {
    'name': 'dj-paypal',
    'version': '0.16.0',
    'description': 'Django / Paypal integration (based on dj-stripe)',
    'long_description': '# dj-paypal\n\n[![Build Status](https://travis-ci.com/HearthSim/dj-paypal.svg?branch=master)](https://travis-ci.com/HearthSim/dj-paypal)\n[![PyPI](https://img.shields.io/pypi/v/dj-paypal.svg)](https://pypi.org/project/dj-paypal/)\n\n\nA Paypal integration for Django, inspired by [dj-stripe](https://github.com/dj-stripe/dj-stripe).\n\nCurrently only supports subscriptions.\n\n\n## Requirements\n\n- Python 3.6+\n- Django 3.1+\n- Postgres 9.6+ (Non-postgres engines not supported)\n\n\n## Installation\n\n1. Install dj-paypal with `pip install dj-paypal`\n2. Add `djpaypal` to django `INSTALLED_APPS` setting\n3. Get a client ID and client secret from paypal and add them to the settings\n   `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET`\n4. Set `PAYPAL_MODE = "sandbox"` (or `"live"`) in the settings\n5. Install your Billing Plans (see below)\n\n\n### Setting up billing plans\n\n#### Download already-created billing plans from Paypal\n\nRun `manage.py djpaypal_download_plans` to sync all plans already created upstream\ninto the local database.\n\nThis will create `djpaypal.models.BillingPlan` objects, which can be listed from\nthe Django admin.\n\n\n#### Creating new Paypal billing plans\n\nThe `manage.py djpaypal_upload_plans` management command creates billing plans using\nthe Paypal API. An extra `PAYPAL_PLANS` setting must be set, which will contain a dict\nof Paypal billing plans to create.\n\nSee `example_settings.py` for an example of plans to create.\n\n\n## Webhooks\n\nThe `djpaypal.views.ProcessWebhookView` view should be hooked up to an URL endpoint\nwhich you then set up in Paypal as a webhook endpoint (https://developer.paypal.com).\n\nIn order to verify webhooks being transmitted to your app, dj-paypal needs to know the\nID of the webhook that is expected at that URL. Set it in the setting `PAYPAL_WEBHOOK_ID`.\n\n\n## Sandbox vs. Live\n\nAll models have a `livemode` boolean attribute. That attribute is set to `True` if created\nin Live (production) mode, `False` otherwise (sandbox mode).\nSandbox and Live data can co-exist without issues. Once you are done testing in Sandbox\nmode, use the `manage.py djpaypal_delete_all_test_data` management command to (locally)\nclear all the test data. This command has no impact on the upstream data.\n\n\n## Data considerations\n\nMost of the models defined in dj-paypal are copies of the upstream Paypal model data.\nDeleting or editing objects (be it from the admin or in the database) does not actually\nchange any of the upstream Paypal data.\n\n\n## License and Sponsorship\n\nThis project was designed and developed by [HearthSim](https://hearthsim.net). It is\nlicensed under the MIT license. The full license text is available in the LICENSE file.\n',
    'author': 'Benedict Etzel',
    'author_email': 'benedict@hearthsim.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dj-stripe/dj-paypal',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
