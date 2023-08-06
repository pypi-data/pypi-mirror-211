import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-atomic-migrations",
    version='0.2.0',
    author="Richard Kojedzinszky",
    author_email="richard@kojedz.in",
    description="Adds unique constraint on Django's migration tracking model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rkojedzinszky/django-atomic-migrations",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
