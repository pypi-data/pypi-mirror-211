from setuptools import find_packages, setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="blenderline",
    version="0.1.1",
    description="A pipeline for generating synthetic production line images",
    packages=find_packages(exclude=["examples*", "data*"]),
    include_dirs=[
        "img",
        "examples",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaxvandenHoven/blenderline",
    author="Max van den Hoven",
    author_email="max.hoven@gmail.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "blender-stubs>=3.12.27",
        "bpy>=3.5.0",
    ],
    extras_require={
        "dev": [
            "black>=23.3.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "twine>=4.0.2",
        ],
    },
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "blenderline = blenderline.command_line:cli",
        ],
    },
)
