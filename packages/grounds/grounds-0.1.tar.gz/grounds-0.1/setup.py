from pathlib import Path

from setuptools import Extension, setup, find_packages

ROOT = Path(__file__).parent
SRC_DIR = "src"


def mk_ext_from_ext_path(ext_path: Path):
    return Extension(str(ext_path.relative_to(ROOT / SRC_DIR))[:-4].replace("/", "."), [str(ext_path)])


extensions = [mk_ext_from_ext_path(f) for f in (ROOT / SRC_DIR).rglob("*.pyx")]

with (ROOT / "requirements.txt").open("r") as f:
    requirements = [
        line.strip()
        for line in f.readlines()
        if not line.startswith("#")
    ]

with (ROOT / "README.md").open("r") as f:
    README = f.read()

setup(
    name="grounds",
    version="0.1",
    description="Fast entropy coder for Python",
    author="KLZ-0",
    author_email="adrian@kalazi.com",
    url="https://github.com/KLZ-0/grounds/",
    packages=find_packages(ROOT / SRC_DIR),
    install_requires=requirements,
    package_dir={"": SRC_DIR},
    ext_modules=extensions,
    python_requires=">=3.6",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["grounds=grounds.__main__:main"],
    },
)
