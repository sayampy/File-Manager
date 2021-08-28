from setuptools import setup, find_packages

setup(
    name='File-Manager-Cli',
    version='0.1.0',
    author='sayampy',
    install_requires=[
        'Click',
        'seedir',
    ],
    url='https://github.com/sayampy/File-Manager',
    packages=find_packages(),
    entry_points="""
         [console_scripts]
          fmc = fima.main:main""",
)
