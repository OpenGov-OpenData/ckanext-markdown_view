# encoding: utf-8
import pytest
import responses
from ckan.tests import factories

import ckan.plugins as p
from ckan.plugins import toolkit as tk


def _add_responses_solr_passthru():
    responses.add_passthru(tk.config.get('solr_url'))


@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins', 'with_request_context')
@pytest.mark.ckan_config('ckan.plugins', 'datastore markdown_view')
def test_view_create():
    org = factories.Organization()
    dataset = factories.Dataset(owner_org=org['id'],)
    sysadmin = factories.Sysadmin()
    resource = factories.Resource(
        package_id=dataset['id'],
        url='http://some.website.html',)

    p.toolkit.get_action('datastore_create')(
       {'user': sysadmin.get('name')},
       {'resource_id': resource.get('id'), 'force': True}
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
