import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from src.handlers.pr_handler import PRAnalyzerHandler
from src.models.webhook_models import ADOWebhookPayload
from src.config import Settings
from src.services.cosmos_service import CosmosService


@pytest.fixture
def settings():
    return Settings(
        ado_organization="test-org",
        ado_project="test-project",
        ado_pat="test-pat",
        azure_openai_endpoint="https://test.openai.azure.com/",
        azure_openai_api_key="test-key",
        environment="test",
    )


@pytest.fixture
def cosmos():
    cosmos = MagicMock(spec=CosmosService)
    cosmos.save_pr_analysis = AsyncMock()
    return cosmos


def make_pr_payload(pr_id: int = 42, target_ref: str = "refs/heads/main", event_type: str = "git.pullrequest.created"):
    return ADOWebhookPayload(
        id="evt-001",
        eventType=event_type,
        resource={
            "pullRequestId": pr_id,
            "title": "feat: add payment gateway",
            "description": "Adds Stripe payment integration",
            "status": "active",
            "targetRefName": target_ref,
            "sourceRefName": "refs/heads/feat/payment",
            "createdBy": {"displayName": "Alice Dev"},
            "repository": {"id": "repo-123"},
            "url": f"https://dev.azure.com/test/_apis/git/repositories/repo-123/pullRequests/{pr_id}",
        },
    )


@pytest.mark.asyncio
async def test_pr_review_happy_path(settings, cosmos):
    """Should fetch diff, call AI, post comment, persist result."""
    with (
        patch("src.handlers.pr_handler.ADOService") as MockADO,
        patch("src.handlers.pr_handler.AIService") as MockAI,
    ):
        mock_ado = MockADO.return_value
        mock_ado.get_pr_diff = AsyncMock(return_value="+ added line\n- removed line")
        mock_ado.post_pr_comment = AsyncMock()

        mock_ai = MockAI.return_value
        mock_ai.review_pull_request = AsyncMock(return_value="## Review\nLooks good!")

        handler = PRAnalyzerHandler(settings, cosmos)
        handler._ado = mock_ado
        handler._ai = mock_ai

        result = await handler.handle(make_pr_payload())

    assert result["prId"] == 42
    assert result["commentPosted"] is True
    mock_ado.post_pr_comment.assert_awaited_once()
    cosmos.save_pr_analysis.assert_awaited_once_with(42, "repo-123", "## Review\nLooks good!")


@pytest.mark.asyncio
async def test_pr_skipped_for_non_target_branch(settings, cosmos):
    """Should skip PRs not targeting main/master/develop."""
    handler = PRAnalyzerHandler(settings, cosmos)
    result = await handler.handle(make_pr_payload(target_ref="refs/heads/feature/experiment"))
    assert result["skipped"] is True
    assert "non-target branch" in result["reason"]


@pytest.mark.asyncio
async def test_pr_diff_failure_gracefully_handled(settings, cosmos):
    """Should still call AI and post comment even if diff fetch fails."""
    with (
        patch("src.handlers.pr_handler.ADOService") as MockADO,
        patch("src.handlers.pr_handler.AIService") as MockAI,
    ):
        mock_ado = MockADO.return_value
        mock_ado.get_pr_diff = AsyncMock(side_effect=Exception("Network error"))
        mock_ado.post_pr_comment = AsyncMock()

        mock_ai = MockAI.return_value
        mock_ai.review_pull_request = AsyncMock(return_value="## Review\nNo diff available.")

        handler = PRAnalyzerHandler(settings, cosmos)
        handler._ado = mock_ado
        handler._ai = mock_ai

        result = await handler.handle(make_pr_payload())

    # Should still complete — diff failure is non-fatal
    assert result["commentPosted"] is True
    mock_ai.review_pull_request.assert_awaited_once()
