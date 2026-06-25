from archon.service_catalog import ai_ml, analytics, compute, database, storage
from archon.service_catalog.base import Provider, Service, ServiceCategory

_ALL_SERVICES: list[Service] = []
for module in [compute, storage, database, analytics, ai_ml]:
    _ALL_SERVICES.extend(module.SERVICES)


def search_services(query: str) -> list[Service]:
    q = query.lower()
    results: list[Service] = []
    for service in _ALL_SERVICES:
        if (
            q in service.name.lower()
            or q in service.description.lower()
            or any(q in uc.lower() for uc in service.use_cases)
        ):
            results.append(service)
    return results


def get_by_provider(provider: Provider) -> list[Service]:
    return [s for s in _ALL_SERVICES if s.provider == provider]


def get_by_category(category: ServiceCategory) -> list[Service]:
    return [s for s in _ALL_SERVICES if s.category == category]


__all__ = [
    'Service',
    'ServiceCategory',
    'Provider',
    'search_services',
    'get_by_provider',
    'get_by_category',
]
