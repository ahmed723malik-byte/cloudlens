"""
Data models for cloud infrastructure resources.
Simulates real AWS/GCP/Azure resource discovery.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import uuid


class CloudProvider(str, Enum):
    AWS = "AWS"
    GCP = "GCP"
    AZURE = "Azure"


class ResourceType(str, Enum):
    COMPUTE = "Compute"
    STORAGE = "Storage"
    DATABASE = "Database"
    NETWORK = "Network"
    SERVERLESS = "Serverless"
    CONTAINER = "Container"
    MONITORING = "Monitoring"


class OptimisationSeverity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class CloudResource:
    name: str
    provider: CloudProvider
    resource_type: ResourceType
    region: str
    monthly_cost: float
    utilisation_pct: float
    tags: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    @property
    def cost_efficiency_score(self) -> float:
        """Higher is better: penalises low utilisation on expensive resources."""
        if self.monthly_cost == 0:
            return 100.0
        return round((self.utilisation_pct / 100) * 100, 1)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "provider": self.provider.value,
            "resource_type": self.resource_type.value,
            "region": self.region,
            "monthly_cost": self.monthly_cost,
            "utilisation_pct": self.utilisation_pct,
            "cost_efficiency_score": self.cost_efficiency_score,
            "tags": self.tags,
        }


@dataclass
class OptimisationRecommendation:
    resource_id: str
    resource_name: str
    severity: OptimisationSeverity
    title: str
    description: str
    estimated_monthly_saving: float
    action: str

    def to_dict(self) -> dict:
        return {
            "resource_id": self.resource_id,
            "resource_name": self.resource_name,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "estimated_monthly_saving": self.estimated_monthly_saving,
            "action": self.action,
        }


@dataclass
class ArchitecturePattern:
    name: str
    description: str
    provider: CloudProvider
    use_cases: list[str]
    components: list[dict]
    estimated_monthly_cost: float
    reliability_tier: str  # e.g. "99.9%", "99.99%"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "provider": self.provider.value,
            "use_cases": self.use_cases,
            "components": self.components,
            "estimated_monthly_cost": self.estimated_monthly_cost,
            "reliability_tier": self.reliability_tier,
        }
