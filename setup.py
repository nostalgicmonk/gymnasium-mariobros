"""The setup script for installing the package."""
from setuptools import setup, find_packages


# read the contents of the README
with open('README.md', encoding='utf-8') as README_md:
    README = README_md.read()


setup(
    name='gymnasium-mariobros',
    version='1.0.1',
    description='Super Mario Bros. for Gymnasium',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords=' '.join([
        'Gymnasium',
        'NES',
        'Super-Mario-Bros',
        'Lost-Levels',
        'Reinforcement-Learning-Environment',
    ]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: Free For Educational Use',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    url='https://github.com/Kautenja/gym-super-mario-bros',
    author='joker001',
    license='Proprietary',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    package_data={ 'gymnasium_mariobros': ['_roms/*.nes'] },
    install_requires=['cynes>=0.1.0', 'gymnasium>=0.26.0', 'numpy>=2.0.0', 'pygame>=2.6.0'],
    entry_points={
        'console_scripts': [
            'gymnasium_mariobros = gymnasium_mariobros._app.cli:main',
        ],
    },
)
