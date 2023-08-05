from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='slf4py',
    version='0.0.2',
    author='taiyo tamura',
    author_email='gtaiyou24@gmail.com',
    description='Simple Logging Facade for Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(where="src"),
    package_dir={"": "src"}
)
