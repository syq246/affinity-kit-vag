"""
Affinity Photo for Windows Toolkit - Python automation and utilities

A comprehensive toolkit for working with Affinity Photo for Windows files and automation.
"""
from .client import AffinityPhotoClient
from .processor import AffinityPhotoProcessor
from .metadata import AffinityPhotoMetadataReader
from .batch import BatchProcessor
from .exporter import DataExporter

__version__ = "0.1.0"
__author__ = "Open Source Community"

__all__ = [
    "AffinityPhotoClient",
    "AffinityPhotoProcessor",
    "AffinityPhotoMetadataReader",
    "BatchProcessor",
    "DataExporter",
]
