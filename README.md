# GraphIt Dashboard

GraphIt Dashboard is a data visualization platform developed for a bachelor
project in software engineering. The project is written in Python using the
Dash framework.

## Table of Contents

- [Installation](#installation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Project structure](#project-structure)
- [Enforcing Code Quality](#enforcing-code-quality)
- [Dependencies](#dependencies)

## Installation

The below installation instruction is platform-specific. The first command is
creating a virtual environment named venv and upgrading the dependencies with
`--upgrade-deps` flag. Then activate the virtual environment with
`venv\Scripts\activate` command in windows and source `venv/bin/activate` in
linux/macOS. Finally, it is installing the package in editable mode along with
the development dependencies.

### Windows

```powershell
python -m venv venv --upgrade-deps
venv/Scripts/activate
pip install -e .[dev]
```

### Linux / macOS

```bash
python -m venv venv --upgrade-deps
source venv/bin/activate
pip install -e '.[dev]'
```

> Note: The `-e` flag installs the project in *edit* mode, meaning that the installed
> package refers to the project source directory. Omiting this flag results in
> hard-to-find bugs as changes to the code are not applied as expected.

### Tailwind CLI

This project uses Tailwind CLI which generates css code for your tailwind syntax.
To setup tailwind CLI on your machine follow this guide.
https://tailwindcss.com/blog/standalone-cli
Notable change from the guide is:
input.css is tailwind.css.
output.css is dashboard.css.


> Note: tailwind CLI will not continually update the css as you code  like CDN did before
> unless you use a watch.

## Deployment
This section will describe how you deploy the GraphIt dashboard locally on your own computer or containerized using Docker and Nginx.

### Locally
Follow the installation guide for your system then run the main python file located in src/dashboard/. This can be done with the command below while in your virtual environment.
```bash
python -m dashboard.main
```

### Docker containerized

To run the GraphIt dashboard application using Docker, Gunicorn and Nginx. Start the Docker daemon and go to the root directory and use the command below.

```bash
docker compose up --build
```

This command will create two separate Docker containers, one for the dashboard and one for Nginx and run it on your machine.

### Environment
The project uses a `.env` file to store various project configuration. This is to avoid commiting potentially sensitive information to GitHub. Creating this file is needed for running the project. Example:
```bash
DB_URL=mongodb://...
SECRET_KEY=...
```

`DB_URL` stores the mongodb database url of the database url.
`SECRET_KEY` is a secret token that is used by Flask to encrypt session tokens. https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY

## Contributing
For information on how to contribute, see [`CONTRIBUTING.md`](./CONTRIBUTING.md)

## Project structure

The dashboard source code is found in [`src/dashboard`](./src/dashboard/).
The web dashboard uses pages, which are found in
[`src/dashboard`](./src/dashboard/pages/). The project uses the MVC
architecture. Each page has its view and controller in its corresponding
directory. Each view page must register itself like following.
```python
dash.register_page(__name__) # or any other suitable path
```
For more information see [Dash documentation](https://dash.plotly.com/urls).

Models are shared between pages and reside in the
(`models`)[./src/dashboard/models] directory.

Reusable components reside in the (`components`)[./src/dashboard/components]
directory.

```
├── src
│   └── dashboard
│       ├── components
│       │   ├── __init__.py
│       │   └── ...
│       ├── models
│       │   ├── __init__.py
│       │   └── ...
│       ├── pages
│       │   ├── index
│       │   │   ├── controller.py
│       │   │   └── index.py
│       │   └── ...
│       ├── static
│       │   ├── style.css
│       │   └── ...
│       ├── __init__.py
│       └── main.py
├── tests
│   ├── test_dashboard.py
│   └── ...
├── README.md
├── noxfile.py
└── pyproject.toml
```

## Enforcing Code Quality

Automated code quality checks are performed using
[Nox](https://nox.thea.codes/en/stable/). Nox will automatically run commands
based on the [`noxfile.py`](./noxfile.py) for unit testing, PEP 8 style guide
checking, type checking and documentation generation.

> Note: `nox` is installed into the virtual environment automatically when you
> follow the installation instructions the above.

### Unit Testing

Unit testing is performed with [pytest](https://pytest.org/). pytest has become
the de facto Python unit testing framework. Some key advantages over the
built-in [unittest](https://docs.python.org/3/library/unittest.html) module are:

1. Significantly less boilerplate is needed for tests.
2. PEP 8 compliant names (e.g. `pytest.raises()` instead of
   `self.assertRaises()`).
3. Vibrant ecosystem of plugins.

pytest will automatically discover and run tests by recursively searching for
folders and `.py` files prefixed with `test` for any functions prefixed by
`test`.

The `tests` folder is created as a Python package (i.e. there is an
`__init__.py` file within it) because this helps `pytest` uniquely namespace the
test files. Without this, two test files cannot be named the same, even if they
are in different subdirectories.

Code coverage is provided by the
[pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) plugin.

pytest and code coverage are configured in [`pyproject.toml`](./pyproject.toml).

To pass arguments to `pytest` through `nox`:

```bash
nox -s test -- -k invalid_factorial
```

### Code Style Checking

[PEP 8](https://peps.python.org/pep-0008/) is the universally accepted style
guide for Python code. PEP 8 code compliance is verified using
[Flake8](http://flake8.pycqa.org/). Flake8 is configured in the `[tool.flake8]`
section of `pyproject.toml`. Extra Flake8 plugins are also included:

- `flake8-bugbear`: Find likely bugs and design problems in your program.
- `flake8-broken-line`: Forbid using backslashes (`\`) for line breaks.
- `flake8-comprehensions`: Helps write better `list`/`set`/`dict`
  comprehensions.
- `pep8-naming`: Ensure functions, classes, and variables are named with correct
  casing.
- `flake8-pyproject`: Allow configuration of `flake8` through `pyproject.toml`.

To lint code, run:

```bash
nox -s lint
```

### Automated Code Formatting

Code is automatically formatted using [black](https://github.com/psf/black).
Imports are automatically sorted and grouped using
[isort](https://github.com/PyCQA/isort/).

These tools are configured by:

- [`pyproject.toml`](./pyproject.toml)

To automatically format code, run:

```bash
nox -s fmt
```

To verify code has been formatted, such as in a CI job:

```bash
nox -s fmt_check
```

### Type Checking

[Type annotations](https://docs.python.org/3/library/typing.html) allows
developers to include optional static typing information to Python source code.
This allows static analyzers such as [mypy](http://mypy-lang.org/),
[PyCharm](https://www.jetbrains.com/pycharm/), or
[Pyright](https://github.com/microsoft/pyright) to check that functions are used
with the correct types before runtime.

Editors such as
[PyCharm](https://www.jetbrains.com/help/pycharm/type-hinting-in-product.html)
and VS Code are able to provide much richer auto-completion, refactoring, and
type checking while the user types, resulting in increased productivity and
correctness.

```python
def factorial(n: int) -> int:
    ...
```

mypy is configured in [`pyproject.toml`](./pyproject.toml). To type check code,
run:

```bash
nox -s type_check
```

See also
[awesome-python-typing](https://github.com/typeddjango/awesome-python-typing).

### Nox tags
To run linter, format check and type check run:
```bash
nox -t lint
```

# Dependabot

Including Dependabot in our Python template means that Dependabot will
automatically check for updates to the dependencies of our project and create
pull requests with the updated dependency versions.

By using Dependabot, we can ensure that our dependencies are always up to date
and that any security vulnerabilities are quickly addressed. When Dependabot
finds an update, it will create a pull request with the updated dependency
versions, along with information such as the version numbers and a summary of
any relevant changes or security vulnerabilities that have been fixed in the
update.

You and our team can review and test the updates before merging them into our
codebase, so you can be sure that everything is working as expected. Dependabot
can be configured to check for updates on a schedule (e.g., daily or weekly),
and can also be configured to only create pull requests for certain types of
updates (e.g., security updates) or for certain dependencies. By automating this
process, you can save time and effort on dependency management, and free up time
for other important tasks.

## Dependencies

`pyproject.toml` is a file used to define metadata for a Python project. It is
used by the Python Package Index (PyPI) to distribute and manage packages. The
file follows the TOML (Tom's Obvious, Minimal Language) format, which is a
human-readable format for specifying configuration settings. The file contains
information about the package's dependencies, as well as other metadata such as
the package's name, version, and author.

This file replaces the `setup.py` and `setup.cfg` files used in older Python
packaging systems. With `pyproject.toml`, it's possible to specify what version
of the Python Interpreter or build tools are required for the package, and also
the package's dependencies, along with various other package-specific
information like license, description, etc
