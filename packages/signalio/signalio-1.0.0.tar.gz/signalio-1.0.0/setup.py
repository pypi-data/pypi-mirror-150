from setuptools import setup, find_packages

setup(
    name="signalio",
    version="1.0.0",
    description="A simple Python networking package",
    url="https://github.com/suchasaltylemon/Signal-IO",
    author="SuchASaltyLemon",
    author_email="suchasaltylemon@mailbox.org",
    packages=find_packages("signalio"),
    package_dir={"": "signalio"}
)
