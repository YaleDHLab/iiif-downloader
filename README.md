# Note: This repository has been archived
This project was developed under a previous phase of the Yale Digital Humanities Lab. Now a part of Yale Library’s Computational Methods and Data department, the Lab no longer includes this project in its scope of work. As such, it will receive no further updates.


# IIIF Downloader

> A simple utility for downloading images from IIIF servers

## Installation

```bash
pip install iiif_downloader
```

## Usage

```bash
from iiif_downloader import Manifest

Manifest(url='https://manifests.britishart.yale.edu/manifest/46796').save_images()
```
