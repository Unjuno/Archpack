from pathlib import Path

import pytest

from archpack.plugins.agents.generator import AgentsPluginError, load_agent_rules


def write_agents_toml(pack: Path, content: str) -> None:
    pack.mkdir()
    (pack / "agents.toml").write_text(content.strip() + "\n", encoding="utf-8")


def test_agents_reject_parent_directory_escape(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    write_agents_toml(
        pack,
        """
[[agents]]
dir = ".."
rules = ["bad"]
""",
    )

    with pytest.raises(AgentsPluginError):
        load_agent_rules(pack)


def test_agents_reject_absolute_directory(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    write_agents_toml(
        pack,
        """
[[agents]]
dir = "/tmp"
rules = ["bad"]
""",
    )

    with pytest.raises(AgentsPluginError):
        load_agent_rules(pack)


def test_agents_reject_duplicate_directories(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    write_agents_toml(
        pack,
        """
[[agents]]
dir = "src"
rules = ["first"]

[[agents]]
dir = "./src"
rules = ["second"]
""",
    )

    with pytest.raises(AgentsPluginError):
        load_agent_rules(pack)


def test_agents_reject_empty_rule(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    write_agents_toml(
        pack,
        """
[[agents]]
dir = "."
rules = [""]
""",
    )

    with pytest.raises(AgentsPluginError):
        load_agent_rules(pack)


def test_agents_reject_multiline_rule(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    write_agents_toml(
        pack,
        '''
[[agents]]
dir = "."
rules = ["first line\\nsecond line"]
''',
    )

    with pytest.raises(AgentsPluginError):
        load_agent_rules(pack)


def test_agents_wrap_toml_parse_errors(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "agents.toml").write_text("[[agents]\n", encoding="utf-8")

    with pytest.raises(AgentsPluginError, match="Invalid agents.toml"):
        load_agent_rules(pack)
