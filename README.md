# ARP Template Selection Service

Use this repo as a starting point for building an **ARP compliant Selection Service**.

The Selection Service produces bounded candidate sets for mapping subtasks to NodeTypes. The selection strategy is intentionally implementation-defined; this template provides a small, deterministic baseline.

This minimal template implements the Selection API using only the SDK packages:
`arp-standard-server`, `arp-standard-model`, and `arp-standard-client`.

Implements: ARP Standard `spec/v1` Selection API (contract: `ARP_Standard/spec/v1/openapi/selection.openapi.yaml`).

## Requirements

- Python >= 3.10

## Install

```bash
python3 -m pip install -e .
```

## Local configuration (optional)

For local dev convenience, copy the template env file:

```bash
cp .env.example .env.local
```

`src/scripts/dev_server.sh` auto-loads `.env.local` (or `.env`).

## Run

- Selection Service listens on `http://127.0.0.1:8085` by default.

```bash
python3 -m pip install -e '.[run]'
python3 -m arp_template_selection_service
```

> [!TIP]
> Use `bash src/scripts/dev_server.sh --host ... --port ... --reload` for dev convenience.

## Using this repo

To build your own selection service, fork this repository and replace the selection strategy while preserving request/response semantics.

If all you need is to change selection strategy, edit:
- `src/arp_template_selection_service/service.py`

Outgoing client wrapper (selection -> node registry):
- `src/arp_template_selection_service/node_registry_client.py`

### Default behavior

- Returns a deterministic candidate set containing `atomic.echo@0.1.0`.
- Applies `constraints.candidates.max_candidates_per_subtask` as a top-K bound when provided.

## Quick health check

```bash
curl http://127.0.0.1:8085/v1/health
```

## Configuration

CLI flags:
- `--host` (default `127.0.0.1`)
- `--port` (default `8085`)
- `--reload` (dev only)

## Validate conformance (`arp-conformance`)

```bash
python3 -m pip install arp-conformance
arp-conformance check selection --url http://127.0.0.1:8085 --tier smoke
arp-conformance check selection --url http://127.0.0.1:8085 --tier surface
```

## Helper scripts

- `src/scripts/dev_server.sh`: run the server (flags: `--host`, `--port`, `--reload`).
- `src/scripts/send_request.py`: generate a candidate set from a JSON file.

  ```bash
  python3 src/scripts/send_request.py --request src/scripts/request.json
  ```

## Authentication

For out-of-the-box usability, this template defaults to auth-disabled unless you set `ARP_AUTH_MODE` or `ARP_AUTH_PROFILE`.

To enable JWT auth, set either:
- `ARP_AUTH_PROFILE=dev-secure-keycloak` + `ARP_AUTH_SERVICE_ID=<audience>`
- or `ARP_AUTH_MODE=required` with `ARP_AUTH_ISSUER` and `ARP_AUTH_AUDIENCE`

## Upgrading

When upgrading to a new ARP Standard SDK release, bump pinned versions in `pyproject.toml` (`arp-standard-*==...`) and re-run conformance.
