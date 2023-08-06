from setuptools import find_packages, setup

setup(
    name='cgdb_client',
    packages=find_packages(include=["cgdb"]),
    version='0.1.2',
    install_requires=["pandas==1.1.5"],
    description='CGDB Client',
    author='CzechGlobe',
    license='MIT',
)
