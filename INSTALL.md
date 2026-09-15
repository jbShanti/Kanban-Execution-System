# Installation Guide for Windows

## Prerequisites
- Python 3.10 or higher
- pip (usually comes with Python)

## Installation Steps

1. Clone the repository:
   ```powershell
   git clone https://github.com/jbShanti/Kanban-Execution-System.git
   cd Kanban-Execution-System
   ```

2. Create and activate virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install the package in editable mode:
   ```powershell
   pip install -e .
   ```

## Usage

### Generate a report
```powershell
kes --input path\to\your\board.md --output report.md
```

### Show help
```powershell
kes --help
```

### Without specifying input (uses default board search)
```powershell
kes --output my_report.md
```

## Troubleshooting

If `kes` command is not found after installation:
1. Ensure virtual environment is activated
2. Check that Python Scripts directory is in PATH
3. Try reinstalling: `pip uninstall kanban-execution-system && pip install -e .`