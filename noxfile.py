import nox
import nox_poetry.patch  # noqa
from nox.sessions import Session


@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
def tests(session: Session) -> None:
    session.run("pip", "--version")
    # session.run("pip", "install", "pip==20.2.4")
    session.run("poetry", "lock")
    session.install(".")
    session.install("docker")

    if session.python in ["3.6", "3.7"]:
        session.install("aiounittest")

    session.run("python", "-m", "unittest")


@nox.session(python="3.9")
def coverage(session: Session) -> None:
    session.run("poetry", "lock")
    session.install(".")
    session.install("docker")
    session.install("coverage[toml]")
    session.install("codecov")
    session.run("coverage", "run", "-m", "unittest", "discover")
    session.run("codecov", *session.posargs)
