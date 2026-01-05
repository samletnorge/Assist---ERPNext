from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="erpnext_assist",
    version="0.0.1",
    description="ERPNext Assist - AI-powered tools for extending ERPNext with MCP integration",
    author="samletnorge",
    author_email="",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
