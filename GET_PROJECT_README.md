# get_project.py

A Python script to clone GitHub projects and automatically rename the directory based on the project type found in the project's `info.yaml` file. Supports both Wokwi and Verilog projects.

## Features

- Clones GitHub repositories to the current working directory
- Parses `info.yaml` to determine project type (Wokwi or Verilog)
- Automatically renames the directory based on project type:
  - **Wokwi projects**: `tt_um_wokwi_{wokwi_id}`
  - **Verilog projects**: `{top_module}`
- Handles errors gracefully with cleanup
- Supports custom target directory names
- Case-insensitive language detection

## Requirements

- Python 3.6+
- PyYAML (`pip install PyYAML`)
- Git (for cloning repositories)

## Installation

1. Install PyYAML:
   ```bash
   pip install PyYAML
   ```
   
   Or install all project requirements:
   ```bash
   pip install -r tt/requirements.txt
   ```

2. Make the script executable:
   ```bash
   chmod +x get_project.py
   ```

## Usage

### Basic Usage
```bash
python get_project.py <github_url>
```

### Examples
```bash
# Clone a Wokwi project and rename based on wokwi_id
python get_project.py https://github.com/user/wokwi-project.git

# Clone a Verilog project and rename based on top_module
python get_project.py https://github.com/user/verilog-project.git

# Clone with custom target directory name
python get_project.py https://github.com/user/repo.git --target-dir my_project

# Test YAML parsing functionality
python get_project.py --test
```

### Command Line Options

- `github_url`: The GitHub repository URL to clone (required)
- `--target-dir`: Custom target directory name (optional, defaults to repository name)
- `--test`: Run YAML parsing test (optional)

## Expected Project Structure

The script expects the cloned repository to have an `info.yaml` file in its root. The structure depends on the project type:

### Wokwi Projects
```yaml
project:
  language: "Wokwi"  # Case insensitive
  wokwi_id: 123456789  # This will be used for directory naming
  title: "Project Title"
  author: "Author Name"
  # ... other project fields
```

### Verilog Projects
```yaml
project:
  language: "Verilog"  # Case insensitive
  top_module: "tt_um_my_verilog_project"  # This will be used for directory naming
  title: "Project Title"
  author: "Author Name"
  # ... other project fields
```

## Output

The script will:
1. Clone the repository to a temporary directory
2. Parse the `info.yaml` file to determine project type and extract naming information
3. Rename the directory based on project type:
   - **Wokwi projects**: `tt_um_wokwi_{wokwi_id}`
   - **Verilog projects**: `{top_module}`
4. Report success with the final directory path

## Error Handling

The script includes comprehensive error handling:
- Validates GitHub URL format
- Checks for existing directories
- Handles missing or malformed `info.yaml` files
- Validates project language (must be "wokwi" or "verilog")
- Ensures required fields are present for each project type
- Cleans up on errors or interruption
- Provides clear error messages

## Example Output

### Wokwi Project
```
$ python get_project.py https://github.com/user/my-wokwi-project.git
Cloning repository: https://github.com/user/my-wokwi-project.git
Successfully cloned to: /path/to/my-wokwi-project
Found wokwi project with wokwi_id: 431407462994924545
Renamed directory to: /path/to/tt_um_wokwi_431407462994924545
Success! Project cloned and renamed to: tt_um_wokwi_431407462994924545
Full path: /path/to/tt_um_wokwi_431407462994924545
```

### Verilog Project
```
$ python get_project.py https://github.com/user/my-verilog-project.git
Cloning repository: https://github.com/user/my-verilog-project.git
Successfully cloned to: /path/to/my-verilog-project
Found verilog project with top_module: tt_um_my_verilog_project
Renamed directory to: /path/to/tt_um_my_verilog_project
Success! Project cloned and renamed to: tt_um_my_verilog_project
Full path: /path/to/tt_um_my_verilog_project
```
