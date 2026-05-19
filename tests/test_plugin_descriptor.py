from importlib import resources


def read_agents_plugin_descriptor() -> str:
    return resources.files("archpack.plugins.agents").joinpath("plugin.yml").read_text(encoding="utf-8")


def test_agents_plugin_descriptor_is_packaged() -> None:
    descriptor = read_agents_plugin_descriptor()

    assert "id: agents" in descriptor
    assert "name: AGENTS.md generator" in descriptor
    assert "status: experimental" in descriptor


def test_agents_plugin_descriptor_links_usage_docs() -> None:
    descriptor = read_agents_plugin_descriptor()

    assert "docs:" in descriptor
    assert "usage: docs/plugins/agents.md" in descriptor


def test_agents_plugin_descriptor_declares_command_input_output_and_removal() -> None:
    descriptor = read_agents_plugin_descriptor()

    assert "name: agents-generate" in descriptor
    assert "entrypoint: archpack.plugins.agents.commands:generate" in descriptor
    assert "inputs:" in descriptor
    assert "- agents.toml" in descriptor
    assert "outputs:" in descriptor
    assert "- AGENTS.md" in descriptor
    assert '"**/AGENTS.md"' in descriptor
    assert "remove:" in descriptor
    assert "safe_to_delete:" in descriptor
