from io import BytesIO

from jinja2 import Template


def get_template(html_string: str) ->Template:
    return Template(html_string)

def get_content(template: Template, payload) -> str:
    return template.render(payload)

def get_html_string(html_string, jinja_data_to_fill) -> str:
    return get_content( get_template(html_string), jinja_data_to_fill)

