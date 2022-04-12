# Wizard _(Client Program for Umich-SIM)_

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

Repository for Wizard of Oz Project.

## Table of Contents

* [Background](##Background)
* [Install & Usage](##Install-&-Usage)
* [Maintainers](##Maintainers)
* [License](##License)

## Background

The Wizard of Oz is an inexpensive and flexible method to examine shared control between humans and automated cars. In the Wizard of Oz method, a hidden experimenter -- the wizard as in the Wizard of Oz story -- controls the system as if it were controlled by automation.

## Install & Usage

The project uses [poetry](https://python-poetry.org/) to manage packages and environments, make sure poetry is installed before continue. See the [documentation](https://python-poetry.org/docs/) for more infos.

* select desired python version, currently only support `python3.6-8`.

```bash
poetry env use /full/path/to/python3.[6-8].*
```

* install dependencies

```bash
poetry install
# if using python 3.6, need to install dataclasses
pip install dataclasses
```

* run the program

```bash
# run directly
poetry run python wizard/main.py
# alternatively, activate the virtual environment for more flexibility
poetry shell
python wizard/main.py
```

The client program needs the Carla server to be running, use command line options to change the default host and port.

## Overall Project setup
1. Start the CARLA server(GUI and Map Team perhaps can help)

2. Start the [wizard server](https://github.com/UmichSIM/Wizard-Server)

3. connect the racing wheel and indicate the device path in `wizard/config.py`

   + find the device path

   ```bash
   # note the event number in the H field
   cat /proc/bus/input/devices
   ```

   + edit `wizard/config.py` file and change the file path if needed

   ```python
   # device event file
   user_input_event:str = "/dev/input/eventX"
   ```

4. run the program

```bash
python wizard/main.py
# for wizard side, use
python wizard/main.py --host <host> --wizard
```

## Documentation

1. see the [project wiki](https://github.com/UmichSIM/Wizard/wiki) for hardware setups
2. use `pdoc3` to view the overall code structure

```bash
# assume poetry environment is activated
pdoc3 --http : wizard
```





## Maintainers

Umich Driving Simulator Wizard Team











