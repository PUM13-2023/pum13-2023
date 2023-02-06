import nox


@nox.session(venv_backend="none")
def fmt_check(s: nox.Session) -> None:
    s.run("isort", "--check", ".")
    s.run("black", "--check", ".")


@nox.session(venv_backend="none")
def lint(s: nox.Session) -> None:
    s.run("pflake8", "--color", "always")


@nox.session(venv_backend="none")
def type_check(s: nox.Session) -> None:
    s.run("mypy", "src", "noxfile.py")


@nox.session(venv_backend="none")
def test(s: nox.Session) -> None:
    s.run("pytest", "--cov")
    s.run("coverage", "report")
    s.run("coverage", "xml")
