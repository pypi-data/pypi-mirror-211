from setuptools import find_packages, setup

setup(
    name="Aehold",
    version="0.1.3",
    packages=find_packages(include=["Aehold", "Aehold.*"]),
    description="XML & JSON serializator.""",
    author="Me",
    license="MIT",
    entry_points={
        'console_scripts': ['aehold=aehold.lib:main']
    }
)