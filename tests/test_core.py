from pathlib import Path

import pytest

from archpack.core import ExistingFileError, UnsafePathError, repair, unpack, validate_relative_path

from conftest import require_symlink_support


def test_unpack_generates_file_tree(pack_dir: Path, tmp_path: Path) -> None:
    out = tmp_path / "out"

    result = unpack(pack_dir, out)

    assert sorted(path.as_posix() for path in result.written) == [
        "README.md",
        "docs/architecture.md",
    ]
    assert (out / "README.md").read_text(encoding="utf-8") == "# Example\n"
    assert (out / "docs" / "architecture.md").read_text(encoding="utf-8") == "# Architecture\n"


def test_unpack_refuses_existing_file(pack_dir: Path, tmp_path: Path) -> None:
    out = tmp_path / "out"
    (out).mkdir()
    (out / "README.md").write_text("user edit\n", encoding="utf-8")

    with pytest.raises(ExistingFileError):
        unpack(pack_dir, out)

    assert (out / "README.md").read_text(encoding="utf-8") == "user edit\n"


def test_unpack_skip_existing_adds_missing_files_without_changing_existing(
    pack_dir: Path, tmp_path: Path
) -> None:
    out = tmp_path / "out"
    out.mkdir()
    (out / "README.md").write_text("user edit\n", encoding="utf-8")

    result = unpack(pack_dir, out, skip_existing=True)

    assert sorted(path.as_posix() for path in result.written) == ["docs/architecture.md"]
    assert sorted(path.as_posix() for path in result.skipped) == ["README.md"]
    assert (out / "README.md").read_text(encoding="utf-8") == "user edit\n"
    assert (out / "docs" / "architecture.md").read_text(encoding="utf-8") == "# Architecture\n"


def test_repair_restores_missing_files_only_by_default(pack_dir: Path, tmp_path: Path) -> None:
    out = tmp_path / "out"
    unpack(pack_dir, out)
    (out / "README.md").unlink()
    (out / "docs" / "architecture.md").write_text("changed\n", encoding="utf-8")

    result = repair(pack_dir, out)

    assert sorted(path.as_posix() for path in result.written) == ["README.md"]
    assert sorted(path.as_posix() for path in result.skipped) == ["docs/architecture.md"]
    assert (out / "README.md").read_text(encoding="utf-8") == "# Example\n"
    assert (out / "docs" / "architecture.md").read_text(encoding="utf-8") == "changed\n"


def test_repair_overwrite_replaces_changed_files(pack_dir: Path, tmp_path: Path) -> None:
    out = tmp_path / "out"
    unpack(pack_dir, out)
    (out / "README.md").write_text("changed\n", encoding="utf-8")

    result = repair(pack_dir, out, overwrite=True)

    assert "README.md" in [path.as_posix() for path in result.written]
    assert (out / "README.md").read_text(encoding="utf-8") == "# Example\n"


def test_pack_tree_rejects_symlink_files(pack_dir: Path, tmp_path: Path) -> None:
    require_symlink_support(tmp_path)
    target = tmp_path / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    (pack_dir / "tree" / "link.txt").symlink_to(target)

    with pytest.raises(UnsafePathError):
        unpack(pack_dir, tmp_path / "out")


def test_pack_tree_rejects_symlink_directories(pack_dir: Path, tmp_path: Path) -> None:
    require_symlink_support(tmp_path)
    target_dir = tmp_path / "target-dir"
    target_dir.mkdir()
    (target_dir / "leak.txt").write_text("leak\n", encoding="utf-8")
    (pack_dir / "tree" / "linked-dir").symlink_to(target_dir, target_is_directory=True)

    with pytest.raises(UnsafePathError):
        unpack(pack_dir, tmp_path / "out")


def test_relative_path_rejects_windows_drive_path() -> None:
    with pytest.raises(UnsafePathError):
        validate_relative_path(Path("C:/outside"))


def test_relative_path_rejects_backslash_path() -> None:
    with pytest.raises(UnsafePathError):
        validate_relative_path(Path("src/services"), raw="src\\services")


def test_relative_path_rejects_parent_segment() -> None:
    with pytest.raises(UnsafePathError):
        validate_relative_path(Path("src/../src"))


def test_relative_path_rejects_duplicate_slashes() -> None:
    with pytest.raises(UnsafePathError):
        validate_relative_path(Path("src//services"), raw="src//services")
