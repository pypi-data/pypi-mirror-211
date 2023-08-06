import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="EduSocialMediaDSHelper", # Replace with your own username
    version="0.1.0",
    author="Josh King",
    author_email="joshkking@gmail.com",
    description="Helper for DS Social Media learning material",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Joshkking/EduSocialMediaDSHelper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)