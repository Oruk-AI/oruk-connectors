#!/usr/bin/env python3
"""Check the hosted Oruk MCP. No credentials, audio, or transcripts are logged."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

ENDPOINT = "https://oruk.ai/mcp"
SAMPLE = "https://oruk.ai/samples/oruk-quickstart.wav"
PROTOCOL = "2025-11-25"


class CheckError(Exception):
    pass


def rpc(method, params=None, token=None, notification=False):
    body = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        body["params"] = params
    if not notification:
        body["id"] = method
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": PROTOCOL,
        "User-Agent": "OrukConnectorCheck/1.0",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(), headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            if notification:
                if response.status != 202:
                    raise CheckError("Initialized notification did not return HTTP 202")
                return None
            data = json.load(response)
    except urllib.error.HTTPError as error:
        raise CheckError(f"{method} returned HTTP {error.code}") from None
    except (urllib.error.URLError, TimeoutError):
        raise CheckError(f"{method} could not reach Oruk") from None
    if data.get("jsonrpc") != "2.0" or data.get("id") != method:
        raise CheckError(f"{method} returned an invalid JSON-RPC response")
    if "error" in data:
        raise CheckError(f"{method} returned JSON-RPC error {data['error'].get('code')}")
    if "result" not in data:
        raise CheckError(f"{method} omitted its result")
    return data["result"]


def call(name, arguments=None, token=None):
    result = rpc("tools/call", {"name": name, "arguments": arguments or {}}, token=token)
    if result.get("isError"):
        # Do not echo provider responses: a downstream error may contain credentials.
        raise CheckError(f"{name} returned a tool error; check account access and service status")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--free-trial", action="store_true", help="Mint ONE temporary key and run ONE public sample analysis; never retries trial creation")
    parser.add_argument("--account", action="store_true", help="Verify ORUK_API_KEY and analyze one public sample (uses account minutes)")
    args = parser.parse_args()
    if args.free_trial and args.account:
        parser.error("choose --free-trial or --account")
    token = os.environ.get("ORUK_API_KEY") if args.account else None
    if args.account and not token:
        raise CheckError("Set ORUK_API_KEY in your environment before using --account")

    initialized = rpc("initialize", {"protocolVersion": PROTOCOL, "capabilities": {}, "clientInfo": {"name": "oruk-connector-check", "version": "1.0.0"}}, token=token)
    if initialized.get("protocolVersion") != PROTOCOL:
        raise CheckError("Server did not negotiate the requested protocol")
    rpc("notifications/initialized", notification=True, token=token)
    rpc("ping", token=token)
    tool_response = rpc("tools/list", token=token)
    if tool_response.get("nextCursor"):
        raise CheckError("Tool catalog now paginates; update this check before asserting full coverage")
    names = {tool["name"] for tool in tool_response.get("tools", [])}
    required = {"oruk_analyze_speech", "oruk_transcribe_audio", "oruk_analyze_tone", "oruk_list_models", "oruk_get_started", "oruk_check_usage"}
    missing = required - names
    if missing:
        raise CheckError("Missing expected tools: " + ", ".join(sorted(missing)))
    call("oruk_list_models", token=token)
    call("oruk_get_started", token=token)
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": ENDPOINT,
        "server": initialized.get("serverInfo"),
        "protocol": initialized["protocolVersion"],
        "tools": sorted(names),
        "handshake": "passed",
        "public_tools": "passed",
        "audio": "not requested",
    }
    if not args.account:
        blocked = rpc("tools/call", {"name": "oruk_analyze_speech", "arguments": {"audio_url": SAMPLE, "model": "oruk-resonance"}})
        messages = "\n".join(part.get("text", "") for part in blocked.get("content", []) if part.get("type") == "text")
        if not blocked.get("isError") or "No oruk API key was provided." not in messages:
            raise CheckError("Expected account access to be required for speech analysis")
        report["missing_key"] = "rejected as expected"
    if args.free_trial:
        trial = call("oruk_create_trial_key")
        token = trial.get("structuredContent", {}).get("token")
        if not isinstance(token, str) or not token.startswith("oruk_test_"):
            raise CheckError("Trial creation did not return a temporary key")
    if args.free_trial or args.account:
        if args.account:
            call("oruk_check_usage", token=token)
        # Exercise the permanent-connection header path, even with a temporary key.
        result = call("oruk_analyze_speech", {"audio_url": SAMPLE, "model": "oruk-resonance", "detail": "compact"}, token=token)
        structured = result.get("structuredContent", {})
        if not structured.get("text") or not structured.get("segments"):
            raise CheckError("Sample analysis did not return transcript and segments")
        if structured.get("model") != "oruk-resonance":
            raise CheckError("Sample analysis used an unexpected model")
        report["audio"] = {"status": "passed", "model": structured["model"], "transcript_characters": len(structured["text"]), "segments": len(structured["segments"])}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (CheckError, json.JSONDecodeError, KeyError) as error:
        print(json.dumps({"status": "failed", "reason": str(error)}), file=sys.stderr)
        sys.exit(1)
