from __future__ import annotations

from pathlib import Path

from .generator import generate_agents


def generate(pack_dir: Path, out_dir: Path, *, overwrite: bool = False):
    return generate_agents(pack_dir, out_dir, overwrite=overwrite)
