# Programming Exam Template

A template system for creating and packaging programming exams using Quarto markdown and Python.

## Overview

This project provides a structured template for creating programming exams that can be automatically built into PDF documents and packaged into zip files for distribution to students.

## Project Structure

```
.
├── Exam/                    # Example exam directory
│   ├── text.qmd            # Quarto markdown file with exam description
│   ├── text.pdf            # Generated PDF (created after build)
│   ├── image.png           # Optional header image for the exam
│   └── src/                # Source code directory
│       ├── main.py         # Test cases and main execution file
│       └── solve.py        # Solution template (students modify this)
├── zips/                   # Generated zip files (created after packaging)
├── packing.py              # Script to package exams into zip files
└── makefile                # Build automation

```

## Requirements

- **Python 3.x** - For running the packing script
- **Quarto** - For rendering `.qmd` files to PDF
- **Make** - For running build commands

### Installing Quarto

Visit [quarto.org](https://quarto.org/docs/get-started/) for installation instructions.

## Usage

### Creating a New Exam

1. Create a new directory (e.g., `Exam2/`)
2. Add a `text.qmd` file with the exam description (see `Exam/text.qmd` for template)
3. Optionally add an `image.png` file for the exam header
4. Create a `src/` directory with:
   - `solve.py` - Template file with the solution function signature
   - `main.py` - Test cases and execution code

### Building PDFs

To build PDF files from all `.qmd` files:

```bash
make build
```

This will render all `text.qmd` files in exam directories to `text.pdf`.

### Packaging Exams

To build PDFs and package all exams into zip files:

```bash
make package
```

This will:

1. Build all PDF files from `.qmd` files
2. Create zip files in the `zips/` directory
3. Each zip contains:
   - The PDF (renamed based on the exam title from `text.qmd`)
   - All files from the `src/` directory

The zip filename is derived from the exam title in the `text.qmd` YAML frontmatter.

### Cleaning Generated Files

To remove all generated PDF files:

```bash
make clean
```

## Exam Template Structure

### `text.qmd`

A Quarto markdown file with YAML frontmatter:

```yaml
---
title: "Exam Title"
subtitle: "Exam Type. Exam ID. Course"
format:
  pdf:
    colorlinks: true
    fontsize: 11pt
    geometry:
      - margin=2cm
    whitespace: small
    linestretch: 1
---
```

### `src/solve.py`

This is the only file students can modify. It contains the solution function template:

```python
def solution_function(parametro_1, parametro_2):
    # Implementa tu solución aquí
    pass
```

**Important:** Students cannot change function names, parameters, or return types.

### `src/main.py`

Contains test cases and execution code:

```python
from solve import solution_function

# Escriba sus casos de prueba aquí
```

## Notes

- PDF filenames in zip files are sanitized to be valid filenames
- Only directories containing both `text.pdf` and `src/` will be packaged
- Existing zip files are skipped during packaging (to avoid overwriting)
