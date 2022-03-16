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

* select desired python version, currently only support `python3.6.*`.

```bash
poetry env use /full/path/to/python3.6.*
```

* install dependencies

```bash
poetry install
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

## Maintainers

## License














