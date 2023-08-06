import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    ld = f.read()
setuptools.setup(
    name='tongsmath',
    version='1.2.1',
    author='Tong',
    author_email='3231690635@qq.com',
    description='The new version of tongsmath',
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
