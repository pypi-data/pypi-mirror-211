# Python module for binary_c
![docstring coverage](./badges/docstring_coverage.svg) ![test coverage](./badges/test_coverage.svg)

[![DOI](https://joss.theoj.org/papers/10.21105/joss.04642/status.svg)](https://doi.org/10.21105/joss.04642)

We present our package [binary_c-python](https://binary_c.gitlab.io/binary_c-python/), a population synthesis code which is aimed to provide a convenient and easy-to-use interface to the [binary_c](https://binary_c.gitlab.io/binary_c/) framework, allowing the user to rapidly evolve single stellar systems and populations of star systems. Based on earlier Perl versions by [Robert Izzard](https://robizzard.gitlab.io/), updated and extended for Python 3 by [David Hendriks](https://davidhendriks.com/), Robert Izzard. Credits to Jeff Andrews for early efforts on the python-c interface.

`binary_c-python` is developed for students and scientists in the field of stellar astrophysics, who want to study the evolution of individual or populations of single and binary star systems (see the [example use-case notebooks](https://binary_c.gitlab.io/binary_c-python/example_notebooks.html) in the [online documentation](https://binary_c.gitlab.io/binary_c-python)).

This is the development branch for `binary_c-python` version [1.0.1](https://gitlab.com/binary_c/binary_c-python/-/tree/releases/1.0.1/2.2.4) and `binary_c` version [2.2.4](https://gitlab.com/binary_c/binary_c/-/tree/releases/2.2.4).

The latest release branch is `binary_c-python` version [1.0.0](https://gitlab.com/binary_c/binary_c-python/-/tree/releases/1.0.0/2.2.4) and `binary_c` version [2.2.4](https://gitlab.com/binary_c/binary_c/-/tree/releases/2.2.4).

## Installation
Below we provide the installation instructions for `binary_c-python`.

### Requirements
To run this code you need to at least have installations of:

- `Python` version 3.9 up to 3.12 (it's recommended to use [Pyenv](https://github.com/pyenv/pyenv) to manage your Python versions)
- `binary_c` version 2.2.4 (See [installation section](https://binary_c.gitlab.io/binary_c#magicparlabel-156))

The Python packages that are required for this code to run are listed in the `requirements.txt`, which automatically gets read out by `setup.py`.

To build the documentation the following additional software is required:

- `pandoc` available on https://pandoc.org/ or via `sudo apt-get install pandoc`

### Environment variables
Before building `binary_c-python` please make sure to have defined the following environment variables:

- `BINARY_C` should point to the root directory of your binary_c installation
- `LD_LIBRARY_PATH` should include $BINARY_C/src and whatever directories are required to run binary_c (e.g. locations of libgsl, libmemoize, librinterpolate, etc.)
- `LIBRARY_PATH` should include whatever directories are required to build binary_c (e.g. locations of libgsl, libmemoize, librinterpolate, etc.)
- `GSL_DIR` should point to the root location where you installed GSL to. This root dir should contain `bin/`, `lib/` etc

### Installing `binary_c-python`
There are several ways to install `binary_c-python`:

### Installation via PIP:
To install this package via pip:

```
pip install binarycpython
```

This will install the latest stable installation that is available on Pip. The version on the master branch of `binary_c-python` is the same version as the latest stable version on Pip.

### Installation from source:
To install the `binary_c-python` from source, which is useful for development versions and customisation, run

```
./install.sh
```

This will install the package, along with all the dependencies, into the current active (virtual) python environment.

### Use of code without installation
It is possible to use parts of the code without installing it, by adding the root directory of this repo to your `$PYTHONPATH`.

- Download `binary_c-python`, via e.g. `git clone https://gitlab.com/binary_c/binary_c-python.git`
- Add the path to the downloaded repo to your `$PYTHONPATH`, via e.g. `export PYTHONPATH="~/binary_c-python:$PYTHONPATH"`

It will not be possible to actually run systems through `binary_c` though.

## Usage
Instructions on how to use `binary_c-python` are available in the form of [tutorial and example use-case notebooks](https://binary_c.gitlab.io/binary_c-python/example_notebooks.html) in the [online documentation](https://binary_c.gitlab.io/binary_c-python).

The documentation for the latest stable release of `binary_c-python` is available on https://binary_c.gitlab.io/binary_c-python/.

The documentation for `binary_c` is available on https://binary_c.gitlab.io/binary_c.

### Usage notes
Make sure that with every change/recompilation you make in `binary_c`, you also rebuild `binary_c-python`. Whenever you change the source code of this package, you need to re-install it into your virtualenvironment as well.

### Unit tests
After installing `binary_c-python` from source you can run the unit tests to make sure the code works as it should.

There are two suites of unit tests for `binary_c-python`. The first includes only the actual code of the project, and is located at `binarycpython/test/main.py`. The second includes only the tutorial and example notebooks, and is located at `python binarycpython/tests/test_notebooks.py`.

## Development:
If you want to contribute to the code, then it is recommended that you install the packages in `development_requirements.txt`:

```
pip install -r development_requirements.txt
```

Please do not hesitate to contact us to discuss any contribution. Please see `HOW_TO_CONTRIBUTE`.

Some useful commands to generate documentation and coverage reports are stored in the `commands/` directory.

We use the following naming convention for development and release branches:

```
development/<binary_c-python version>/<binary_c version>
releases/<binary_c-python version>/<binary_c version>
```

### Generating documentation
To build the documentation manually, run

```
./generate_docs.sh
```

from within the `commands/` directory. Note: this requires `pandoc` to be installed on your machine.

### Generating docstring and test coverage report
To generate the unit test and docstring coverage report, run

```
./generate_reports.sh
```

from within the `commands/` directory.

## JOSS paper
We've written a JOSS paper for `binary_c-python`, which is stored in [papers/joss/paper.pdf](https://gitlab.com/binary_c/binary_c-python/-/blob/master/papers/joss/paper.pdf).

Paper review status:
[![status](https://joss.theoj.org/papers/7c43806e6d1f82c2945e12ae500f03b2/status.svg)](https://joss.theoj.org/papers/7c43806e6d1f82c2945e12ae500f03b2)


## FAQ/Issues:
If you encounter an issue with the code, or if you want to suggest extra features or changes in the code, please submit an issue at https://gitlab.com/binary_c/binary_c-python/-/issues/new.

Here we provide a non-exhaustive list of some issues we encountered and solutions for these:

Building issues with binary_c itself:
- see the documentation of binary_c (in doc/).
- If you have MESA installed, make sure that the `$MESASDK_ROOT/bin/mesasdk_init.sh` is not sourced. It comes with its own version of some programs, and those can interfere with installing.

When Pip install fails:
- Run the installation with `-v` and/or `--log <logfile>` to get some more info
- If gcc throws errors like `gcc: error: unrecognized command line option ‘-ftz’; did you mean ‘-flto’?`, this might be due to that the python on that system was built with a different compiler. It then passes the python3.6-config --cflags to the binarycpython installation, which, if done with gcc, will not work. Try a different python3.6. I suggest using `pyenv` to manage python versions. If installing a version of python with pyenv is not possible, then try to use a python version that is avaible to the machine that is built with the same compiler as binary_c was built with.
- if pip installation results in `No files/directories in /tmp/pip-1ckzg0p9-build/pip-egg-info (from PKG-INFO)`, try running it verbose (`-v`) to see what is actually going wrong.
- If pip terminates with the error FileNotFoundError: [Errno 2] No such file or directory: '<...>/binary_c-config' Then make sure that the path to your main $BINARY_C directory is set correctly.

Other:
- When running jupyter notebooks, make sure you are running the jupyter installation from the same virtual environment.
- When the output of binary_c seems to be different than expected, you might need to rebuild this python package. Everytime binary_c is compiled, this package needs to be rebuilt too.
