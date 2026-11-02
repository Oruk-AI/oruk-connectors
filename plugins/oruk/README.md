<img src="assets/oruk-primary.svg" alt="oruk" width="180">

# Oruk

Transcribe prerecorded English speech and analyze vocal tone with Oruk's hosted MCP server. Ask for a transcript, emotion and speaking-style scores, or speaker turns. The bundled `analyze-speech` skill selects the appropriate tool and explains its output without treating acoustic scores as facts about someone's feelings.

This package connects to `https://oruk.ai/mcp`. Its default configuration contains no credentials. Public model information and setup tools work immediately; speech analysis needs a configured Oruk API key or a limited temporary trial. For permanent account access, use the [Codex and Claude setup instructions](https://github.com/Oruk-AI/oruk-connectors#connect-codex). Never paste a permanent API key into chat.

Install in Claude Code 2.1.275 or later:

```text
/plugin install oruk --marketplace Oruk-AI/oruk-connectors
```

Example: “Use Oruk to transcribe https://oruk.ai/samples/oruk-quickstart.wav and describe the delivery. Use Resonance and include timestamps.”

Audio is processed by the Oruk service, not locally. Public URL inputs support up to 30 MB, inline base64 up to 8 MiB decoded, and recordings up to 60 minutes. The MCP audio tools currently accept English speech. They do not generate speech or diagnose people.

[Documentation](https://oruk.ai/docs/mcp) · [Privacy](https://oruk.ai/privacy) · [Terms](https://oruk.ai/terms) · Support: **access@oruk.ai**

This is a direct-install package. It does not imply approval in the OpenAI or Claude public directories.
