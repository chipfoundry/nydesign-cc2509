# Copy Hardened Project Script

This script (`copy_hardened_project.py`) helps you copy files from a hardened TinyTapeout project to the projects directory for integration with the TinyTapeout script system.

## What Files Are Copied

The script copies the following files and directories from your hardened project. Note that design files and some metadata are expected to be in a `tt_submission` subdirectory:

### Required Files:
- `docs/info.md` - Project documentation
- `tt_submission/stats/` - Statistics directory (with all contents)
- `LICENSE` - Project license file
- `tt_submission/commit_id.json` - Git commit information
- `info.yaml` - Project configuration file

### Optional Files:
- `wokwi-diagram.json` - Wokwi diagram file (if present)

### Design Files (from tt_submission directory):
- `tt_submission/*.gds` - GDS layout files
- `tt_submission/*.lef` - LEF library files
- `tt_submission/*.oas` - OAS layout files
- `tt_submission/*.v` - Verilog source files

## Usage

### Basic Usage
```bash
python3 copy_hardened_project.py
```

The script defaults to using the current directory as the source and the directory name as the project name. You can optionally specify a different source directory with `-s` and/or a custom project name with `-n`.

### Examples

1. **Copy from current directory (project name defaults to directory name):**
   ```bash
   python3 copy_hardened_project.py
   ```

2. **Copy from specific source directory (project name defaults to directory name):**
   ```bash
   python3 copy_hardened_project.py -s /path/to/hardened/project
   ```

3. **Copy with custom project name:**
   ```bash
   python3 copy_hardened_project.py -n tt_um_my_project
   ```

4. **Copy with verbose output:**
   ```bash
   python3 copy_hardened_project.py -v
   ```

5. **Specify custom projects directory:**
   ```bash
   python3 copy_hardened_project.py -p /path/to/projects
   ```

## Command Line Options

- `-s, --source`: Source directory containing the hardened project files (default: current directory)
- `-n, --name`: Project name (defaults to source directory name)
- `-p, --projects-dir`: Projects directory (default: 'projects' or TINYTAPEOUT_PROJECTS_DIR env var)
- `-v, --verbose`: Enable verbose output
- `-h, --help`: Show help message

## Environment Variables

You can set the `TINYTAPEOUT_PROJECTS_DIR` environment variable to specify a default projects directory:

```bash
# Set environment variable
export TINYTAPEOUT_PROJECTS_DIR="/path/to/my/projects"

# Now the script will use this directory by default
python3 copy_hardened_project.py -s . -n tt_um_my_project
```

## Project Naming Convention

Project names should follow the TinyTapeout convention and start with `tt_um_`. The script will warn you if your project name doesn't follow this convention.

## Output

The script will:
1. Create a new directory in the projects folder with your project name
2. Copy all required and optional files
3. Provide a summary of successful operations
4. Report any errors or missing files

## Example Output

```
Copying hardened project from '/path/to/source' to '/path/to/projects/tt_um_my_project'
  Copying GDS files (1 files):
    Copied file: /path/to/source/tt_submission/tt_um_my_project.gds -> /path/to/projects/tt_um_my_project/tt_um_my_project.gds
  Copying LEF files (1 files):
    Copied file: /path/to/source/tt_submission/tt_um_my_project.lef -> /path/to/projects/tt_um_my_project/tt_um_my_project.lef
  Copied file: /path/to/source/docs/info.md -> /path/to/projects/tt_um_my_project/docs/info.md
  Copied directory: /path/to/source/tt_submission/stats -> /path/to/projects/tt_um_my_project/stats
  Copied file: /path/to/source/LICENSE -> /path/to/projects/tt_um_my_project/LICENSE
  Copied file: /path/to/source/tt_submission/commit_id.json -> /path/to/projects/tt_um_my_project/commit_id.json
  Copied file: /path/to/source/info.yaml -> /path/to/projects/tt_um_my_project/info.yaml

Copy operation completed:
  Successful operations: 7/7
  Project directory: /path/to/projects/tt_um_my_project
  All files copied successfully!

Project copied successfully! You can now integrate it with TinyTapeout.
```

## Troubleshooting

- **Source directory not found**: Make sure the source directory path is correct
- **Projects directory not found**: The script will create the projects directory if it doesn't exist
- **Permission errors**: Make sure you have write permissions to the destination directory
- **Missing files**: The script will warn about missing required files but continue with available files

## Integration with TinyTapeout

After running this script, your project will be properly structured in the projects directory and ready for integration with the TinyTapeout script system. The copied files will be in the correct format and location expected by TinyTapeout tools.
