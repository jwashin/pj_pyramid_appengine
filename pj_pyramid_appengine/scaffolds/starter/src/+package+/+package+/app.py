from pyramid.config import Configurator
from resources import Root
import views
import pyramid_jinja2
import os

__here__ = os.path.dirname(os.path.abspath(__file__))


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_renderer('.jinja2', pyramid_jinja2.Jinja2Renderer)
    config.add_view(views.my_view,
                    context=Root,
                    renderer='mytemplate.jinja2')
    config.add_static_view(name='static', path=os.path.join(__here__, 'static'))
    config.include('pyramid_rpc.jsonrpc')

    config.add_jsonrpc_endpoint('echoservice', '/echo')
    config.scan()
    return config.make_wsgi_app()
