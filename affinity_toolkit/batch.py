import concurrent.futures
from pathlib import Path
from typing import List, Callable, Optional
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

@dataclass
class Result:
    path: Path
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

class BatchProcessor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def process_directory(self, path: Path, pattern: str = "*") -> List[Result]:
        """Process all files in the given directory that match the pattern."""
        results = []
        try:
            files = list(path.glob(pattern))
            logging.info(f"Found {len(files)} files in {path} matching pattern '{pattern}'")
            results = self.process_files(files)
        except Exception as e:
            logging.error(f"Error processing directory {path}: {e}")
            results.append(Result(path, False, error=str(e)))
        return results

    def process_files(self, paths: List[Path], callback: Optional[Callable] = None) -> List[Result]:
        """Process a list of files concurrently."""
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {executor.submit(self.process_file, path, callback): path for path in paths}
            for future in concurrent.futures.as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logging.error(f"Error processing file {path}: {e}")
                    results.append(Result(path, False, error=str(e)))
        return results

    def process_file(self, path: Path, callback: Optional[Callable] = None) -> Result:
        """Process a single file and return a Result."""
        try:
            logging.info(f"Processing file: {path}")
            # Placeholder for actual file processing logic
            data = self.extract_data_from_file(path)
            success = True
            if callback:
                callback(path, data)
            return Result(path, success, data)
        except Exception as e:
            logging.error(f"Error processing file {path}: {e}")
            return Result(path, False, error=str(e))

    def extract_data_from_file(self, path: Path) -> dict:
        """Extract data from the given file."""
        # Simplified example of file data extraction
        data = {
            "filename": path.name,
            "size": path.stat().st_size,
            "extension": path.suffix
        }
        return data

# Example usage:
# if __name__ == "__main__":
#     processor = BatchProcessor(max_workers=4)
#     results = processor.process_directory(Path("path/to/directory"), "*.jpg")
#     for result in results:
#         if result.success:
#             print(f"Processed {result.path}: {result.data}")
#         else:
#             print(f"Failed to process {result.path}: {result.error}")
