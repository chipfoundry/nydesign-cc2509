#!/usr/bin/env python3
"""
Script to clone a GitHub project and rename the directory based on project type from info.yaml.

This script:
1. Clones a GitHub repository to the current working directory
2. Parses the info.yaml file in the project root to determine project type and extract naming information
3. Renames the local directory based on project type:
   - For wokwi projects: tt_um_wokwi_{wokwi_id}
   - For verilog projects: {top_module}

Usage:
    python get_project.py <github_url> [--target-dir <name>]
    
Examples:
    python get_project.py https://github.com/user/repo.git
    python get_project.py https://github.com/user/repo.git --target-dir my_project
    
Requirements:
    - PyYAML (install with: pip install PyYAML)
    - Git (for cloning repositories)
    
The script expects the cloned repository to have an info.yaml file in its root
with the following structure:
    For wokwi projects:
    project:
      language: "Wokwi"
      wokwi_id: <numeric_id>
    
    For verilog projects:
    project:
      language: "Verilog"
      top_module: <module_name>
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required but not installed.")
    print("Please install it with: pip install PyYAML")
    print("Or install all requirements with: pip install -r tt/requirements.txt")
    sys.exit(1)


def run_command(cmd, cwd=None):
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {cmd}")
            print(f"Error output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command '{cmd}': {e}")
        return False


def clone_repository(github_url, target_dir):
    """Clone a GitHub repository to the target directory."""
    print(f"Cloning repository: {github_url}")
    
    # Use git clone to clone the repository
    cmd = f"git clone {github_url} {target_dir}"
    if not run_command(cmd):
        return False
    
    print(f"Successfully cloned to: {target_dir}")
    return True


def parse_info_yaml(project_dir):
    """Parse info.yaml file and extract project information."""
    info_yaml_path = Path(project_dir) / "info.yaml"
    
    if not info_yaml_path.exists():
        print(f"Error: info.yaml not found in {project_dir}")
        return None
    
    try:
        with open(info_yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if 'project' not in data:
            print("Error: project section not found in info.yaml")
            return None
        
        project_data = data['project']
        language = project_data.get('language', '').lower()
        
        # Handle wokwi projects
        if language == 'wokwi':
            if 'wokwi_id' in project_data:
                wokwi_id = project_data['wokwi_id']
                print(f"Found wokwi project with wokwi_id: {wokwi_id}")
                return {'type': 'wokwi', 'id': wokwi_id}
            else:
                print("Error: wokwi_id not found in info.yaml for wokwi project")
                return None
        
        # Handle verilog projects
        elif language == 'verilog':
            if 'top_module' in project_data:
                top_module = project_data['top_module']
                print(f"Found verilog project with top_module: {top_module}")
                return {'type': 'verilog', 'top_module': top_module}
            else:
                print("Error: top_module not found in info.yaml for verilog project")
                return None
        
        else:
            print(f"Error: Unsupported project language '{language}'. Supported languages: wokwi, verilog")
            return None
            
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None
    except Exception as e:
        print(f"Error reading info.yaml: {e}")
        return None


def rename_directory(old_path, new_name):
    """Rename a directory."""
    old_path = Path(old_path)
    new_path = old_path.parent / new_name
    
    if new_path.exists():
        print(f"Warning: Directory {new_path} already exists. Removing it first.")
        shutil.rmtree(new_path)
    
    try:
        old_path.rename(new_path)
        print(f"Renamed directory to: {new_path}")
        return str(new_path)
    except Exception as e:
        print(f"Error renaming directory: {e}")
        return None


def extract_repo_name_from_url(github_url):
    """Extract repository name from GitHub URL."""
    parsed = urlparse(github_url)
    path = parsed.path.strip('/')
    
    # Handle both .git and non-.git URLs
    if path.endswith('.git'):
        path = path[:-4]
    
    # Extract the last part (repo name)
    repo_name = path.split('/')[-1]
    return repo_name


def test_yaml_parsing():
    """Test function to validate YAML parsing logic."""
    # Test wokwi project
    test_wokwi_yaml = """
project:
  wokwi_id: 123456789
  title: "Test Wokwi Project"
  author: "Test Author"
  language: "Wokwi"
"""
    
    # Test verilog project
    test_verilog_yaml = """
project:
  top_module: "tt_um_test_verilog"
  title: "Test Verilog Project"
  author: "Test Author"
  language: "Verilog"
"""
    
    try:
        # Test wokwi parsing
        data = yaml.safe_load(test_wokwi_yaml)
        project_data = data['project']
        language = project_data.get('language', '').lower()
        
        if language == 'wokwi' and 'wokwi_id' in project_data:
            wokwi_id = project_data['wokwi_id']
            print(f"Wokwi test successful: extracted wokwi_id = {wokwi_id}")
        else:
            print("Wokwi test failed")
            return False
        
        # Test verilog parsing
        data = yaml.safe_load(test_verilog_yaml)
        project_data = data['project']
        language = project_data.get('language', '').lower()
        
        if language == 'verilog' and 'top_module' in project_data:
            top_module = project_data['top_module']
            print(f"Verilog test successful: extracted top_module = {top_module}")
        else:
            print("Verilog test failed")
            return False
        
        print("All tests passed!")
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Clone GitHub project and rename based on project type (wokwi or verilog)')
    parser.add_argument('github_url', help='GitHub repository URL to clone')
    parser.add_argument('--target-dir', help='Target directory name (default: extracted from URL)')
    parser.add_argument('--test', action='store_true', help='Run YAML parsing test')
    
    args = parser.parse_args()
    
    # Run test if requested
    if args.test:
        print("Running YAML parsing test...")
        if test_yaml_parsing():
            print("Test passed!")
            sys.exit(0)
        else:
            print("Test failed!")
            sys.exit(1)
    
    # Validate GitHub URL
    if not args.github_url.startswith(('http://', 'https://', 'git@')):
        print("Error: Please provide a valid GitHub URL")
        sys.exit(1)
    
    # Determine target directory name
    if args.target_dir:
        temp_dir_name = args.target_dir
    else:
        temp_dir_name = extract_repo_name_from_url(args.github_url)
    
    # Get current working directory
    current_dir = Path.cwd()
    temp_dir_path = current_dir / temp_dir_name
    
    # Check if target directory already exists
    if temp_dir_path.exists():
        print(f"Error: Directory '{temp_dir_name}' already exists in current directory")
        sys.exit(1)
    
    try:
        # Clone the repository
        if not clone_repository(args.github_url, temp_dir_path):
            print("Failed to clone repository")
            sys.exit(1)
        
        # Parse info.yaml to get project information
        project_info = parse_info_yaml(temp_dir_path)
        if project_info is None:
            print("Failed to extract project information from info.yaml")
            # Clean up the cloned directory
            shutil.rmtree(temp_dir_path)
            sys.exit(1)
        
        # Determine new directory name based on project type
        if project_info['type'] == 'wokwi':
            new_dir_name = f"tt_um_wokwi_{project_info['id']}"
        elif project_info['type'] == 'verilog':
            new_dir_name = project_info['top_module']
        else:
            print(f"Error: Unknown project type '{project_info['type']}'")
            shutil.rmtree(temp_dir_path)
            sys.exit(1)
        
        final_path = rename_directory(temp_dir_path, new_dir_name)
        
        if final_path:
            print(f"Success! Project cloned and renamed to: {new_dir_name}")
            print(f"Full path: {final_path}")
        else:
            print("Failed to rename directory")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        # Clean up on interruption
        if temp_dir_path.exists():
            shutil.rmtree(temp_dir_path)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Clean up on error
        if temp_dir_path.exists():
            shutil.rmtree(temp_dir_path)
        sys.exit(1)


if __name__ == "__main__":
    main()
