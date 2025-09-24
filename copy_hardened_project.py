#!/usr/bin/env python3
"""
Script to copy files from a hardened TinyTapeout project to the projects directory.

This script copies all necessary files from a hardened TinyTapeout project
to integrate it with the TinyTapeout script system.

Required files to copy:
- docs/info.md
- stats/ directory (with all contents)
- LICENSE
- commit_id.json
- info.yaml
- GDS files (*.gds)
- LEF files (*.lef)
- OAS files (*.oas)
- Verilog files (*.v)
- wokwi-diagram.json (if present)
"""

import os
import shutil
import argparse
import glob
from pathlib import Path
import json
import time


def fix_commit_id_json(file_path, verbose=False):
    """Fix commit_id.json file by adding sort_id if missing."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Check if sort_id is missing
        if 'sort_id' not in data:
            # Generate a sort_id based on current timestamp
            sort_id = int(time.time() * 1000)  # milliseconds since epoch
            data['sort_id'] = sort_id
            
            # Write the updated data back to the file
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            if verbose:
                print(f"  Added missing sort_id ({sort_id}) to {file_path}")
            return True
        else:
            if verbose:
                print(f"  sort_id already present in {file_path}")
            return True
            
    except Exception as e:
        print(f"  Error fixing commit_id.json {file_path}: {e}")
        return False


def copy_file_or_dir(src_path, dst_path, verbose=False):
    """Copy a file or directory from src_path to dst_path."""
    try:
        if os.path.isdir(src_path):
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
            if verbose:
                print(f"  Copied directory: {src_path} -> {dst_path}")
        else:
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            if verbose:
                print(f"  Copied file: {src_path} -> {dst_path}")
        return True
    except Exception as e:
        print(f"  Error copying {src_path}: {e}")
        return False


def find_files_by_pattern(src_dir, pattern, verbose=False):
    """Find files matching a pattern in the source directory."""
    search_path = os.path.join(src_dir, pattern)
    files = glob.glob(search_path)
    if verbose and files:
        print(f"  Found {len(files)} files matching pattern '{pattern}':")
        for f in files:
            print(f"    {f}")
    return files


def copy_hardened_project(src_dir, project_name, projects_dir, verbose=False):
    """
    Copy all required files from a hardened TinyTapeout project.
    
    Args:
        src_dir: Source directory containing the hardened project
        project_name: Name of the project (e.g., 'tt_um_my_project')
        projects_dir: Destination projects directory
        verbose: Whether to print detailed output
    """
    
    if not os.path.exists(src_dir):
        print(f"Error: Source directory '{src_dir}' does not exist")
        return False
    
    if not os.path.exists(projects_dir):
        print(f"Error: Projects directory '{projects_dir}' does not exist")
        return False
    
    # Create destination project directory
    dst_project_dir = os.path.join(projects_dir, project_name)
    os.makedirs(dst_project_dir, exist_ok=True)
    
    print(f"Copying hardened project from '{src_dir}' to '{dst_project_dir}'")
    
    success_count = 0
    total_operations = 0
    
    # Define the files and directories to copy
    items_to_copy = [
        ("docs/info.md", "docs/info.md"),
        ("tt_submission/stats", "stats"),
        ("LICENSE", "LICENSE"),
        ("tt_submission/commit_id.json", "commit_id.json"),
        ("info.yaml", "info.yaml"),
        ("wokwi-diagram.json", "wokwi-diagram.json"),  # Optional file
    ]
    
    # Copy specific files and directories
    for src_item, dst_item in items_to_copy:
        src_path = os.path.join(src_dir, src_item)
        dst_path = os.path.join(dst_project_dir, dst_item)
        
        if os.path.exists(src_path):
            total_operations += 1
            if copy_file_or_dir(src_path, dst_path, verbose):
                success_count += 1
                
                # Fix commit_id.json if it was copied
                if src_item == "tt_submission/commit_id.json":
                    if verbose:
                        print(f"  Checking and fixing commit_id.json...")
                    fix_commit_id_json(dst_path, verbose)
                    
        elif src_item == "wokwi-diagram.json":
            # wokwi-diagram.json is optional, so don't count it as an error
            if verbose:
                print(f"  Optional file not found: {src_path}")
        else:
            print(f"  Warning: Required file/directory not found: {src_path}")
    
    # Copy files by pattern (GDS, LEF, OAS, V files) from tt_submission directory
    file_patterns = [
        ("tt_submission/*.gds", "GDS files"),
        ("tt_submission/*.lef", "LEF files"), 
        ("tt_submission/*.oas", "OAS files"),
        ("tt_submission/*.v", "Verilog files"),
    ]
    
    for pattern, description in file_patterns:
        files = find_files_by_pattern(src_dir, pattern, verbose)
        if files:
            print(f"  Copying {description} ({len(files)} files):")
            for src_file in files:
                filename = os.path.basename(src_file)
                dst_path = os.path.join(dst_project_dir, filename)
                total_operations += 1
                if copy_file_or_dir(src_file, dst_path, verbose):
                    success_count += 1
        else:
            if verbose:
                print(f"  No {description} found in tt_submission directory")
    
    # Summary
    print(f"\nCopy operation completed:")
    print(f"  Successful operations: {success_count}/{total_operations}")
    print(f"  Project directory: {dst_project_dir}")
    
    if success_count == total_operations:
        print("  All files copied successfully!")
        return True
    else:
        print(f"  {total_operations - success_count} operations failed")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Copy files from a hardened TinyTapeout project to the projects directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Copy from current directory (project name defaults to directory name)
  python copy_hardened_project.py
  
  # Copy from specific source directory (project name defaults to directory name)
  python copy_hardened_project.py -s /path/to/hardened/project
  
  # Copy with custom project name
  python copy_hardened_project.py -n tt_um_my_project
  
  # Copy with verbose output
  python copy_hardened_project.py -v
  
  # Specify custom projects directory
  python copy_hardened_project.py -p /path/to/projects
  
        """
    )
    
    parser.add_argument(
        "-s", "--source", 
        default=".",
        help="Source directory containing the hardened project files (default: current directory)"
    )
    
    parser.add_argument(
        "-n", "--name",
        help="Project name (defaults to source directory name)"
    )
    
    parser.add_argument(
        "-p", "--projects-dir",
        default=os.environ.get("TINYTAPEOUT_PROJECTS_DIR", "projects"),
        help="Projects directory (default: 'projects' or TINYTAPEOUT_PROJECTS_DIR env var)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    
    args = parser.parse_args()
    
    # Convert relative paths to absolute
    src_dir = os.path.abspath(args.source)
    projects_dir = os.path.abspath(args.projects_dir)
    
    # Default project name to source directory name if not provided
    if args.name is None:
        project_name = os.path.basename(src_dir)
    else:
        project_name = args.name
    
    # Validate project name format
    if not project_name.startswith("tt_um_"):
        print(f"Warning: Project name '{project_name}' doesn't follow TinyTapeout naming convention (should start with 'tt_um_')")
    
    success = copy_hardened_project(src_dir, project_name, projects_dir, args.verbose)
    
    if success:
        print("\nProject copied successfully! You can now integrate it with TinyTapeout.")
    else:
        print("\nSome files failed to copy. Please check the output above for details.")
        exit(1)


if __name__ == "__main__":
    main()
