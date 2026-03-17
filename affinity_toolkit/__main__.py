import argparse
import json
import os
import pathlib
import csv
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AffinityFile:
    name: str
    path: pathlib.Path
    size: int

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": str(self.path),
            "size": self.size
        }

class AffinityToolkit:

    @staticmethod
    def scan_directory(directory: pathlib.Path) -> List[AffinityFile]:
        """Scan the directory for Affinity Photo files."""
        affinity_files = []
        try:
            for entry in directory.iterdir():
                if entry.is_file() and entry.suffix in ['.afdesign', '.afphoto', '.afpub']:
                    affinity_files.append(AffinityFile(name=entry.name, path=entry, size=entry.stat().st_size))
        except Exception as e:
            print(f"Error scanning directory: {e}")
        return affinity_files

    @staticmethod
    def show_info(file_path: pathlib.Path) -> Optional[AffinityFile]:
        """Show information about a specific Affinity file."""
        try:
            if file_path.exists() and file_path.is_file():
                return AffinityFile(name=file_path.name, path=file_path, size=file_path.stat().st_size)
            else:
                print("File does not exist.")
        except Exception as e:
            print(f"Error retrieving file info: {e}")
        return None

    @staticmethod
    def export_data(files: List[AffinityFile], output_format: str, output_path: pathlib.Path) -> None:
        """Export file data to JSON or CSV."""
        try:
            if output_format == 'json':
                with open(output_path, 'w') as json_file:
                    json.dump([file.to_dict() for file in files], json_file, indent=4)
            elif output_format == 'csv':
                with open(output_path, 'w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=["name", "path", "size"])
                    writer.writeheader()
                    for file in files:
                        writer.writerow(file.to_dict())
            else:
                print("Unsupported format. Use 'json' or 'csv'.")
        except Exception as e:
            print(f"Error exporting data: {e}")

    @staticmethod
    def batch_process(files: List[AffinityFile]) -> None:
        """Batch process multiple Affinity files."""
        for file in files:
            print(f"Processing {file.name}...")
            # Placeholder for actual processing logic
            # Add processing code here
            print(f"Processed {file.name} successfully.")

def main():
    parser = argparse.ArgumentParser(description="Affinity Photo Toolkit for Windows")
    subparsers = parser.add_subparsers(dest='command')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan directory for Affinity Photo files')
    scan_parser.add_argument('directory', type=str, help='Directory to scan')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show information about a specific file')
    info_parser.add_argument('file', type=str, help='Path to the Affinity file')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export data to JSON/CSV')
    export_parser.add_argument('files', type=str, nargs='+', help='Paths to the Affinity files')
    export_parser.add_argument('output_format', type=str, choices=['json', 'csv'], help='Output format')
    export_parser.add_argument('output_path', type=str, help='Output file path')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process multiple files')
    batch_parser.add_argument('files', type=str, nargs='+', help='Paths to the Affinity files')

    args = parser.parse_args()

    toolkit = AffinityToolkit()

    if args.command == 'scan':
        directory = pathlib.Path(args.directory)
        files = toolkit.scan_directory(directory)
        for file in files:
            print(file)

    elif args.command == 'info':
        file_path = pathlib.Path(args.file)
        file_info = toolkit.show_info(file_path)
        if file_info:
            print(file_info)

    elif args.command == 'export':
        files = [pathlib.Path(file) for file in args.files]
        affinity_files = [toolkit.show_info(file) for file in files if toolkit.show_info(file)]
        toolkit.export_data(affinity_files, args.output_format, pathlib.Path(args.output_path))

    elif args.command == 'batch':
        files = [pathlib.Path(file) for file in args.files]
        toolkit.batch_process([toolkit.show_info(file) for file in files if toolkit.show_info(file)])

if __name__ == "__main__":
    main()
