from setuptools import setup, find_packages

setup(
    name="inventory-simulator",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'streamlit>=1.31.0',
        'plotly>=5.18.0',
        'pandas>=2.2.0',
        'numpy>=1.26.3',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="An interactive inventory management simulation tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/inventory-simulator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)