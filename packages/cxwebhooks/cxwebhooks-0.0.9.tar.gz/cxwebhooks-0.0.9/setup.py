import setuptools

PROJECT_NAME = 'cxwebhooks'

params = dict(
    name = PROJECT_NAME,
    version = '0.0.9',
    author = 'Yvan J. Aquino',
    author_email = 'yvanjaquino@gmail.com',
    scripts = [],
    url = 'https://www.cloud-colosseum.net',
    license = 'LICENSE.txt',
    description = "Dialogflow CX Webhook object classes.",
    install_requires =[
        "pydantic >= 1.8.2"
    ],
    package_dir = {PROJECT_NAME: 'cx-webhooks'},
    packages=[PROJECT_NAME],
    python_requires = ">=3.6"
)

setuptools.setup(**params)
