import re
from setuptools import setup


requirements = [
    "certifi==2021.10.8",
    "charset-normalizer==2.0.12",
    "idna==3.3",
    "requests==2.27.1",
    "urllib3==1.26.9"
]

version = ""
with open("touka/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Version is not set.")

readme = ""
with open("README.rst") as f:
    readme = f.read()

packages = [
    "touka",
    "touka.ext"
]

setup(
    name="touka",
    author="Black Reaper",
    project_urls={
        "Discord": "https://discord.gg/yzAJ3wg5S3"
    },
    version=version,
    packages=packages,
    license="MIT",
    description="A Python wrapper for automation.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.10.0,<4.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Other Audience",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Home Automation",
        "Topic :: Utilities",
        "Typing :: Typed",
    ]
)