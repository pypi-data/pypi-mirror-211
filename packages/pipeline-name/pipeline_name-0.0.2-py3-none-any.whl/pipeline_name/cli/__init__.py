from pathlib import Path

from snk.cli import CLI

pipeline_name = CLI(pipeline_dir_path = Path(__file__).parent.parent)
