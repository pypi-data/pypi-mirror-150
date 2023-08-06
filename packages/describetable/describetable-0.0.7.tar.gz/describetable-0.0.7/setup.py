import json
import os
from setuptools import setup


with open('package.json') as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    install_requires=[],
    classifiers = [
        'Framework :: Dash',
    ],
    long_description="A very simple input for Pandas.describe() method. The size and layout should work out of the box but the colors were designed with the plotly 'plasma' scheme in mind, but everything except the most critical should be easily overwritten without the !important flag./ ## Example Usage/ import describetable.Describetable as dTable/ dTable(id=\"innercontainerId\", data=df.describe().to_html(), buttonText='Click to unfold')",
    long_description_content_type="text/markdown",
)
