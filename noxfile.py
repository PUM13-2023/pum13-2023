import nox


@nox.session(tags=["lint"], venv_backend="none")
def fmt_check(s: nox.Session) -> None:
    s.run("isort", "--check", ".")
    s.run("black", "--check", ".")


@nox.session(tags=["lint"], venv_backend="none")
def lint(s: nox.Session) -> None:
    s.run(
        "pflake8", "--color", "always", "--per-file-ignores", "*__init__.py:F401", "src", "tests"
    )


@nox.session(tags=["lint"], venv_backend="none")
def type_check(s: nox.Session) -> None:
    s.run("mypy", "src", "noxfile.py")


@nox.session(tags=["test"], venv_backend="none")
def test(s: nox.Session) -> None:
    s.run("pytest", "--cov", "--junitxml=test_result.xml")
    s.run("coverage", "report")
    s.run("coverage", "xml")
