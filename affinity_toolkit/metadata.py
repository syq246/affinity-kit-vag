from pathlib import Path
import json
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Metadata:
    title: str
    author: str
    created: str
    modified: str
    description: str

class AffinityPhotoMetadataReader:
    @staticmethod
    def read(path: Path) -> Metadata:
        """
        Reads metadata from a JSON file.

        Args:
            path (Path): The path to the JSON file containing metadata.

        Returns:
            Metadata: An instance of Metadata populated with data from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file is not a valid JSON.
            KeyError: If expected keys are missing from the JSON data.
        """
        if not path.is_file():
            raise FileNotFoundError(f"Metadata file not found: {path}")

        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            return Metadata(
                title=data['title'],
                author=data['author'],
                created=data['created'],
                modified=data['modified'],
                description=data['description']
            )
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON from {path}: {e}")
        except KeyError as e:
            raise KeyError(f"Missing expected key in metadata: {e}")

    @staticmethod
    def write(path: Path, metadata: Metadata) -> bool:
        """
        Writes metadata to a JSON file.

        Args:
            path (Path): The path to the JSON file where metadata will be saved.
            metadata (Metadata): An instance of Metadata to write to the file.

        Returns:
            bool: True if writing was successful, False otherwise.

        Raises:
            IOError: If there is an issue writing to the file.
        """
        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(metadata.__dict__, file, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            raise IOError(f"Error writing to metadata file {path}: {e}")
