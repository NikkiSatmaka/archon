from archon.service_catalog import get_by_category, get_by_provider, search_services


def test_search_by_name():
    results = search_services('Lambda')
    assert len(results) >= 1
    assert any('Lambda' in s.name for s in results)


def test_search_by_description():
    results = search_services('serverless')
    assert len(results) >= 1


def test_search_empty_query():
    results = search_services('xyznonexistent')
    assert len(results) == 0


def test_get_by_provider_aws():
    results = get_by_provider('aws')
    assert len(results) >= 1
    assert all(s.provider == 'aws' for s in results)


def test_get_by_provider_gcp():
    results = get_by_provider('gcp')
    assert len(results) >= 1


def test_get_by_category_compute():
    results = get_by_category('compute')
    assert len(results) >= 1
    assert all(s.category == 'compute' for s in results)


def test_get_by_category_storage():
    results = get_by_category('storage')
    assert len(results) >= 1
