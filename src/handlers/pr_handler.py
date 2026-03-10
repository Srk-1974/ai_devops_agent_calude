from ..services.ado_service import ADOService
from ..services.ai_service import AIService
from ..models.webhook_models import ADOWebhookPayload

class PRAnalyzerHandler:
    def __init__(self, settings, cosmos):
        self.settings = settings
        self.cosmos = cosmos
        self._ado = ADOService()
        self._ai = AIService()

    async def handle(self, payload: ADOWebhookPayload):
        resource = payload.resource
        pr_id = resource.get("pullRequestId")
        target_ref = resource.get("targetRefName")
        repo_id = resource.get("repository", {}).get("id")
        
        # Branch filter: Should skip PRs not targeting main/master/develop.
        target_branches = ["refs/heads/main", "refs/heads/master", "refs/heads/develop"]
        if target_ref not in target_branches:
            return {"skipped": True, "reason": "non-target branch"}
            
        try:
            diff = await self._ado.get_pr_diff(pr_id)
        except Exception as e:
            # Should still call AI and post comment even if diff fetch fails.
            diff = f"Error fetching diff: {str(e)}"
            
        # Call AI
        analysis = await self._ai.review_pull_request(diff)
        
        # Post comment
        await self._ado.post_pr_comment(pr_id, analysis)
        
        # Persist result
        await self.cosmos.save_pr_analysis(pr_id, repo_id, analysis)
        
        return {
            "prId": pr_id,
            "commentPosted": True
        }
