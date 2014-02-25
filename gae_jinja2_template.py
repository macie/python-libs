"""
Jinja2 template decorator for Google App Engine.

Maciej Żok, 2013 MIT License

"""
from functools import wraps
import logging


class template(object):
    """
    Decorator for rendering templates with jinja2.

    Decorated function should return dictionary (or nothing).

    Args:
        name (str): template name

    Returns:
        Rendered template.

    Example:
        @template('index.html')
        def get(self):
            d = {'id': 15,
                 'name': 'John Smith'}
            return d

    """
    def __init__(self, name):
        self.template_name = name

    def __call__(self, request):
        @wraps(request)
        def render_template(inst, *args, **kwargs):
            """
            Set response.

            """
            inst.response.headers['X-Content-Type-Options'] = 'nosniff'
            inst.response.headers['X-Frame-Options'] = 'deny'
            inst.response.headers['X-XSS-Protection'] = '1; mode=block'
            context = request(inst, *args, **kwargs)
            if context is None:
                context = {}
            elif not isinstance(context, dict):
                logging.error('Invalid template arguments: <%r>', context)
                context = {}
            inst.response.write(
                inst.jinja2.render_template(self.template_name, **context))
        return render_template
