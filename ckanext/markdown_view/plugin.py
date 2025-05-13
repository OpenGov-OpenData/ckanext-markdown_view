import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
import logging


logger = logging.getLogger(__name__)
ignore_empty = tk.get_validator('ignore_empty')
unicode_safe = tk.get_validator('unicode_safe')
url_validator = tk.get_validator('url_validator')


class MarkdownViewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IResourceView, inherit=True)

    # IConfigurer
    def update_config(self, config):
        tk.add_template_directory(config, 'templates')
        tk.add_resource('assets', 'md_view_assets')

    def info(self):
        return {
            'name': tk._('Markdown'),
            'icon': 'file-text-o',
            'filterable': False,
            'iframed': False,
            'always_available': True,
            'schema': {
                'page_url': [unicode_safe, url_validator, url_to_md_file]
            },
        }

    def can_view(self, data_dict):
        return data_dict.get('resource', {}).get('format', '').lower() in ('text/markdown', 'markdown', 'md')

    def setup_template_variables(self, context, data_dict):
        resource = data_dict['resource']
        resource_view = data_dict['resource_view']

        return {'resource': resource,
                'resource_view': resource_view,
                'resource_url': resource.get('url'),
                }

    def view_template(self, context, data_dict):
        return 'markdown_view.html'

    def form_template(self, context, data_dict):
        return 'markdown_form.html'


def url_to_md_file(value):
    if not value:
        return None
    elif value.endswith('.md'):
        return value
    else:
        raise tk.Invalid(tk._('Url should point to a markdown file (ends with .md)'))
