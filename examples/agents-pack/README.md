# agents-pack example

This example is for the reviewed agents plugin only.

It contains:

```text
agents.toml
```

Core commands (`unpack`, `repair`) require a `tree/` directory. This sample does not include `tree/` because it demonstrates `agents-generate` only.

For a core pack example, use:

```text
examples/minimal-pack/
```

Generate AGENTS.md files:

```bash
archpack agents-generate examples/agents-pack --out tmp/agents-out
```
