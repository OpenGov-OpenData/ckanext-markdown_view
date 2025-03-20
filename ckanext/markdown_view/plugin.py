import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
import logging

import requests
import mistune


logger = logging.getLogger(__name__)


class MarkdownViewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config):
        tk.add_template_directory(config, 'templates')
        tk.add_public_directory(config, 'public')

    def info(self):
        return {
            'name': tk._('Markdown'),
            'icon': 'file-text-o',
            'filterable': False,
            'iframed': False,
        }

    def can_view(self, data_dict):
        return data_dict['resource'].get('format', '').lower() in ('text/markdown', 'markdown', 'md')

    def setup_template_variables(self, context, data_dict):
        resource = data_dict['resource']
        resource_view = data_dict['resource_view']

        resp = requests.get(resource.get('url'), stream=False, timeout=60)
        resp.raise_for_status()

        return {'resource': resource,
                'resource_view': resource_view,
                'content': resp.text,
                }

    def view_template(self, context, data_dict):
        return 'markdown_view.html'

    def form_template(self, context, data_dict):
        return 'markdown_form.html'

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'markdown_to_html': markdown_to_html,
        }


def markdown_to_html(content):
    html = mistune.html(content)
    return tk.literal(html)
