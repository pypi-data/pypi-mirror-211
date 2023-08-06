from setuptools import setup

setup(
    name='CP-Teams-webhook',
    version='0.1.0',
    description='Python library for sending notifications to Microsoft Teams webhooks',
    long_description='Long description of your package',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourusername/your-package',
    py_modules=['SendTeams'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)