#!/usr/bin/env python3
"""
TinyTapeout Project Process Script

This script automates the complete setup process for a TinyTapeout project:
1. Clone project and rename based on project type (wokwi or verilog)
2. Clone tt-support-tools repository
3. Create user configuration
4. Harden the project
5. Create TT submission
6. Copy hardened project files

Usage: python3 process_tt_project.py <github_url>
"""

import subprocess
import sys
import os
import csv
import argparse
from pathlib import Path
from datetime import datetime


def play_sound(sound_type="success"):
    """Play a system sound notification."""
    try:
        if sound_type == "success":
            # Play success sound (system bell or beep)
            print("\a", end="", flush=True)  # ASCII bell character
            # Also try system beep command
            subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], 
                          capture_output=True, timeout=2)
        elif sound_type == "error":
            # Play error sound
            print("\a", end="", flush=True)  # ASCII bell character
            # Also try system beep command
            subprocess.run(["afplay", "/System/Library/Sounds/Basso.aiff"], 
                          capture_output=True, timeout=2)
    except Exception:
        # Fallback to simple beep if system sounds fail
        print("\a", end="", flush=True)


def run_command(command, description, capture_output=True):
    """Run a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Step: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=capture_output, text=True)
        print("✅ Success!")
        if result.stdout:
            print("Output:", result.stdout)
        return True, result.stdout if capture_output else ""
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)
        return False, e.stdout if capture_output else ""


def update_project_manifest(project_name, github_url, project_dir, manifest_dir=None):
    """Update the project manifest with new project information."""
    if manifest_dir is None:
        manifest_dir = os.getcwd()
    
    manifest_file = os.path.join(manifest_dir, "project_manifest.csv")
    
    # Define CSV headers
    headers = ["project_name", "github_url", "project_directory", "processed_date", "status"]
    
    # Load existing projects
    existing_projects = []
    if os.path.exists(manifest_file):
        try:
            with open(manifest_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                existing_projects = list(reader)
        except Exception as e:
            print(f"Warning: Could not read existing manifest: {e}")
            existing_projects = []
    
    # Create new project entry
    new_entry = {
        "project_name": project_name,
        "github_url": github_url,
        "project_directory": project_dir,
        "processed_date": datetime.now().isoformat(),
        "status": "completed"
    }
    
    # Check if project already exists (by github_url)
    existing_index = None
    for i, project in enumerate(existing_projects):
        if project["github_url"] == github_url:
            existing_index = i
            break
    
    if existing_index is not None:
        # Update existing entry
        existing_projects[existing_index] = new_entry
        print(f"✅ Updated existing project entry for {project_name}")
    else:
        # Add new entry
        existing_projects.append(new_entry)
        print(f"✅ Added new project entry for {project_name}")
    
    # Save manifest
    try:
        with open(manifest_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(existing_projects)
        print(f"✅ Project manifest updated: {manifest_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to update project manifest: {e}")
        return False


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Process TinyTapeout project from GitHub URL')
    parser.add_argument('github_url', help='GitHub repository URL to clone and process')
    parser.add_argument('--help-steps', action='store_true', help='Show detailed step information')
    
    args = parser.parse_args()
    
    # Show detailed steps if requested
    if args.help_steps:
        print("📋 TinyTapeout Project Processing Steps:")
        print("1. Clone project and rename based on project type (wokwi or verilog)")
        print("2. Clone tt-support-tools repository")
        print("3. Create user configuration")
        print("4. Harden the project")
        print("5. Create TT submission")
        print("6. Copy hardened project files")
        print("7. Update project manifest")
        print("8. Change to project directory")
        print("\nUsage: python3 process_tt_project.py <github_url>")
        sys.exit(0)
    
    print("🚀 Starting TinyTapeout Project Processing")
    print(f"Working directory: {os.getcwd()}")
    print(f"GitHub URL: {args.github_url}")
    
    github_url = args.github_url
    original_dir = os.getcwd()  # Store the original directory for manifest updates
    
    # Step 1: Clone project and rename based on project type
    success, output = run_command(
        f"get_project.py {github_url}",
        "Clone project and rename based on project type (wokwi or verilog)"
    )
    
    if not success:
        print("❌ Failed to clone and rename project. Exiting...")
        play_sound("error")
        sys.exit(1)
    
    # Parse the directory name from the output
    project_dir = None
    for line in output.split('\n'):
        if "Success! Project cloned and renamed to:" in line:
            # Extract directory name from the line
            project_dir = line.split(":")[-1].strip()
            break
    
    if not project_dir:
        print("❌ Could not parse project directory from get_project.py output. Exiting...")
        play_sound("error")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"Step: Change to project directory")
    print(f"Directory: {project_dir}")
    print(f"{'='*60}")
    
    try:
        os.chdir(project_dir)
        print(f"✅ Successfully changed to: {os.getcwd()}")
    except Exception as e:
        print(f"❌ Failed to change directory: {e}")
        play_sound("error")
        sys.exit(1)
    
    # Step 2: Clone tt-support-tools repository
    success, _ = run_command(
        "git clone https://github.com/TinyTapeout/tt-support-tools.git tt",
        "Clone tt-support-tools repository"
    )
    if not success:
        print("❌ Failed to clone repository. Exiting...")
        play_sound("error")
        sys.exit(1)
    
    # Step 3: Create user configuration
    success, _ = run_command(
        "python3 tt/tt_tool.py --create-user-config",
        "Create user configuration"
    )
    if not success:
        print("❌ Failed to create user configuration. Exiting...")
        play_sound("error")
        sys.exit(1)
    
    # Step 4: Harden the project
    success, _ = run_command(
        "python3 tt/tt_tool.py --harden",
        "Harden the project"
    )
    if not success:
        print("❌ Failed to harden project. Exiting...")
        play_sound("error")
        sys.exit(1)
    
    # Step 5: Create TT submission
    success, _ = run_command(
        "python3 tt/tt_tool.py --create-tt-submission",
        "Create TT submission"
    )
    if not success:
        print("❌ Failed to create TT submission. Exiting...")
        play_sound("error")
        sys.exit(1)
    
    # Step 6: Copy hardened project
    success, _ = run_command(
        "copy_hardened_project.py",
        "Copy hardened project files"
    )
    if not success:
        print("❌ Failed to copy hardened project. Exiting...")
        play_sound("error")
        sys.exit(1)
    
    # Step 7: Update project manifest
    # Get the current directory name (should be the project directory)
    current_dir = os.path.basename(os.getcwd())
    project_name = current_dir
    
    print(f"\n{'='*60}")
    print(f"Step: Update project manifest")
    print(f"Project: {project_name}")
    print(f"GitHub URL: {github_url}")
    print(f"Manifest location: {original_dir}")
    print(f"{'='*60}")
    
    if not update_project_manifest(project_name, github_url, current_dir, original_dir):
        print("❌ Failed to update project manifest. Continuing...")
    
    print("\n🎉 TinyTapeout project setup completed successfully!")
    print("\nNext steps:")
    print("- Review the generated files")
    print("- Test your project")
    
    # Play success sound
    play_sound("success")
    print("- Submit to TinyTapeout if ready")


if __name__ == "__main__":
    main()
