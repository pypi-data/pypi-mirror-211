import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='udm-toolbox',
    version='0.0.1',
    author='Yiran Ji',
    author_email='yiranji@zju.edu.cn',
    description='A urban drainage model toolbox',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/Jistill/UDM-toolbox',
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",

                 "License :: OSI Approved :: MIT License",

                 "Operating System :: OS Independent", ],
    python_requires='>=3.10'
)
