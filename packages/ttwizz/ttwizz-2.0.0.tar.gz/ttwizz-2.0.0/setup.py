from setuptools import setup, find_packages

def README():
    with open("README.md", "r") as file:
        return file.read()

setup(
    name = "ttwizz",
    version = "2.0.0",
    author = "ttwiz_z",
    author_email = "moderkascriptsltd@gmail.com",
    description = "Registers an always-on web server.",
    long_description = README(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/ttwizz",
    packages = find_packages(),
    install_requires = ["Flask>=1.1.2"],
    classifiers = [
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords = "ttwizz",
    project_urls = {
        "Organization": "https://github.com/ModerkaScripts"
    },
    python_requires = ">=3.8"
)