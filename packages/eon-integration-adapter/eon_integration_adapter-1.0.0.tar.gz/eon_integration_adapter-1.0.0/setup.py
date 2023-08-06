from setuptools import setup, find_packages
setup(
    name='eon_integration_adapter',
    version='1.0.0',
    license='MIT',
    author="Ahmad Salameh",
    author_email='a.salameh@eonaligner.com',
    packages=find_packages("src"),
    package_dir={'': 'src'},
    url='https://bitbucket.org/eon-mes/broker_utilities/src/master',
    keywords='eon broker project',
    install_requires=[
        "python-magic==0.4.27",
        "requests==2.25.1",
        "aio_pika==8.3.0"
      ],

)