# This is the setup.py for module abstract_utilities_test
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='abstract_utilities_test',
    version='0.0.3',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='abstract_utilities_test is a Python package.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/abstract_package_test/abstract_utilities_test',
    packages=find_packages(where="src"),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        "Operating System :: OS Independent",
    ],
    package_dir={"abstract_utilities_test": "src/abstract_utilities_test"},
    python_requires=">=3.6",
    install_requires=[
        # Add your project's requirements here, e.g.,
        # 'numpy>=1.22.0',
        # 'pandas>=1.3.0',
    ],
    include_package_data=True,  # This is to include any data files found inside your packages
    entry_points={
        'console_scripts': [
            "abstract_utilities_test=abstract_utilities_test.main:main"
        ]
    },
)
