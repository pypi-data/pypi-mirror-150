from setuptools import setup, find_packages

with open('backend/requirements.txt') as file:
    requirements = [line.strip() for line in file.readlines()]

setup(
    name="personal_site-msilvasy",
    version="1.0.5",
    description="Vue.js, Nuxt.js, Django, Django Rest Framework and PostgreSQL personal project",
    author="Mike Silvasy",
    author_email="mike.silvasy@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "backend=backend.manage:main",
        ]
    },
    url="http://mikesilvasy.com",
)
