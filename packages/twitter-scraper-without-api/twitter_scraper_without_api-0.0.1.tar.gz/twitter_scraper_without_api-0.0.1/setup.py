from setuptools import setup
import setuptools

#with open("README.MD", "r", encoding="utf-8") as fh:
#    long_description = fh.read()


setup(
    name='twitter_scraper_without_api',
    version='0.0.1',
    license='',
    author='Hamed',
    author_email='hamed.minaei@gmail.com',
    description='twitter_scraper without API',
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="https://github.com/HamedMinaeizaeim/twitter_scraper",
    project_urls={
        "Bug Tracker": "https://github.com/HamedMinaeizaeim/twitter_scraper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
