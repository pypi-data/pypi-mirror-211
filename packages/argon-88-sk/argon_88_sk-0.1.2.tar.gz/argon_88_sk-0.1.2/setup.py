from setuptools import find_packages, setup

setup(
    name="argon_88_sk",
    version="0.1.2",
    packages=find_packages(include=["argon_88_sk", "argon_88_sk.*"]),
    description="XML & JSON serialization tools at BSUIR 2023 spring semester.""",
    author="Me",
    license="MIT",
    entry_points={
        'console_scripts': ['argon_88_sk=argon_88_sk.lib:main']
    }
)