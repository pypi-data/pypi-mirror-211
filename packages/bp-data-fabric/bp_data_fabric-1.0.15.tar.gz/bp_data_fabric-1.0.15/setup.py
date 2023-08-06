import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="bp_data_fabric",
    version="1.0.15",
    author="Bluepineapple",
    author_email="avinash@bluepineapple.io",
    description="",    
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8.10",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.20.0",
        "bp-query-tool >= 0.0.3",
        "bp-data-grid >= 0.0.9",
        "bp-data-visualization >= 0.0.9",
    ],
)
