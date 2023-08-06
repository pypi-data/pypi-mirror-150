# encoding: utf-8
from setuptools import setup, find_packages


setup(
    name='mosaik-simpy-io',
    version='0.2.4',
    author='mosaik',
    author_email='mosaik@offis.de',
    description='Asynchronous networking based on SimPy.',
    long_description=(open('README.rst', encoding='utf-8').read() + '\n\n' +
                      open('CHANGES.txt', encoding='utf-8').read() + '\n\n' +
                      open('AUTHORS.txt', encoding='utf-8').read()),
    url='https://gitlab.com/mosaik/tools/simpy.io',
    license='MIT License',
    install_requires=[
        'SimPy>=3.0.9,<4.0',
    ],
    packages=['simpy.io'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Networking',
    ],
)
