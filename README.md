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