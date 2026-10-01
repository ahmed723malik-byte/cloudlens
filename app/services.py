"""
CloudService: Simulates multi-cloud resource discovery and cost analysis.

In production, this would integrate with:
- AWS: boto3 (Cost Explorer, EC2, S3, RDS APIs)
- GCP: google-cloud-billing, google-cloud-asset APIs
- Azure: azure-mgmt-costmanagement, azure-mgmt-resource SDKs
"""

from .models import (
    CloudResource, CloudProvider, ResourceType,
    OptimisationRecommendation, OptimisationSeverity,
    ArchitecturePattern,
)


MOCK_RESOURCES: list[CloudResource] = [
    # AWS Resources
    CloudResource("prod-api-ec2-3xl", CloudProvider.AWS, ResourceType.COMPUTE,
                  "eu-west-1", 420.00, 12.0, {"env": "prod", "team": "platform"}),
    CloudResource("prod-rds-postgres", CloudProvider.AWS, ResourceType.DATABASE,
                  "eu-west-1", 380.00, 68.0, {"env": "prod", "team": "data"}),
    CloudResource("prod-s3-assets", CloudProvider.AWS, ResourceType.STORAGE,
                  "eu-west-1", 47.00, 91.0, {"env": "prod", "team": "frontend"}),
    CloudResource("staging-ec2-xlarge", CloudProvider.AWS, ResourceType.COMPUTE,
                  "eu-west-1", 180.00, 8.0, {"env": "staging", "team": "platform"}),
    CloudResource("prod-lambda-ingest", CloudProvider.AWS, ResourceType.SERVERLESS,
                  "eu-west-1", 22.50, 77.0, {"env": "prod", "team": "data"}),
    CloudResource("prod-eks-cluster", CloudProvider.AWS, ResourceType.CONTAINER,
                  "eu-west-1", 290.00, 55.0, {"env": "prod", "team": "platform"}),
    CloudResource("dev-rds-mysql", CloudProvider.AWS, ResourceType.DATABASE,
                  "eu-west-1", 95.00, 4.0, {"env": "dev", "team": "backend"}),
    CloudResource("prod-cloudwatch", CloudProvider.AWS, ResourceType.MONITORING,
                  "eu-west-1", 38.00, 100.0, {"env": "prod", "team": "ops"}),

    # GCP Resources
    CloudResource("prod-gke-autopilot", CloudProvider.GCP, ResourceType.CONTAINER,
                  "europe-west2", 340.00, 72.0, {"env": "prod", "team": "ml"}),
    CloudResource("prod-bigquery-dw", CloudProvider.GCP, ResourceType.DATABASE,
                  "europe-west2", 210.00, 83.0, {"env": "prod", "team": "data"}),
    CloudResource("prod-gcs-datalake", CloudProvider.GCP, ResourceType.STORAGE,
                  "europe-west2", 89.00, 95.0, {"env": "prod", "team": "data"}),
    CloudResource("prod-cloud-run", CloudProvider.GCP, ResourceType.SERVERLESS,
                  "europe-west2", 31.00, 44.0, {"env": "prod", "team": "backend"}),
    CloudResource("staging-compute-engine", CloudProvider.GCP, ResourceType.COMPUTE,
                  "europe-west2", 120.00, 6.0, {"env": "staging", "team": "ml"}),

    # Azure Resources
    CloudResource("prod-aks-cluster", CloudProvider.AZURE, ResourceType.CONTAINER,
                  "uksouth", 310.00, 61.0, {"env": "prod", "team": "platform"}),
    CloudResource("prod-cosmos-db", CloudProvider.AZURE, ResourceType.DATABASE,
                  "uksouth", 275.00, 52.0, {"env": "prod", "team": "backend"}),
    CloudResource("prod-blob-storage", CloudProvider.AZURE, ResourceType.STORAGE,
                  "uksouth", 54.00, 88.0, {"env": "prod", "team": "frontend"}),
    CloudResource("dev-vm-standard", CloudProvider.AZURE, ResourceType.COMPUTE,
                  "uksouth", 75.00, 3.0, {"env": "dev", "team": "dev"}),
    CloudResource("prod-functions", CloudProvider.AZURE, ResourceType.SERVERLESS,
                  "uksouth", 18.00, 35.0, {"env": "prod", "team": "backend"}),
]


ARCHITECTURE_PATTERNS: list[ArchitecturePattern] = [
    ArchitecturePattern(
        name="Serverless Event-Driven API",
        description="Fully managed, pay-per-use REST API using AWS Lambda, API Gateway, and DynamoDB. Zero idle cost.",
        provider=CloudProvider.AWS,
        use_cases=["REST APIs", "Webhook processors", "Mobile backends"],
        components=[
            {"name": "API Gateway", "type": "Network", "icon": "🔀"},
            {"name": "Lambda", "type": "Serverless", "icon": "⚡"},
            {"name": "DynamoDB", "type": "Database", "icon": "🗄️"},
            {"name": "CloudWatch", "type": "Monitoring", "icon": "📊"},
        ],
        estimated_monthly_cost=45.0,
        reliability_tier="99.95%",
    ),
    ArchitecturePattern(
        name="Containerised Microservices",
        description="Kubernetes-based microservices on EKS with auto-scaling, service mesh, and GitOps deployment.",
        provider=CloudProvider.AWS,
        use_cases=["Complex business logic", "Team-scaled apps", "High-traffic services"],
        components=[
            {"name": "Route 53 / ALB", "type": "Network", "icon": "🌐"},
            {"name": "EKS Cluster", "type": "Container", "icon": "☸️"},
            {"name": "ECR Registry", "type": "Storage", "icon": "📦"},
            {"name": "RDS Aurora", "type": "Database", "icon": "🗄️"},
            {"name": "ElastiCache", "type": "Database", "icon": "⚡"},
        ],
        estimated_monthly_cost=680.0,
        reliability_tier="99.99%",
    ),
    ArchitecturePattern(
        name="Data Lake & Analytics Pipeline",
        description="Scalable GCP data pipeline from ingestion to BI dashboards using Pub/Sub, Dataflow, BigQuery.",
        provider=CloudProvider.GCP,
        use_cases=["Real-time analytics", "ML feature pipelines", "Business intelligence"],
        components=[
            {"name": "Pub/Sub", "type": "Network", "icon": "📨"},
            {"name": "Dataflow", "type": "Compute", "icon": "🔄"},
            {"name": "GCS Data Lake", "type": "Storage", "icon": "🪣"},
            {"name": "BigQuery", "type": "Database", "icon": "🔍"},
            {"name": "Looker Studio", "type": "Monitoring", "icon": "📈"},
        ],
        estimated_monthly_cost=320.0,
        reliability_tier="99.9%",
    ),
    ArchitecturePattern(
        name="Multi-Region Active-Active",
        description="Azure high-availability architecture spanning UK South and West Europe with Traffic Manager.",
        provider=CloudProvider.AZURE,
        use_cases=["Mission-critical apps", "GDPR-compliant SaaS", "Global user bases"],
        components=[
            {"name": "Traffic Manager", "type": "Network", "icon": "🔀"},
            {"name": "AKS (2 regions)", "type": "Container", "icon": "☸️"},
            {"name": "Cosmos DB Global", "type": "Database", "icon": "🌍"},
            {"name": "Azure CDN", "type": "Network", "icon": "⚡"},
            {"name": "Azure Monitor", "type": "Monitoring", "icon": "📊"},
        ],
        estimated_monthly_cost=1240.0,
        reliability_tier="99.995%",
    ),
]


class CloudService:
    def get_all_resources(self) -> list[dict]:
        return [r.to_dict() for r in MOCK_RESOURCES]

    def get_cost_summary(self) -> dict:
        total = sum(r.monthly_cost for r in MOCK_RESOURCES)
        by_provider: dict[str, float] = {}
        by_type: dict[str, float] = {}
        by_env: dict[str, float] = {}

        for r in MOCK_RESOURCES:
            by_provider[r.provider.value] = round(
                by_provider.get(r.provider.value, 0) + r.monthly_cost, 2)
            by_type[r.resource_type.value] = round(
                by_type.get(r.resource_type.value, 0) + r.monthly_cost, 2)
            env = r.tags.get("env", "unknown")
            by_env[env] = round(by_env.get(env, 0) + r.monthly_cost, 2)

        return {
            "total_monthly": round(total, 2),
            "projected_annual": round(total * 12, 2),
            "by_provider": by_provider,
            "by_type": by_type,
            "by_environment": by_env,
            "resource_count": len(MOCK_RESOURCES),
        }

    def get_optimisation_recommendations(self) -> list[dict]:
        recs: list[OptimisationRecommendation] = []

        for r in MOCK_RESOURCES:
            if r.utilisation_pct < 10 and r.monthly_cost > 50:
                saving = round(r.monthly_cost * 0.65, 2)
                recs.append(OptimisationRecommendation(
                    resource_id=r.id,
                    resource_name=r.name,
                    severity=OptimisationSeverity.HIGH,
                    title=f"Severely underutilised {r.resource_type.value.lower()}",
                    description=(
                        f"{r.name} is running at only {r.utilisation_pct}% utilisation "
                        f"but costing £{r.monthly_cost}/mo. Consider downsizing or "
                        f"scheduling shutdown for non-production hours."
                    ),
                    estimated_monthly_saving=saving,
                    action="Downsize or schedule stop/start",
                ))
            elif r.utilisation_pct < 20 and r.monthly_cost > 30:
                saving = round(r.monthly_cost * 0.35, 2)
                recs.append(OptimisationRecommendation(
                    resource_id=r.id,
                    resource_name=r.name,
                    severity=OptimisationSeverity.MEDIUM,
                    title=f"Low utilisation on {r.resource_type.value.lower()}",
                    description=(
                        f"{r.name} averages {r.utilisation_pct}% utilisation. "
                        f"Right-sizing to a smaller instance type could save ~£{saving}/mo."
                    ),
                    estimated_monthly_saving=saving,
                    action="Right-size instance type",
                ))

        total_saving = round(sum(rec.estimated_monthly_saving for rec in recs), 2)
        return {
            "recommendations": [rec.to_dict() for rec in recs],
            "total_potential_saving": total_saving,
            "count": len(recs),
        }

    def get_architecture_patterns(self) -> list[dict]:
        return [p.to_dict() for p in ARCHITECTURE_PATTERNS]
