import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    ld = f.read()
setuptools.setup(
    name='tongsmath',
    version='1.2.0',
    author='Tong',
    author_email='3231690635@qq.com',
    description='Tong\'s exclusive math library contains some junior high school math functions',
    long_description=ld,
    long_description_content_type='text/markdown',
    url='https://github.com/',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
