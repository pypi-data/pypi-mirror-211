from setuptools import find_packages, setup
setup(
    name='pointa-to-pointb',
    packages=find_packages(include=['pointa-to-pointb']),
    version='0.1.0',
    description='Python library to calculate accurate distance between Point A and Point B in a given context or setup. It currently supports only geo-spatial distances and euclidean distances',
    author='Shashank Sahoo',
    license='MIT',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)