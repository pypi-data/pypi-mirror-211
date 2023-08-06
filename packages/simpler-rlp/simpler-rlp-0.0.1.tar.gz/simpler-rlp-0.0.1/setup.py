from setuptools import setup

with open('README.md', 'r') as readme_file:
    README = readme_file.read()

setup(
    name='simpler-rlp',
    version='0.0.1',
    packages=['simpler_rlp'],
    url='https://github.com/kristian1108/simple-rlp',
    license='MIT Custom',
    author='Kristian Gaylord',
    author_email='krlgaylord@gmail.com',
    description='RLP (Recursive Length Prefix) - Encode and decode data structures',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6'
)
