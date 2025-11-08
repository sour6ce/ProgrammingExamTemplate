import zipfile
import re
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
ZIP_PATH = BASE_DIR / "zips"
FOLDER_PATH = BASE_DIR / "packages"
EXAM_DIR_NAME = "Examen"

ZIP_PATH.mkdir(parents=True, exist_ok=True)
FOLDER_PATH.mkdir(parents=True, exist_ok=True)


def extract_title_from_qmd(qmd_path):
    """Extract title from text.qmd YAML frontmatter."""
    try:
        with open(qmd_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Match title in YAML frontmatter: title: "..." or title: ...
        match = re.search(r"title:\s*[\"'](.+?)[\"']", content)
        if match:
            return match.group(1)
        # Fallback: match without quotes
        match = re.search(r"title:\s*(.+?)\n", content)
        if match:
            return match.group(1).strip()
    except Exception as e:
        print(f"Warning: Could not extract title from {qmd_path}: {e}")
    return None


def sanitize_filename(title):
    """Convert title to a valid filename."""
    if not title:
        return "text.pdf"
    # Remove or replace invalid filename characters
    # Keep only alphanumeric, spaces, hyphens, underscores, and some special chars
    sanitized = re.sub(r'[<>:"/\\|?*]', "", title)
    # Replace multiple spaces with single space
    sanitized = re.sub(r"\s+", " ", sanitized)
    # Trim and add .pdf extension
    sanitized = sanitized.strip()
    if not sanitized:
        return "text.pdf"
    return f"{sanitized}.pdf"


def pack_exams():
    """Create zip files for each exam directory containing text.pdf and src directory."""
    # Find all exam directories (directories that contain text.pdf and src/)
    exam_dirs = []
    for item in BASE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            text_pdf = item / "text.pdf"
            src_dir = item / "src"
            if text_pdf.exists() and src_dir.exists():
                exam_dirs.append(item)

    # Create zip file for each exam
    for exam_dir in exam_dirs:
        # Extract title from text.qmd
        qmd_path = exam_dir / "text.qmd"
        pdf_name = "text.pdf"  # default name
        if qmd_path.exists():
            title = extract_title_from_qmd(qmd_path)
            if title:
                pdf_name = sanitize_filename(title)

        zip_name = f"{pdf_name[:-4]}.zip"
        zip_path = ZIP_PATH / zip_name

        if zip_path.exists():
            print(f"Zip file {zip_path} already exists")
            continue

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add text.pdf with renamed arcname inside exam directory
            text_pdf = exam_dir / "text.pdf"
            zipf.write(text_pdf, arcname=f"{EXAM_DIR_NAME}/{pdf_name}")

            # Add all files from src directory recursively inside exam directory
            src_dir = exam_dir / "src"
            for file_path in src_dir.rglob("*"):
                if file_path.is_file():
                    # Preserve directory structure within src, but place inside exam directory
                    relative_path = file_path.relative_to(exam_dir)
                    arcname = f"{EXAM_DIR_NAME}/{relative_path}"
                    zipf.write(file_path, arcname=arcname)

        print(f"Created {zip_name} with PDF named: {pdf_name}")


def pack_exams_to_folders():
    """Copy exam files to folders instead of zip files."""
    # Find all exam directories (directories that contain text.pdf and src/)
    exam_dirs = []
    for item in BASE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            text_pdf = item / "text.pdf"
            src_dir = item / "src"
            if text_pdf.exists() and src_dir.exists():
                exam_dirs.append(item)

    # Create folder for each exam
    for exam_dir in exam_dirs:
        # Extract title from text.qmd
        qmd_path = exam_dir / "text.qmd"
        pdf_name = "text.pdf"  # default name
        if qmd_path.exists():
            title = extract_title_from_qmd(qmd_path)
            if title:
                pdf_name = sanitize_filename(title)

        folder_name = pdf_name[:-4]  # Remove .pdf extension
        folder_path = FOLDER_PATH / folder_name

        if folder_path.exists():
            print(f"Folder {folder_path} already exists")
            continue

        # Create the folder
        folder_path.mkdir(parents=True, exist_ok=True)

        # Copy text.pdf with renamed filename based on title
        text_pdf = exam_dir / "text.pdf"
        dest_pdf = folder_path / pdf_name
        shutil.copy2(text_pdf, dest_pdf)

        # Copy all files from src directory recursively
        src_dir = exam_dir / "src"
        dest_src_dir = folder_path / "src"
        shutil.copytree(src_dir, dest_src_dir)

        print(f"Created folder {folder_name} with PDF named: {pdf_name}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--folder":
        pack_exams_to_folders()
    else:
        pack_exams()
