from pathlib import Path

import pytest


def require_symlink_support(tmp_path: Path) -> None:
    link = tmp_path / "link"
    target = tmp_path / "target"
    target.write_text("x", encoding="utf-8")
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is not supported in this environment")
    link.unlink()


def _make_pack(tmp_path: Path) -> Path:
    pack = tmp_path / "pack"
    tree = pack / "tree"
    (tree / "docs").mkdir(parents=True)
    (tree / "README.md").write_text("# Example\n", encoding="utf-8")
    (tree / "docs" / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
    return pack


def _make_cli_pack(tmp_path: Path) -> Path:
    pack = tmp_path / "pack"
    tree = pack / "tree"
    (tree / "docs").mkdir(parents=True)
    (tree / "README.md").write_text("# From pack\n", encoding="utf-8")
    (tree / "docs" / "new.md").write_text("# New\n", encoding="utf-8")
    return pack


@pytest.fixture
def pack_dir(tmp_path: Path) -> Path:
    return _make_pack(tmp_path)


@pytest.fixture
def cli_pack_dir(tmp_path: Path) -> Path:
    return _make_cli_pack(tmp_path)
