from pyramid.config import Configurator


def configure_api_v1(config):
    api_v = '/api/v1'
    config.add_route('api_v1', api_v)
    config.add_route('api_v1_getdatasets', api_v + '/getdatasets')
    config.add_route('api_v1_getmodels', api_v + '/getmodels')
    config.add_route('api_v1_getarchs', api_v + '/getarchs')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    configure_api_v1(config)

    config.scan()
    return config.make_wsgi_app()
