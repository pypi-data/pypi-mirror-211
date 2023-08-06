from setuptools import find_packages, setup

setup(
    name="AeholdSerializer",
    version="0.2.3",
    packages=find_packages(include=["AeholdSerializer", "AeholdSerializer.*"]),
    description="XML & JSON serializator.""",
    author="Me",
    license="MIT",
    entry_points={
        'console_scripts': ['aehold=AeholdSerializer.lib:main']
    }
)