from setuptools import find_packages, setup
from UDPeep.__version__ import VERSION


with open("README.md") as file:
    setup(
        name="UD Peep",
        license="GPLv3",
        description="Search for secrets inside user data attached to EC2 \
            instances on multiple AWS accounts",
        long_description=file.read(),
        author="Akhil Reni",
        version=VERSION,
        author_email="akhil@wesecureapp.com",
        url="https://strobes.co/",
        python_requires='>=3.6',
        install_requires=["boto3==1.16.10"],
        packages=find_packages(
            exclude=('test')),
        package_data={
            'UDPeep': [
                '*.txt',
                '*.json']},
        entry_points={
            'console_scripts': ['ud_peep = UDPeep.ud_peep:main']},
        include_package_data=True)
