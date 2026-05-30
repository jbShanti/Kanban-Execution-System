from pathlib import Path

# Current project root
ROOT = Path(".")

# Directory structure
DIRECTORIES = [
    ROOT / "specs",
    ROOT / "src",
    ROOT / "src" / "parser",
    ROOT / "src" / "parser" / "fixtures",
    ROOT / "src" / "parser" / "schemas",
    ROOT / "tests",
    ROOT / "examples",
    ROOT / "output",
]

# Files with optional initial content
FILES = {
    ROOT / "README.md": "# Kanban Execution System\n",

    ROOT / "requirements.txt": "\n".join([
        "pydantic",
    ]) + "\n",

    ROOT / ".gitignore": "\n".join([
        "__pycache__/",
        ".venv/",
        "*.pyc",
        ".DS_Store",
        "output/",
    ]) + "\n",

    ROOT / "src" / "main.py": "",

    ROOT / "src" / "parser" / "__init__.py": "",
    ROOT / "src" / "parser" / "parser.py": "",
    ROOT / "src" / "parser" / "metadata.py": "",
    ROOT / "src" / "parser" / "models.py": "",
    ROOT / "src" / "parser" / "analytics.py": "",
    ROOT / "src" / "parser" / "constants.py": "",
    ROOT / "src" / "parser" / "enums.py": "",

    ROOT / "tests" / "test_parser.py": "",
    ROOT / "tests" / "test_metadata.py": "",
    ROOT / "tests" / "test_analytics.py": "",

    ROOT / "examples" / "sample_output.json": "{}\n",

    ROOT / "src" / "parser" / "fixtures" / "simple_board.md": "",
    ROOT / "src" / "parser" / "fixtures" / "archive_cases.md": "",
    ROOT / "src" / "parser" / "fixtures" / "malformed_metadata.md": "",
    ROOT / "src" / "parser" / "fixtures" / "nested_tasks.md": "",
}

# Create directories
for directory in DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)

# Create files only if they don't exist
for filepath, content in FILES.items():
    if not filepath.exists():
        filepath.write_text(content, encoding="utf-8")
        print(f"[CREATED] {filepath}")
    else:
        print(f"[SKIPPED] {filepath} already exists")

print("\nProject structure initialization completed.")