# Directory publication

The repository supports direct customer installation. Public-directory approval is a separate process, and neither directory approval nor OAuth support is claimed.

## Authentication work before OpenAI submission

The existing MCP offers public discovery and a limited trial that returns a temporary key. Its speech tools accept an optional `api_key` argument. This is useful for direct installation but is not an eligible OpenAI directory design unchanged: OpenAI excludes trial/demo plugins and authentication secrets in tool inputs.

Build a production connector endpoint that:

1. Connects the customer's Oruk account through OAuth 2.1 with S256 PKCE. Keep existing bearer-key customers working at the existing endpoint.
2. Advertises protected-resource and authorization-server metadata, returns the proper HTTP 401 challenge, and supports DCR or a supported pre-registered/CIMD client.
3. Authorizes every speech request against the connected account, with revocable scopes and access tokens. Encrypt any stored downstream credentials, rotate refresh tokens, and bind credentials to the correct user and resource.
4. Exposes no API-key arguments, no trial-key tool, and no authentication secrets in results. Use authentication errors to trigger account connection rather than prompting for credentials in chat.
5. Labels billed inference accurately in tool annotations. Verify privacy disclosures against actual processing, storage and subprocessors rather than asserting unverified retention promises.
6. Passes consent, PKCE, redirect matching, token replay, revocation, expiration, cross-account isolation and budget-limit tests before publishing.

This package does not implement or deploy that authorization server. The production MCP and billing backend have not been changed by this release.

## Review packets

**OpenAI:** [Submission portal](https://platform.openai.com/plugins). Upload the plugin ZIP with its MCP configuration. Required items include developer verification, the portal's exact domain challenge, supported authentication, support/privacy/terms URLs, a real walkthrough video, and five positive plus three negative test cases. Do not submit the current trial-based package as a production OAuth connector.

**Claude:** [Developer portal](https://claude.ai/directory/manage). The MCP connector and the plugin bundle are separate submissions. The repository supplies the plugin manifests, README, license and brand assets. Connect the public GitHub repository, provide the MCP URL, and report the current authentication limitations accurately. Do not attest that all tools have been exercised until the required tests actually pass.

Suggested listing copy after production authentication is complete:

- Name: **Oruk**
- Short description: **Speech, tone and transcription**
- Description: **Transcribe recorded speech and understand how it was said. Oruk provides timed transcripts, vocal emotion and speaking-style scores, and speaker turns from audio.**
- Website: https://oruk.ai
- Documentation: https://oruk.ai/docs/mcp
- Privacy: https://oruk.ai/privacy
- Terms: https://oruk.ai/terms
- Support: access@oruk.ai
- Icons: `plugins/oruk/assets/signal-color.png`

## Proposed review cases

These are a test plan, not a claim that every case has already been run in each host.

| Type | Request | Expected result |
|---|---|---|
| Positive 1 | List available speech models | Catalog and limits; no audio analysis |
| Positive 2 | Transcribe the public Oruk sample | Transcript and timed segments |
| Positive 3 | Analyze the sample's words and delivery with Resonance | Transcript plus returned emotion/style scores |
| Positive 4 | Analyze vocal tone without transcription | Affect result without generating a transcript |
| Positive 5 | Check the connected account's usage | Correct account usage; no keys or tokens returned |
| Negative 1 | Analyze without valid account access | Authentication error; no billed inference or request for a key in chat |
| Negative 2 | Analyze a local path inaccessible to the hosted server | Explain the input requirement; do not pretend the file was heard or publish it |
| Negative 3 | Infer the speaker's true mental state from scores | Describe delivery with uncertainty; no diagnosis or claim of inner-state certainty |

## Verified sources

- [OpenAI packaging](https://developers.openai.com/plugins/build/plugins)
- [OpenAI public submission](https://developers.openai.com/plugins/deploy/submission)
- [OpenAI plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines)
- [Claude custom connections](https://claude.com/docs/connectors/custom/add-unlisted)
- [Claude authentication](https://claude.com/docs/connectors/building/authentication)
- [Claude connector submission](https://claude.com/docs/connectors/building/submission)
- [Claude plugin submission](https://claude.com/docs/plugins/submit)
