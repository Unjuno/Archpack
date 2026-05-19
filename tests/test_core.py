from pathlib import Path

import pytest

from archpack.core import ExistingFileError, UnsafePathError, repair, unpack


def make_pack(tmp_path: Path) -> Path:
    pack = tmp_path / "pack"
    tree = pack / "tree"
    (tree / "docs").mkdir(parents=True)
    (tree / "README.md").write_text("# Example\n", encoding="utf-8")
    (tree / "docs" / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
    return pack


def test_unpack_generates_file_tree(tmp_path: Path) -> None:
    pack = make_pack(tmp_path)
    out = tmp_path / "out"

    result = unpack(pack, out)

    assert sorted(path.as_posix() for path in result.written) == [
        "README.md",
        "docs/architecture.md",
    ]
    assert (out / "README.md").read_text(encoding="utf-8") == "# Example\n"
    assert (out / "docs" / "architecture.md").read_text(encoding="utf-8") == "# Architecture\n"


def test_unpack_refuses_existing_file(tmp_path: Path) -> None:
    pack = make_pack(tmp_path)
    out = tmp_path / "out"
    (out).mkdir()
    (out / "README.md").write_text("user edit\n", encoding="utf-8")

    with pytest.raises(ExistingFileError):
        unpack(pack, out)

    assert (out / "README.md").read_text(encoding="utf-8") == "user edit\n"


def test_unpack_skip_existing_adds_missing_files_without_changing_existing(tmp_path: Path) -> None:
    pack = make_pack(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "README.md").write_text("user edit\n", encoding="utf-8")

    result = unpack(pack, out, skip_existing=True)

    assert sorted(path.as_posix() for path in result.written) == ["docs/architecture.md"]
    assert sorted(path.as_posix() for path in result.skipped) == ["README.md"]
    assert (out / "README.md").read_text(encoding="utf-8") == "user edit\n"
    assert (out / "docs" / "architecture.md").read_text(encoding="utf-8") == "# Architecture\n"


def test_repair_restores_missing_files_only_by_default(tmp_path: Path) -> None:
    pack = make_pack(tmp_path)
    out = tmp_path / "out"
    unpack(pack, out)
    (out / "README.md").unlink()
    (out / "docs" / "architecture.md").write_text("changed\n", encoding="utf-8")

    result = repair(pack, out)

    assert sorted(path.as_posix() for path in result.written) == ["README.md"]
    assert sorted(path.as_posix() for path in result.skipped) == ["docs/architecture.md"]
    assert (out / "README.md").read_text(encoding="utf-8") == "# Example\n"
    assert (out / "docs" / "architecture.md").read_text(encoding="utf-8") == "changed\n"


def test_repair_overwrite_replaces_changed_files(tmp_path: Path) -> None:
    pack = make_pack(tmp_path)
    out = tmp_path / "out"
    unpack(pack, out)
    (out / "README.md").write_text("changed\n", encoding="utf-8")

    result = repair(pack, out, overwrite=True)

    assert "README.md" in [path.as_posix() for path in result.written]
    assert (out / "README.md").read_text(encoding="utf-8") == "# Example\n"


def test_pack_tree_rejects_symlinks(tmp_path: Path) -> None:
    pack = make_pack(tmp_path)
    target = tmp_path / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    (pack / "tree" / "link.txt").symlink_to(target)

    with pytest.raises(UnsafePathError):
        unpack(pack, tmp_path / "out")
