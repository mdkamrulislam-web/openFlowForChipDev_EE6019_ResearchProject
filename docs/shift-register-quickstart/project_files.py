"""Keep the portable seven-file starter aligned with the real project root."""
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
PROJECT_ROOT=HERE.parents[1]
FILES=(
    'info.yaml','src/shift_register.v','src/project.v',
    'test/Makefile','test/tb.v','test/test.py','docs/info.md',
)

def sync_starter():
    # A standalone learning pack still contains its portable starter snapshot.
    if not (PROJECT_ROOT/'info.yaml').is_file():return
    for name in FILES:
        source=PROJECT_ROOT/name
        if not source.is_file():raise FileNotFoundError(f'Missing documented project file: {source}')
        dest=HERE/'starter'/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists() or dest.read_bytes()!=source.read_bytes():shutil.copy2(source,dest)
