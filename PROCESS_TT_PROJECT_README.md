# process_tt_project.py

A comprehensive Python script that automates the complete setup process for TinyTapeout projects. This script handles both Wokwi and Verilog projects by automatically detecting the project type from the `info.yaml` file.

## Features

- **Automatic project type detection**: Supports both Wokwi and Verilog projects
- **Complete automation**: Handles the entire TinyTapeout project setup process
- **Project naming**: Automatically renames projects based on type:
  - **Wokwi projects**: `tt_um_wokwi_{wokwi_id}`
  - **Verilog projects**: `{top_module}`
- **Error handling**: Comprehensive error handling with cleanup
- **Progress tracking**: Clear step-by-step progress reporting
- **Sound notifications**: Audio feedback for success/failure
- **Project manifest**: Automatically updates project tracking

## Requirements

- Python 3.6+
- PyYAML (`pip install PyYAML`)
- Git (for cloning repositories)
- TinyTapeout support tools (cloned automatically)

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
   chmod +x process_tt_project.py
   ```

## Usage

### Basic Usage
```bash
python3 process_tt_project.py <github_url>
```

### Examples
```bash
# Process a Wokwi project
python3 process_tt_project.py https://github.com/user/wokwi-project.git

# Process a Verilog project
python3 process_tt_project.py https://github.com/user/verilog-project.git

# Show detailed step information
python3 process_tt_project.py --help-steps
```

### Command Line Options

- `github_url`: The GitHub repository URL to clone and process (required)
- `--help-steps`: Show detailed step information (optional)

## Processing Steps

The script automates the following steps:

1. **Clone project and rename based on project type** (wokwi or verilog)
2. **Clone tt-support-tools repository**
3. **Create user configuration**
4. **Harden the project**
5. **Create TT submission**
6. **Copy hardened project files**
7. **Update project manifest**
8. **Change to project directory**

## Expected Project Structure

The script expects the cloned repository to have an `info.yaml` file in its root. The structure depends on the project type:

### Wokwi Projects
```yaml
project:
  language: "Wokwi"  # Case insensitive
  wokwi_id: 123456789  # Used for directory naming
  title: "Project Title"
  author: "Author Name"
  # ... other project fields
```

### Verilog Projects
```yaml
project:
  language: "Verilog"  # Case insensitive
  top_module: "tt_um_my_verilog_project"  # Used for directory naming
  title: "Project Title"
  author: "Author Name"
  # ... other project fields
```

## Output

The script provides detailed output for each step:

```
🚀 Starting TinyTapeout Project Processing
Working directory: /path/to/current/directory
GitHub URL: https://github.com/user/project.git

============================================================
Step: Clone project and rename based on project type (wokwi or verilog)
Command: get_project.py https://github.com/user/project.git
============================================================
✅ Success!

============================================================
Step: Clone tt-support-tools repository
Command: git clone https://github.com/TinyTapeout/tt-support-tools.git tt
============================================================
✅ Success!

[... additional steps ...]

🎉 TinyTapeout project setup completed successfully!

Next steps:
- Review the generated files
- Test your project
- Submit to TinyTapeout if ready
```

## Project Manifest

The script automatically updates a `project_manifest.csv` file in the original directory with project information:

- Project name
- GitHub URL
- Project directory
- Processed date
- Status

## Error Handling

The script includes comprehensive error handling:
- Validates GitHub URL format
- Handles cloning failures
- Manages missing or malformed `info.yaml` files
- Validates project language and required fields
- Cleans up on errors or interruption
- Provides clear error messages
- Audio notifications for success/failure

## Integration

This script works seamlessly with:
- `get_project.py` - For project cloning and renaming
- `copy_hardened_project.py` - For copying hardened project files
- TinyTapeout support tools - For project hardening and submission

## Troubleshooting

- **PyYAML not found**: Install with `pip install PyYAML`
- **Git clone fails**: Check GitHub URL and network connectivity
- **Missing info.yaml**: Ensure the repository has a valid `info.yaml` file
- **Unsupported language**: Only "wokwi" and "verilog" are supported
- **Permission errors**: Ensure write permissions to the current directory

## Example Complete Workflow

```bash
# Start the complete process
python3 process_tt_project.py https://github.com/user/my-project.git

# The script will:
# 1. Clone and rename the project
# 2. Set up TinyTapeout tools
# 3. Harden the project
# 4. Create submission files
# 5. Copy files to projects directory
# 6. Update project manifest
# 7. Play success sound

# Your project is now ready for TinyTapeout!
```
