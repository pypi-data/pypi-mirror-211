from setuptools import setup
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gauth",
    version="1.0.2",
    license='MIT',
    description="Tool to help migrate Google Authenticator from phone to desktop",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Damon Yuan",
    author_email="damon.yuan.dev@gmail.com",
    url="https://github.com/damonYuan/gauth",
    packages=['gauth'],
    entry_points="""
    [console_scripts]
    gauth = gauth.main:main
    """,
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)