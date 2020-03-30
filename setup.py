import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="project-euler-scraper", # Replace with your own username
    version="0.0.1",
    author="Pierre Palud",
    author_email="paludpierre@hotmail.fr",
    description="A scraper for Project Euler Problems data and User Progression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pierrePalud/project-euler-scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires
)