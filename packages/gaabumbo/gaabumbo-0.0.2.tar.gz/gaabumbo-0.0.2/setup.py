import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = "gaabumbo"
DESCRIPTION = "Bumbo Python Web Framework built for learning purposes."
EMAIL = "gorbachyow.andrei@yandex.ru"
AUTHOR = "Gorbachyow Andrei"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.2"

# Which packages are required for this module to be executed?
REQUIRED = [
    "attrs==21.4.0",
    "certifi==2021.10.8",
    "gunicorn==20.1.0",
    "idna==3.3",
    "iniconfig==1.1.1",
    "Jinja2==3.1.1",
    "MarkupSafe==2.1.1",
    "mccabe==0.6.1",
    "packaging==21.3",
    "parse==1.19.0",
    "pluggy==1.0.0",
    "py==1.11.0",
    "pycodestyle==2.8.0",
    "pyparsing==3.0.7",
    "pytest==7.1.1",
    "pytest-cov==3.0.0",
    "requests==2.27.1",
    "requests-wsgi-adapter==0.4.1",
    "tomli==2.0.1",
    "urllib3==1.26.9",
    "WebOb==1.8.7",
    "whitenoise==6.0.0",
]

# The rest you shouldn't have to touch too much :)

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=["test_*"]),
    install_requires=REQUIRED,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    setup_requires=["wheel"],
)
