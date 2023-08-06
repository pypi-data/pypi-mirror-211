from setuptools import setup

with open('README.md', 'r') as fh:
    readme = fh.read()

setup(
    name='hecho-events',
    version='1.2.1',
    license='MIT License',
    author='Compasso UOL',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='hecho.teste@outlook.com',
    keywords='Pacote hecho',
    description='Event Broker Rasa',
    packages=['hecho_events'],
    package_data={'': ['.env']},
    dependency_links=['https://pypi.org/project/aiohttp'],
    install_requires=['aiohttp>=3.8.1'],
)
