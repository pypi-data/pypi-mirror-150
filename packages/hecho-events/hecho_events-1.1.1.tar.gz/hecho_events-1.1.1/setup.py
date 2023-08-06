from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='hecho_events',
    version='1.1.1',
    license='MIT License',
    author='Compasso UOL',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='hecho.teste@outlook.com',
    keywords='Pacote hecho',
    description=u'Event Broker Rasa',
    packages=['hecho'],
    package_data={'': ['.env']},
    dependency_links=['https://pypi.org/project/requests'],
    install_requires=['python-decouple', 'requests>=2.20']
)
