#!/usr/bin/env python
"""Diagnostic script to test TTS app setup"""

import sys
from pathlib import Path

print("=" * 60)
print("TTS App - Diagnostic Check")
print("=" * 60)

# Check Python version
print(f"\n✓ Python version: {sys.version}")

# Check required modules
required_modules = ["flask", "edge_tts", "asyncio"]
print("\nChecking required modules:")
for module in required_modules:
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except ImportError as e:
        print(f"  ✗ {module} - NOT INSTALLED")
        print(f"    Error: {e}")
        print(f"    Fix: pip install {module}")

# Check story file
story_path = Path("/workspaces/TTS/input/hindi_story.txt")
print(f"\nChecking story file:")
if story_path.exists():
    size = story_path.stat().st_size
    print(f"  ✓ Story file exists: {size} bytes")
    content = story_path.read_text(encoding="utf-8")
    if "[NAME]" in content:
        print(f"  ✓ Contains [NAME] placeholder")
    else:
        print(f"  ✗ Missing [NAME] placeholder")
else:
    print(f"  ✗ Story file NOT FOUND: {story_path}")

# Check output directory
output_dir = Path("/workspaces/TTS/output")
print(f"\nChecking output directory:")
if output_dir.exists():
    print(f"  ✓ Output directory exists: {output_dir}")
else:
    print(f"  ! Output directory will be created at runtime")

# Check Flask templates
template_dir = Path("/workspaces/TTS/templates")
print(f"\nChecking templates:")
if (template_dir / "index.html").exists():
    print(f"  ✓ Template file exists: templates/index.html")
else:
    print(f"  ✗ Template NOT FOUND: templates/index.html")

# Check app.py
app_file = Path("/workspaces/TTS/app.py")
print(f"\nChecking app.py:")
if app_file.exists():
    print(f"  ✓ app.py exists")
    # Try to import it
    try:
        sys.path.insert(0, str(app_file.parent))
        from app import app as flask_app
        print(f"  ✓ app.py can be imported successfully")
    except Exception as e:
        print(f"  ✗ app.py import failed: {e}")
else:
    print(f"  ✗ app.py NOT FOUND")

print("\n" + "=" * 60)
print("Diagnostic Complete!")
print("=" * 60)
print("\nTo start the app, run:")
print("  python /workspaces/TTS/app.py")
print("\nThen open: http://localhost:5000")
print("=" * 60)
