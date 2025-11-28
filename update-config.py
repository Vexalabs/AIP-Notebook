#!/usr/bin/env python3
"""
Update config to use AI-Predictions-Model-Templates repository
"""
import json
import os
from pathlib import Path

# Find config file
config_path = Path(__file__).parent / ".secrets" / "config.json"

if not config_path.exists():
    print(f"❌ Config file not found at {config_path}")
    exit(1)

# Read current config
with open(config_path, 'r') as f:
    config = json.load(f)

# Update repository settings
if "github" not in config:
    config["github"] = {}

config["github"]["repo_owner"] = "Vexalabs"
config["github"]["repo_name"] = "AI-Predictions-Model-Templates"

# Save updated config
with open(config_path, 'w') as f:
    json.dump(config, f, indent=4)

print("✅ Config updated successfully!")
print(f"   Repository: {config['github']['repo_owner']}/{config['github']['repo_name']}")
print("")
print("The backend will auto-reload with the new configuration.")
print("You can now test submission and restore features.")
