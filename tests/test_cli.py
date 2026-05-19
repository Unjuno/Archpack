from pathlib import Path

from archpack.cli import main


def test_unpack_skip_existing_adds_missing_files_without_changing_existing(
    cli_pack_dir: Path, tmp_path: Path
) -> None:
    pack = cli_pack_dir
    out = tmp_path / "out"
    out.mkdir()
    (out / "README.md").write_text("user edit\n", encoding="utf-8")

    exit_code = main(["unpack", str(pack), "--out", str(out), "--skip-existing"])

    assert exit_code == 0
    assert (out / "README.md").read_text(encoding="utf-8") == "user edit\n"
    assert (out / "docs" / "new.md").read_text(encoding="utf-8") == "# New\n"
