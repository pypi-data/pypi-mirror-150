# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turbo', 'turbo.templatetags']

package_data = \
{'': ['*'],
 'turbo': ['static/turbo/js/reconnecting-websocket.min.js',
           'static/turbo/js/reconnecting-websocket.min.js',
           'static/turbo/js/reconnecting-websocket.min.js',
           'static/turbo/js/turbo-django.js',
           'static/turbo/js/turbo-django.js',
           'static/turbo/js/turbo-django.js',
           'static/turbo/js/turbo.min.js',
           'static/turbo/js/turbo.min.js',
           'static/turbo/js/turbo.min.js',
           'templates/turbo/*',
           'templates/turbo/components/*']}

install_requires = \
['Django>=3.2.0', 'channels>=2.0.0']

setup_kwargs = {
    'name': 'turbo-django',
    'version': '0.4.0',
    'description': 'Integrate Hotwire Turbo with Django allowing for a Python-driven dynamic web experience.',
    'long_description': '[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fhotwire-django%2Fturbo-django%2Fbadge%3Fref%3Dmain&style=flat)](https://actions-badge.atrox.dev/hotwire-django/turbo-django/goto?ref=main)\n[![Documentation Status](https://readthedocs.org/projects/turbo-django/badge/?version=latest)](https://turbo-django.readthedocs.io/en/latest/?badge=latest)\n[![Issues](https://img.shields.io/github/issues/hotwire-django/turbo-django)](https://img.shields.io/github/issues/hotwire-django/turbo-django)\n[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2FDjangoHotwire)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fhotwire-django%2Fturbo-django)\n\n# Turbo for Django\n\n\nIntegrate [Hotwire Turbo](https://turbo.hotwired.dev/) with Django with ease.\n\n\n## Requirements\n\n- Python 3.8+\n- Django 3.1+\n- Channels 3.0+ _(Optional for Turbo Frames, but needed for Turbo Stream support)_\n\n## Installation\n\nTurbo Django is available on PyPI - to install it, just run:\n\n    pip install turbo-django\n\nAdd `turbo` and `channels` to `INSTALLED_APPS`, and copy the following `CHANNEL_LAYERS` setting:\n\n```python\nINSTALLED_APPS = [\n    ...\n    \'turbo\',\n    \'channels\'\n    ...\n]\n\nCHANNEL_LAYERS = {\n    "default": {\n        # You will need to `pip install channels_redis` and configure a redis instance.\n        # Using InMemoryChannelLayer will not work as the memory is not shared between threads.\n        # See https://channels.readthedocs.io/en/latest/topics/channel_layers.html\n        "BACKEND": "channels_redis.core.RedisChannelLayer",\n        "CONFIG": {\n            "hosts": [("127.0.0.1", 6379)],\n        },\n    }\n}\n\n```\n\nAnd collect static files if the development server is not hosting them:\n\n```sh\n./manage.py collectstatic\n```\n\n_Note: Both Hotwire and this library are still in beta development and may introduce breaking API changes between releases.  It is advised to pin the library to a specific version during install._\n\n## Quickstart\nWant to see Hotwire in action? Here\'s a simple broadcast that can be setup in less than a minute.\n\n**The basics:**\n\n* A Turbo Stream class is declared in python.\n\n* A template subscribes to the Turbo Stream.\n\n* HTML is be pushed to all subscribed pages which replaces the content of specified HTML p tag.\n\n\n### Example\n\nFirst, in a django app called `quickstart`, declare `BroadcastStream` in a file named `streams.py`.\n\n```python\n# streams.py\n\nimport turbo\n\nclass BroadcastStream(turbo.Stream):\n    pass\n\n```\n\nThen, create a template that subscribes to the stream.\n\n```python\nfrom django.urls import path\nfrom django.views.generic import TemplateView\n\nurlpatterns = [\n    path(\'quickstart/\', TemplateView.as_view(template_name=\'broadcast_example.html\'))\n]\n```\n\n```html\n# broadcast_example.html\n\n{% load turbo_streams %}\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    {% include "turbo/head.html" %}\n</head>\n<body>\n    {% turbo_subscribe \'quickstart:BroadcastStream\' %}\n\n    <p id="broadcast_box">Placeholder for broadcast</p>\n</body>\n</html>\n```\n\nNow run ``./manage.py shell``.  Import the Turbo Stream and tell the stream to take the current timestamp and ``update`` the element with id `broadcast_box` on all subscribed pages.\n\n```python\nfrom quickstart.streams import BroadcastStream\nfrom datetime import datetime\n\nBroadcastStream().update(text=f"The date and time is now: {datetime.now()}", id="broadcast_box")\n```\n\nWith the `quickstart/` path open in a browser window, watch as the broadcast pushes messages to the page.\n\nNow change `.update()` to `.append()` and resend the broadcast a few times.  Notice you do not have to reload the page to get this modified behavior.\n\nExcited to learn more?  Be sure to walk through the [tutorial](https://turbo-django.readthedocs.io/en/latest/index.html) and read more about what Turbo can do for you.\n\n## Documentation\nRead the [full documentation](https://turbo-django.readthedocs.io/en/latest/index.html) at readthedocs.io.\n\n\n## Contribute\n\nDiscussions about a Django/Hotwire integration are happening on the [Hotwire forum](https://discuss.hotwired.dev/t/django-backend-support-for-hotwire/1570). And on Slack, which you can join by [clicking here!](https://join.slack.com/t/pragmaticmindsgruppe/shared_invite/zt-kl0e0plt-uXGQ1PUt5yRohLNYcVvhhQ)\n\nAs this new magic is discovered, you can expect to see a few repositories with experiments and demos appear in [@hotwire-django](https://github.com/hotwire-django). If you too are experimenting, we encourage you to ask for write access to the GitHub organization and to publish your work in a @hotwire-django repository.\n\n\n## License\n\nTurbo-Django is released under the [MIT License](https://opensource.org/licenses/MIT) to keep compatibility with the Hotwire project.\n\nIf you submit a pull request. Remember to add yourself to `CONTRIBUTORS.md`!\n',
    'author': 'Nikita Marchant',
    'author_email': 'C4ptainCrunch@github-username.x',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
