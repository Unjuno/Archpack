from pathlib import Path

from archpack.cli import main
from archpack.plugins.agents.generator import generate_agents, load_agent_rules


def make_agents_pack(tmp_path: Path) -> Path:
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "agents.toml").write_text(
        """
[[agents]]
dir = "."
rules = ["Keep instructions short."]

[[agents]]
dir = "src"
rules = ["Keep application code under src."]
""".strip()
        + "\n",
        encoding="utf-8",
    )
    return pack


def test_load_agent_rules(tmp_path: Path) -> None:
    pack = make_agents_pack(tmp_path)

    blocks = load_agent_rules(pack)

    assert [block.directory.as_posix() for block in blocks] == [".", "src"]
    assert blocks[0].rules == ("Keep instructions short.",)


def test_generate_agents_writes_agents_files(tmp_path: Path) -> None:
    pack = make_agents_pack(tmp_path)
    out = tmp_path / "out"

    result = generate_agents(pack, out)

    assert sorted(path.as_posix() for path in result.written) == ["AGENTS.md", "src/AGENTS.md"]
    assert "Keep instructions short." in (out / "AGENTS.md").read_text(encoding="utf-8")
    assert "Keep application code under src." in (out / "src" / "AGENTS.md").read_text(encoding="utf-8")


def test_generate_agents_skips_existing_by_default(tmp_path: Path) -> None:
    pack = make_agents_pack(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "AGENTS.md").write_text("user edit\n", encoding="utf-8")

    result = generate_agents(pack, out)

    assert "AGENTS.md" in [path.as_posix() for path in result.skipped]
    assert (out / "AGENTS.md").read_text(encoding="utf-8") == "user edit\n"
    assert (out / "src" / "AGENTS.md").exists()


def test_generate_agents_overwrite_replaces_existing(tmp_path: Path) -> None:
    pack = make_agents_pack(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "AGENTS.md").write_text("user edit\n", encoding="utf-8")

    result = generate_agents(pack, out, overwrite=True)

    assert "AGENTS.md" in [path.as_posix() for path in result.written]
    assert "Keep instructions short." in (out / "AGENTS.md").read_text(encoding="utf-8")


def test_agents_generate_cli(tmp_path: Path) -> None:
    pack = make_agents_pack(tmp_path)
    out = tmp_path / "out"

    exit_code = main(["agents-generate", str(pack), "--out", str(out)])

    assert exit_code == 0
    assert (out / "AGENTS.md").exists()
    assert (out / "src" / "AGENTS.md").exists()
