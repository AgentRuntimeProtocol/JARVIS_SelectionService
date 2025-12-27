import asyncio

from arp_standard_model import (
    CandidateSetRequest,
    Candidates,
    ConstraintEnvelope,
    SelectionGenerateCandidateSetRequest,
    SubtaskSpec,
)
from arp_template_selection_service.service import SelectionService


def test_generate_candidate_set_respects_max_k() -> None:
    service = SelectionService()
    request = SelectionGenerateCandidateSetRequest(
        body=CandidateSetRequest(
            subtask_spec=SubtaskSpec(subtask_id="subtask_1", goal="test"),
            constraints=ConstraintEnvelope(
                candidates=Candidates(max_candidates_per_subtask=1),
            ),
        )
    )

    result = asyncio.run(service.generate_candidate_set(request))

    assert result.candidate_set_id
    assert result.top_k == 1
    assert len(result.candidates) == 1
