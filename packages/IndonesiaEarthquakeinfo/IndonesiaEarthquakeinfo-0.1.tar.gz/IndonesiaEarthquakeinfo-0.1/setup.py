import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IndonesiaEarthquakeinfo",
    version="0.1",
    author="Muhammad Maulana B.",
    author_email="muhammadmaulanabdz@gmail.com",
    description="This package informs about the latest earthquake from Meteorology Climatology and "
                "Geophysics Agency(BMKG)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bravelid/latestinformation-earthquake-indonesia",
    project_urls={
        "Github": "https://github.com/Bravelid/latestinformation-earthquake-indonesia",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",

    ],
    # package_dir={"": "src"},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
