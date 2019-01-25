## ISO19115-3Creator

This Python script is used to crawl a specified directory, search for files (raster, vector, LAS) with a specified file extension and automatically create ISO19115-3 compliant XML Metadata files. Due to the limited information that can be automatically extracted from the files the Metadata entries are constrained and several default values are set.

The script was written to automatically create .xml-files for the upload and use with the Geonetwork CSW-Server from an existing filestructure. The goal is the help organize unstructured geodata and to make the search and discovery of certain datasets easier.

### Getting started

There is no package available as for now. The best way to get started is to use [Anaconda](https://www.anaconda.com/) and create a new **Python 3** environment. Clone the repository 

```
git clone https://github.com/AlexZeller/ISO19115-3Creator.git

```

and install the required packages inside the new environemnt. The requirements are:

>[halo](https://github.com/manrajgrover/halo)

>[sridentify](https://github.com/cmollet/sridentify)

>[pyproj](https://github.com/jswhit/pyproj)

>[OWSLib](https://github.com/geopython/OWSLib)

>[GDAL](https://github.com/OSGeo/gdal)

>[PDAL](https://github.com/PDAL/PDAL)

### Explanation

The `main.py` contains an example configuration.

To initiate the crawler create an instance of the `metacrawler.Crawler()` class. The Arguments are:

```
rootDir (string): The path of the directory to be crawled. 
defaultValues (list): A list of certain default values for the xml. 
CSW_URL (string): The URL of the Geonetwork CSW publication server.
username (string): The username to authenticate with.
password (string): The password of the user.
upload (Boolean): Specify wheather to upload the file to Geonetwork or not.
```
