# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iso18245']

package_data = \
{'': ['*'], 'iso18245': ['data/*']}

setup_kwargs = {
    'name': 'iso18245',
    'version': '1.2.0',
    'description': 'The ISO 18245 Merchant Category Codes database',
    'long_description': '# python-iso18245\n\nA Python implementation of the ISO 18245 Merchant Category Codes database.\n\n## Installation\n\n- `pip install iso18245`\n\n## Usage\n\n```py\n\n>>> import iso18245\n>>> iso18245.get_mcc("5542")\nMCC(range=MCCRange(start=\'5000\', end=\'5599\', description=\'Retail outlets\', reserved=False), iso_description=\'Automated fuel dispensers\', usda_description=\'Automated Fuel Dispensers\', stripe_description=\'Automated Fuel Dispensers\', stripe_code=\'automated_fuel_dispensers\')\n>>> iso18245.get_mcc("3000")\nMCC(range=MCCRange(start=\'3000\', end=\'3999\', description=\'Reserved for private use\', reserved=True), iso_description=\'\', usda_description=\'UNITED AIRLINES\', stripe_description=\'\', stripe_code=\'\')\n>>> iso18245.get_mcc("3000").usda_description\n\'UNITED AIRLINES\'\n>>> iso18245.get_mcc("3000").range\nMCCRange(start=\'3000\', end=\'3999\', description=\'Reserved for private use\', reserved=True)\n>>> iso18245.get_mcc("999999")\nTraceback (most recent call last):\n  …\niso18245.InvalidMCC: 999999\n```\n\n## External links\n\n- [Wikipedia: ISO 18245](https://en.wikipedia.org/wiki/ISO_18245)\n- [ISO Standard 18245:2003](https://www.iso.org/standard/33365.html)\n- [AFNOR: ISO 18245](http://portailgroupe.afnor.fr/public_espacenormalisation/ISOTC68SC7/ISO%2018245.html)\n- [Stripe MCC List](https://stripe.com/docs/issuing/categories)\n- [USDA MCC List (incl. private MCCs)](https://www.dm.usda.gov/procurement/card/card_x/mcc.pdf)\n- [VISA Merchant Data Standards Manual](https://usa.visa.com/content/dam/VCOM/download/merchants/visa-merchant-data-standards-manual.pdf)\n',
    'author': 'Jerome Leclanche',
    'author_email': 'jerome@leclan.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jleclanche/python-iso18245',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
