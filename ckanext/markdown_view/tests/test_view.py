# encoding: utf-8
import pytest
from ckan.tests import factories

import ckan.plugins as p
from ckan.logic import ValidationError


@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins', 'with_request_context')
@pytest.mark.ckan_config('ckan.plugins', 'markdown_view')
def test_view_create_for_md_resource(app):
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
    env = {"REMOTE_USER": sysadmin['name'].encode('ascii')}
    resp = app.get(f"/dataset/{dataset['id']}/resource/{resource['id']}?view_id={resource_view['id']}",
                   extra_environ=env)

    assert resp.status_code == 200
    assert f'<div id="md_view_html" data-resource-url="{resource["url"]}"></div>' in resp.body


@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins', 'with_request_context')
@pytest.mark.ckan_config('ckan.plugins', 'markdown_view')
def test_view_create_for_csv_resource(app):
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

    env = {"REMOTE_USER": sysadmin['name'].encode('ascii')}
    resp = app.get(f"/dataset/{dataset['id']}/resource/{resource['id']}?view_id={resource_view['id']}", extra_environ=env)

    assert resp.status_code == 200
    assert 'This Resource cannot be processed by markdown view.' in resp.body


@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins', 'with_request_context')
@pytest.mark.ckan_config('ckan.plugins', 'markdown_view')
def test_view_create_for_csv_resource_with_correct_page_url(app):
    org = factories.Organization()
    dataset = factories.Dataset(owner_org=org['id'],)
    sysadmin = factories.Sysadmin()
    resource = factories.Resource(
        package_id=dataset['id'],
        url='http://some.website.csv',
        format='csv'
    )
    page_url = 'http://some.website.md'

    resource_view = factories.ResourceView(
        resource_id=resource['id'],
        view_type='Markdown',
        page_url=page_url,
    )

    response = p.toolkit.get_action('resource_view_show')(
        {'user': sysadmin.get('name')},
        {'id': resource_view.get('id')}
    )

    assert response.get('view_type') == 'Markdown'

    env = {"REMOTE_USER": sysadmin['name'].encode('ascii')}
    resp = app.get(f"/dataset/{dataset['id']}/resource/{resource['id']}?view_id={resource_view['id']}",
                   extra_environ=env)

    assert resp.status_code == 200
    assert f'<div id="md_view_html" data-resource-url="{page_url}"></div>' in resp.body


@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins', 'with_request_context')
@pytest.mark.ckan_config('ckan.plugins', 'markdown_view')
def test_view_create_for_csv_resource_with_incorrect_page_url(app):
    org = factories.Organization()
    dataset = factories.Dataset(owner_org=org['id'], )
    resource = factories.Resource(
        package_id=dataset['id'],
        url='http://some.website.csv',
        format='csv'
    )
    page_url = 'http://some.website.html'

    with pytest.raises(ValidationError):
        factories.ResourceView(
            resource_id=resource['id'],
            view_type='Markdown',
            page_url=page_url,
        )
