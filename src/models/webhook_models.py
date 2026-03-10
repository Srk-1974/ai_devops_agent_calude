from pydantic import BaseModel
from typing import Dict, Any

class ADOWebhookPayload(BaseModel):
    id: str
    eventType: str
    resource: Dict[str, Any]
