from setuptools import find_packages, setup

name = 'torchdevice'

setup(
    name=name,
    version='0.2.0',
    packages=[package for package in find_packages() if package.startswith(name)],
    url=f'https://github.com/speedcell4/{name}',
    license='MIT',
    author='speedcell4',
    author_email='speedcell4@gmail.com',
    python_requires='>=3.9',
    description='',
    install_requires=[
        'torch',
        'filelock',
    ],
    extras_require={
        'dev': [
            'pytest',
            'hypothesis',
        ],
    }
)
