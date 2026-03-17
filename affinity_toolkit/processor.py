import json
from pathlib import Path
from typing import Dict, Any, List, Callable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class AffinityPhotoProcessor:
    def __init__(self, client: 'AffinityPhotoClient'):
        """
        Initializes the AffinityPhotoProcessor with a given client.

        Args:
            client (AffinityPhotoClient): An instance of AffinityPhotoClient.
        """
        self.client = client

    def process_file(self, path: Path) -> Dict[str, Any]:
        """
        Processes a single Affinity Photo file to extract relevant information.

        Args:
            path (Path): The path to the Affinity Photo file.

        Returns:
            Dict[str, Any]: A dictionary containing extracted data.
        """
        try:
            logging.info(f"Processing file: {path}")
            text = self.extract_text(path)
            metadata = self.extract_metadata(path)
            return {
                "text": text,
                "metadata": metadata
            }
        except Exception as e:
            logging.error(f"Error processing file {path}: {e}")
            return {}

    def extract_text(self, path: Path) -> str:
        """
        Extracts text from a given Affinity Photo file.

        Args:
            path (Path): The path to the Affinity Photo file.

        Returns:
            str: Extracted text from the file.
        """
        try:
            # Simulate text extraction logic
            logging.info(f"Extracting text from: {path}")
            with open(path, 'r') as file:
                content = file.read()
            # This is a simplified example; actual extraction logic will vary
            return content.split('\n')[0]  # Return the first line as example text
        except Exception as e:
            logging.error(f"Error extracting text from {path}: {e}")
            return ""

    def extract_metadata(self, path: Path) -> Dict:
        """
        Extracts metadata from a given Affinity Photo file.

        Args:
            path (Path): The path to the Affinity Photo file.

        Returns:
            Dict: A dictionary containing metadata.
        """
        try:
            logging.info(f"Extracting metadata from: {path}")
            # Simulate metadata extraction logic
            metadata = {
                "filename": path.name,
                "size": path.stat().st_size,
                "last_modified": path.stat().st_mtime
            }
            return metadata
        except Exception as e:
            logging.error(f"Error extracting metadata from {path}: {e}")
            return {}

    def batch_process(self, paths: List[Path], progress_callback: Callable[[int], None] = None) -> List[Dict]:
        """
        Processes a list of Affinity Photo files in batch.

        Args:
            paths (List[Path]): A list of paths to the Affinity Photo files.
            progress_callback (Callable[[int], None], optional): A callback function to report progress.

        Returns:
            List[Dict]: A list of dictionaries containing extracted data from each file.
        """
        results = []
        for index, path in enumerate(paths):
            result = self.process_file(path)
            results.append(result)
            if progress_callback:
                progress_callback(index + 1)
        return results
