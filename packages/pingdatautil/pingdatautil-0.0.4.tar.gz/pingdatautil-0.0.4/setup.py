from setuptools import setup, find_packages

setup(
    name="pingdatautil",
    version="0.0.4",
    author="Vorapol Ping",
    description="Ping's Data Utility Package",
    packages=find_packages(exclude=["test", "test*", "test-.*", "tests"]),
    install_requires=[
        "pyodbc >= 4.0.0",
        "jaydebeapi >= 1.2.3",
        "pandas >= 1.5.0",
        "xlsxwriter >= 3.0.0",
    ]
)
