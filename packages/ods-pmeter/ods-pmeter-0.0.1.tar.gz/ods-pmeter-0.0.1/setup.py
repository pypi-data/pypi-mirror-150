from importlib_metadata import entry_points
from setuptools import setup, find_packages
setup(
    name='ods-pmeter',
    version='0.0.1',

    long_description = 'file: README.md',

    author = 'Loggers a team for CSE 603 at UB',

    packages = find_packages('src'),

    package_dir={'': 'src'},

    classifiers=(
        "Programming Language :: Python :: 3",

        " Programming Language :: Python :: 3.9"
    ),

    install_requires=[
          'docopt',
          'psutil',
          'tcp-latency',
          'ipping',
          'pyping',
          'py-cpuinfo',
          'pythonping',
          'py3-validate-email',
          'requests',
    ],


    zip_safe = False

)