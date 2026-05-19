from pathlib import Path

import pytest

from archpack.plugins.agents.generator import AgentsPluginError, generate_agents, load_agent_rules


def make_inherited_pack(tmp_path: Path) -> Path:
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "agents.toml").write_text(
        """
[[agents]]
dir = "."
rules = ["Root rule"]

[[agents]]
dir = "src"
rules = ["Src rule"]

[[agents]]
dir = "src/services"
rules = ["Services rule"]
""".strip()
        + "\n",
        encoding="utf-8",
    )
    return pack


def test_agents_are_generated_per_declared_directory(tmp_path: Path) -> None:
    pack = make_inherited_pack(tmp_path)
    out = tmp_path / "out"

    result = generate_agents(pack, out)

    assert sorted(path.as_posix() for path in result.written) == [
        "AGENTS.md",
        "src/AGENTS.md",
        "src/services/AGENTS.md",
    ]


def test_child_agents_include_parent_rules(tmp_path: Path) -> None:
    pack = make_inherited_pack(tmp_path)
    out = tmp_path / "out"

    generate_agents(pack, out)

    root_text = (out / "AGENTS.md").read_text(encoding="utf-8")
    src_text = (out / "src" / "AGENTS.md").read_text(encoding="utf-8")
    services_text = (out / "src" / "services" / "AGENTS.md").read_text(encoding="utf-8")

    assert "Root rule" in root_text
    assert "Src rule" not in root_text
    assert "Services rule" not in root_text

    assert "Root rule" in src_text
    assert "Src rule" in src_text
    assert "Services rule" not in src_text

    assert "Root rule" in services_text
    assert "Src rule" in services_text
    assert "Services rule" in services_text


def test_agent_rule_block_rejects_more_than_30_rules(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    rules = ",\n".join(f'  "rule {index}"' for index in range(31))
    (pack / "agents.toml").write_text(
        f"""
[[agents]]
dir = "."
rules = [
{rules}
]
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(AgentsPluginError):
        load_agent_rules(pack)
