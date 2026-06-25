from archon.service_catalog.base import Service

SERVICES: list[Service] = [
    Service(
        name='Amazon S3',
        provider='aws',
        category='storage',
        description='Object storage with 11 9s durability',
        use_cases=['Data lakes', 'Backup and restore', 'Static website hosting', 'Content storage'],
        pricing_model='Per-GB storage, per-request, tiers (Standard, Infrequent Access, Glacier)',
        limitations=[
            'Eventual consistency for some operations',
            'No file locking without additional features',
        ],
        typical_latency='Milliseconds for standard tier',
        compliance=['SOC', 'ISO 27001', 'HIPAA', 'PCI DSS', 'FedRAMP'],
    ),
    Service(
        name='Google Cloud Storage',
        provider='gcp',
        category='storage',
        description='Unified object storage for live and archived data',
        use_cases=['Data lakes', 'Backup', 'Media storage', 'Analytics data'],
        pricing_model='Per-GB, per-operation, multi-class (Standard, Nearline, Coldline, Archive)',
        limitations=['Strong consistency but lower performance on some operations'],
        typical_latency='Milliseconds',
        compliance=['SOC', 'ISO 27001', 'HIPAA', 'PCI DSS'],
    ),
    Service(
        name='Azure Blob Storage',
        provider='azure',
        category='storage',
        description='Massively scalable object storage for unstructured data',
        use_cases=['Data lakes', 'Backup', 'Archive', 'Analytics'],
        pricing_model='Per-GB, per-operation, tiers (Hot, Cool, Cold, Archive)',
        limitations=['Account limits for some tiers'],
        typical_latency='Milliseconds',
        compliance=['SOC', 'ISO 27001', 'HIPAA', 'PCI DSS', 'FedRAMP'],
    ),
]
