#!/usr/bin/env python3
"""Copy the prebuilt competition entry into the requested output directory."""
import os
import shutil
from pathlib import Path

source = Path(__file__).resolve().with_name('entry.png')
if not source.is_file():
    raise FileNotFoundError(f'Required prebuilt entry image is missing: {source}')
output = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
output.mkdir(parents=True, exist_ok=True)
destination = output / 'entry.png'
shutil.copyfile(source, destination)
print(f'Copied {source} to {destination}')
