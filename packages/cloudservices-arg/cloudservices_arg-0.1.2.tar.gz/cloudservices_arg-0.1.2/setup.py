
from setuptools import setup, find_packages

setup(
    name='cloudservices_arg',
    version='0.1.2',
    description='A sample Python project for rach pack',
    author='Rac',
    author_email='rachitmahajan6399@gmail.com',
    url='https://github.com/r-mhjn/QuizCreator',
    packages=['cloudservices_arg'],
    install_requires=['google-auth==2.17.3','google-cloud-pubsub==2.13.0','boto3==1.14.60','botocore==1.17.60','apache-libcloud==3.7.0','PyPubSub==4.0.3'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)