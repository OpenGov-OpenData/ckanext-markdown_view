# encoding: utf-8
import pytest
from ckan.tests import factories

import ckan.plugins as p


@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins', 'with_request_context')
@pytest.mark.ckan_config('ckan.plugins', 'markdown_view')
def test_view_create_for_md_resource():
    org = factories.Organization()
    dataset = factories.Dataset(owner_org=org['id'],)
    sysadmin = factories.Sysadmin()
    resource = factories.Resource(
        package_id=dataset['id'],
        url='http://some.website.md',
        format='md'
    )

    resource_view = factories.ResourceView(
        resource_id=resource['id'],
        view_type='Markdown'
    )

    response = p.toolkit.get_action('resource_view_show')(
        {'user': sysadmin.get('name')},
        {'id': resource_view.get('id')}
    )

    assert response.get('view_type') == 'Markdown'


@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins', 'with_request_context')
@pytest.mark.ckan_config('ckan.plugins', 'markdown_view')
def test_view_create_for_csv_resource():
    org = factories.Organization()
    dataset = factories.Dataset(owner_org=org['id'],)
    sysadmin = factories.Sysadmin()
    resource = factories.Resource(
        package_id=dataset['id'],
        url='http://some.website.csv',
        format='csv'
    )

    resource_view = factories.ResourceView(
        resource_id=resource['id'],
        view_type='Markdown'
    )

    response = p.toolkit.get_action('resource_view_show')(
        {'user': sysadmin.get('name')},
        {'id': resource_view.get('id')}
    )

    assert response.get('view_type') == 'Markdown'
