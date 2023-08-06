from setuptools import find_packages, setup

setup(
    name="ftsnowySerializer",
    version="1.0.0",
    packages=find_packages(include=["MySerializer", "MySerializer.*"]),
    description="Custom-made JSON and XMl Serializer for IGI Lab3.",
    author="Daniil Barkovskiy",
    entry_points={
        'console_scripts': ['MySerializer=MySerializer.lib:main']
    }
)
