import nox
import nox_poetry.patch  # noqa
from nox.sessions import Session


@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
def tests(session: Session) -> None:
    session.run("pip", "--version")
    session.run("pip", "install", "pip==20.2.4")
    session.run("poetry", "lock")
    session.run("echo", "'after lock'", external=True)
    session.install(".")
    session.install("docker")

    if session.python in ["3.6", "3.7"]:
        session.install("typing-extensions")
        session.install("aiounittest")

    session.run("python", "-m", "unittest")
