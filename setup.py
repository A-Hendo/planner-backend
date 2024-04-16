from pathlib import Path

import setuptools

dir = Path("src")
packages = setuptools.find_packages()
setuptools.setup(
    name="Webapp",
    version="0.0.1",
    description="Planner backend",
    url="",
    install_requires=[],
    package_dir={"": str(dir)},
    packages=packages,
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "planner = pixel_planner.main:main",
        ],
    },
)
