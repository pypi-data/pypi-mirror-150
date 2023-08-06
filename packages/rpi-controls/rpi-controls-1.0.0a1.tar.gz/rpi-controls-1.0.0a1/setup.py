# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpicontrols']

package_data = \
{'': ['*']}

install_requires = \
['RPi.GPIO>=0.7.1,<0.8.0', 'importlib-metadata>=4.11.3,<5.0.0']

setup_kwargs = {
    'name': 'rpi-controls',
    'version': '1.0.0a1',
    'description': 'Library that eases interacting with physical buttons through the Raspberry Pi GPIO',
    'long_description': "# GPIO controller for Raspberry Pi\n\n[![CI](https://github.com/2franix/rpi-controls/actions/workflows/python-package.yml/badge.svg)](https://github.com/2franix/rpi-controls/actions/workflows/python-package.yml)\n[![TestPyPI](https://github.com/2franix/rpi-controls/actions/workflows/python-publish-testpypi.yml/badge.svg)](https://github.com/2franix/rpi-controls/actions/workflows/python-publish-testpypi.yml)\n[![PyPI](https://github.com/2franix/rpi-controls/actions/workflows/python-publish-pypi.yml/badge.svg)](https://github.com/2franix/rpi-controls/actions/workflows/python-publish-pypi.yml)\n\nThis package provides classes to interact with physical buttons connected to a Raspberry Pi's GPIO. Those classes make it easy to run event-driven callbacks.\n\n# Brief example\n\nThe example below illustrates the implementation of a callback to execute asynchronously when clicking a button:\n```python\nfrom rpicontrols import Controller, Button, PullType, make_controller\n\n# Initialize the button controller. A single instance can handle as many buttons as needed.\ncontroller: Controller = make_controller()\n\n# Create the button, connected to pin 22.\nbutton: Button = controller.make_button(\n    input_pin_id=22,  # Id of the GPIO pin the button switch is connected to.\n    input=Button.InputType.PRESSED_WHEN_OFF,  # Depends on the physical wiring of the button.\n    pull=PullType.UP  # Whether to enable pull-up or pull-down resistor. Use PullType.NONE to disable.\n)\n\n# Define a callback to run when button is clicked.\nasync def on_click_callback(button: Button) -> None:\n    print(f'Button {button.name} clicked!')\n\n    # Run some IO-bound task without blocking.\n    # Other event handlers may run while waiting.\n    await asyncio.sleep(2)\n\n# Subscribe to the click event.\nbutton.add_on_click(on_click_callback)\n\n# Start controller main loop. Use controller.start_in_thread() for the non-blocking version.\ncontroller.run()\n```\n\nAsynchronous callbacks are optional and synchronous ones work just fine. Check out the full documentation [here](https://rpi-controls.readthedocs.io) for all the details.\n",
    'author': 'Cyrille Defranoux',
    'author_email': None,
    'maintainer': 'Cyrille Defranoux',
    'maintainer_email': 'cyrille.github@defx.fr',
    'url': 'https://githuob.com/2franix/rpi-controls',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
