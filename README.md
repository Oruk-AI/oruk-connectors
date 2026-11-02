<img src="plugins/oruk/assets/oruk-primary.svg" alt="oruk" width="180">

# Oruk for Codex and Claude

Transcribe recorded speech and understand how it was said. The Oruk connector gives your assistant transcripts, timed segments, emotion scores and speaking-style scores from audio.

This package connects to **https://oruk.ai/mcp**, Oruk's hosted MCP server. You don't need to run a server or download models. Bring an Oruk API key for ongoing use; public model information and setup help work without one.

## Connect Codex

Add the production connection:

```sh
codex mcp add oruk --url https://oruk.ai/mcp --bearer-token-env-var ORUK_API_KEY
```

Set `ORUK_API_KEY` in the environment that launches Codex, using the key from [your Oruk account](https://oruk.ai/account). Do not paste it into chat. Codex desktop, CLI and IDE clients on the same host share MCP configuration. A desktop app launched from Finder may not inherit your terminal environment; configure its credential environment before expecting authenticated calls to work.

Then ask: **“Check my Oruk usage.”**

For model discovery without an account, omit `--bearer-token-env-var ORUK_API_KEY`. The server also offers a limited temporary trial; this is separate from a permanent connection.

## Connect Claude Code

Create a project `.mcp.json`, or merge this server entry into your existing file:

```json
{
  "mcpServers": {
    "oruk": {
      "type": "http",
      "url": "https://oruk.ai/mcp",
      "headers": {
        "Authorization": "Bearer ${ORUK_API_KEY}"
      }
    }
  }
}
```

Set `ORUK_API_KEY` in Claude Code's environment, then use `/mcp` to check the connection. The placeholder is resolved by Claude Code; no key belongs in the repository.

For public tools without an account:

```sh
claude mcp add --transport http --scope user oruk https://oruk.ai/mcp
```

## Connect Claude web or Desktop

Open **Customize → Connectors → Add custom connector**, enter `https://oruk.ai/mcp`, and select **No sign-in**. This enables public tools and the limited trial.

Some organizations have **Request headers** enabled. If yours does, add `Authorization` with `Bearer <your Oruk API key>` in the connector settings for ongoing account access. This feature is not available to every organization. Where it is absent, use Claude Code for permanent API-key access. This server does not currently offer OAuth; don't select OAuth or put a permanent key into a chat or a URL.

## Install the workflow package

The package adds a focused speech-analysis skill alongside the remote MCP connection. Its default connection contains **no credentials**, so it starts with public tools and the limited trial. Use the direct connection above for permanent API-key access. Avoid installing both routes in the same client unless you want duplicate tools.

### Codex plugin

```sh
codex plugin marketplace add Oruk-AI/oruk-connectors
codex plugin add oruk@oruk-connectors
```

If your Codex version does not expose plugin installation in the CLI, install it from the Oruk marketplace in the app after adding the marketplace. Start a new chat after installation.

### Claude Code plugin

```text
/plugin marketplace add Oruk-AI/oruk-connectors
/plugin install oruk@oruk-connectors
```

The same `plugins/oruk` directory includes the Claude plugin manifest for supported plugin import flows. This repository distribution is separate from approval in either company's public directory.

## Try it

> Use Oruk to transcribe https://oruk.ai/samples/oruk-quickstart.wav and describe the speaker's delivery. Use Resonance and include timestamps.

| Tool | Use |
|---|---|
| `oruk_analyze_speech` | Transcript, emotion and speaking-style scores in one request |
| `oruk_transcribe_audio` | Transcript and timed segments |
| `oruk_analyze_tone` | Emotion and speaking-style scores without transcription |
| `oruk_check_usage` | Check the configured key, subscription and usage |
| `oruk_list_models` | Inspect models, limits and pricing information |
| `oruk_get_started` | Read setup guidance |

The server also exposes temporary trial creation and a bounded Hume migration planning tool. The live catalog is authoritative. Not every model in Oruk's general catalog is callable through these MCP tools.

For transcript **and** speaking-style scores, select `model: "oruk-resonance"`. Use prerecorded English audio: public URLs up to 30 MB, or base64 audio up to 8 MiB decoded, with a maximum duration of 60 minutes. A local file path or a chat attachment is not automatically accessible to the remote server. Only send recordings the user has chosen to process; don't publish private audio to obtain a URL.

Emotion and style scores describe acoustic delivery, not a person's actual mental state. These tools do not generate speech, diagnose people, or establish whether someone is truthful.

## Check the connection

Python 3.9+; no third-party Python packages required:

```sh
python3 scripts/check.py
```

This checks initialization, notifications, tool discovery, public tool calls, and missing-key behavior. It does not consume account minutes.

To test one public sample using a single temporary trial key:

```sh
python3 scripts/check.py --free-trial
```

To test a permanent key from `ORUK_API_KEY` instead (consumes account minutes):

```sh
python3 scripts/check.py --account
```

The checker never prints or saves keys, audio, or transcripts. It does not automatically retry trial creation. A limited or unavailable trial is not a reason to repeatedly mint keys.

## Data and support

Audio selected for analysis is sent to Oruk's hosted service. This package does not run models locally and does not add a separate analytics service. Hosted processing is governed by [Oruk's privacy policy](https://oruk.ai/privacy) and [terms](https://oruk.ai/terms). See the [API documentation](https://oruk.ai/docs) and [MCP documentation](https://oruk.ai/docs/mcp), or contact **access@oruk.ai**.

The connector code is MIT licensed. Oruk brand assets and hosted service access are covered separately; see [LICENSE](LICENSE).

## Public directory status

Direct customer installation is supported by this repository. **Neither an OpenAI nor an Anthropic directory approval is claimed.** OpenAI's public directory requires an authentication design that does not expose credentials as tool arguments; the current trial-key design is not eligible unchanged. See [directory readiness](docs/directory-readiness.md) for the remaining work and review cases.
