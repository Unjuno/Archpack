from pathlib import Path

from archpack.cli import main


def make_pack(tmp_path: Path) -> Path:
    pack = tmp_path / "pack"
    tree = pack / "tree"
    (tree / "docs").mkdir(parents=True)
    (tree / "README.md").write_text("# From pack\n", encoding="utf-8")
    (tree / "docs" / "new.md").write_text("# New\n", encoding="utf-8")
    return pack


def test_unpack_skip_existing_adds_missing_files_without_changing_existing(tmp_path: Path) -> None:
    pack = make_pack(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "README.md").write_text("user edit\n", encoding="utf-8")

    exit_code = main(["unpack", str(pack), "--out", str(out), "--skip-existing"])

    assert exit_code == 0
    assert (out / "README.md").read_text(encoding="utf-8") == "user edit\n"
    assert (out / "docs" / "new.md").read_text(encoding="utf-8") == "# New\n"
