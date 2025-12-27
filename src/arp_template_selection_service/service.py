from __future__ import annotations

import uuid

from arp_standard_model import (
    Candidate,
    CandidateSet,
    CandidateSetRequest,
    Health,
    NodeTypeRef,
    SelectionGenerateCandidateSetRequest,
    SelectionHealthRequest,
    SelectionVersionRequest,
    Status,
    VersionInfo,
)
from arp_standard_server.selection import BaseSelectionServer

from . import __version__
from .node_registry_client import NodeRegistryGatewayClient
from .utils import now


class SelectionService(BaseSelectionServer):
    """Selection surface; implement your candidate generation here."""

    # Core method - API surface and main extension points
    def __init__(
        self,
        *,
        service_name: str = "arp-template-selection-service",
        service_version: str = __version__,
        node_registry: NodeRegistryGatewayClient | None = None,
    ) -> None:
        """
        Not part of ARP spec; required to construct the selection service.

        Args:
          - service_name: Name exposed by /v1/version.
          - service_version: Version exposed by /v1/version.
          - node_registry: Optional wrapper for Node Registry calls.

        Potential modifications:
          - Inject your selection engine or model.
          - Add caching or persistence for candidate sets.
        """
        self._service_name = service_name
        self._service_version = service_version
        self._node_registry = node_registry

    # Core methods - Selection API implementations
    async def health(self, request: SelectionHealthRequest) -> Health:
        """
        Mandatory: Required by the ARP Selection API.

        Args:
          - request: SelectionHealthRequest (unused).
        """
        _ = request
        return Health(status=Status.ok, time=now())

    async def version(self, request: SelectionVersionRequest) -> VersionInfo:
        """
        Mandatory: Required by the ARP Selection API.

        Args:
          - request: SelectionVersionRequest (unused).
        """
        _ = request
        return VersionInfo(
            service_name=self._service_name,
            service_version=self._service_version,
            supported_api_versions=["v1"],
        )

    async def generate_candidate_set(self, request: SelectionGenerateCandidateSetRequest) -> CandidateSet:
        """
        Mandatory: Required by the ARP Selection API.

        Args:
          - request: SelectionGenerateCandidateSetRequest with subtask + constraints.

        Potential modifications:
          - Replace the default candidate list with your own selection logic.
          - Respect constraints and budgets when generating candidates.
        """
        return self._generate(request.body)

    # Helpers (internal): implementation detail for the template.
    def _generate(self, request: CandidateSetRequest) -> CandidateSet:
        """Minimal selection strategy (edit/extend this)."""
        max_k = None
        if request.constraints and request.constraints.candidates:
            max_k = request.constraints.candidates.max_candidates_per_subtask

        candidates = [
            Candidate(
                node_type_ref=NodeTypeRef(node_type_id="atomic.echo", version="0.1.0"),
                score=1.0,
                rationale="Template default candidate.",
            )
        ]
        if isinstance(max_k, int) and max_k >= 1:
            candidates = candidates[:max_k]

        return CandidateSet(
            candidate_set_id=str(uuid.uuid4()),
            subtask_id=request.subtask_spec.subtask_id,
            candidates=candidates,
            top_k=max_k,
            generated_at=now(),
            constraints=request.constraints,
            extensions=request.extensions,
        )
