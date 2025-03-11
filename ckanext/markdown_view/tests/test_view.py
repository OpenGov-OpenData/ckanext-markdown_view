# encoding: utf-8
import pytest
import responses
from ckan.tests import factories

import ckan.plugins as p
from ckan.plugins import toolkit as tk


def _add_responses_solr_passthru():
    responses.add_passthru(tk.config.get('solr_url'))


def pytest_generate_tests(metafunc):
    # called once per each test function
    if metafunc.cls is not TestMDView:
        return
    funcarglist = metafunc.cls.params[metafunc.function.__name__]

    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )


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


@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins', 'with_request_context')
@pytest.mark.ckan_config('ckan.plugins', 'datastore markdown_view')
class TestMDView:
    params = {
        'test_rendering': [
            dict(file_content='[Test link in new tab](http://www.example.org/){: target=”_blank”}',
                 html_entries=['<a href="http://www.example.org/" target="”_blank”">Test link in new tab</a>']),
            dict(file_content='[Test link](http://www.example.org/)',
                 html_entries=['<a href="http://www.example.org/">Test link</a>']),
            dict(file_content='| Col1 | Col2 |\n'
                              '|------|------|\n'
                              '| val1 | val2 |\n',
                 html_entries=['<table>',
                               '<thead>',
                               '<tr>',
                               '<th>Col1</th>',
                               '<th>Col2</th>',
                               '</tr>',
                               '</thead>',
                               '<tbody>',
                               '<tr>',
                               '<td>val1</td>',
                               '<td>val2</td>',
                               '</tr>',
                               '</tbody>',
                               '</table>',
                               ]
                 ),

        ]
    }

    @responses.activate
    def test_rendering(self, file_content, html_entries, app):
        _add_responses_solr_passthru()
        file = file_content
        responses.get('http://link.to.some.data/', body=file)

        user = factories.Sysadmin()
        org = factories.Organization()
        env = {"REMOTE_USER": user['name'].encode('ascii')}
        dataset = factories.Dataset(owner_org=org['id'])
        res = factories.Resource(user=user, format='abc', package_id=dataset['id'])

        resource_view = factories.ResourceView(
            resource_id=res['id'],
            view_type='Markdown'
        )

        url = tk.url_for('resource.view',
                         id=dataset["id"],
                         resource_id=res.get("id"),
                         view_id=resource_view.get('id'),
                         qualified=False
                         )

        get_response = app.get(url, extra_environ=env)
        for entry in html_entries:
            assert entry in get_response
