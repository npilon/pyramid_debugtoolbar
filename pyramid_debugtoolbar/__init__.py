from pyramid.settings import asbool
from pyramid.encode import url_quote
from pyramid_debugtoolbar.utils import as_globals_list

default_panel_names = (
    'pyramid_debugtoolbar.panels.versions.VersionDebugPanel',
    'pyramid_debugtoolbar.panels.settings.SettingsDebugPanel',
    'pyramid_debugtoolbar.panels.timer.TimerDebugPanel',
    'pyramid_debugtoolbar.panels.headers.HeaderDebugPanel',
    'pyramid_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'pyramid_debugtoolbar.panels.renderings.RenderingsDebugPanel',
    'pyramid_debugtoolbar.panels.logger.LoggingPanel',
    'pyramid_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    'pyramid_debugtoolbar.panels.routes.RoutesDebugPanel',
    )

STATIC_PATH = 'pyramid_debugtoolbar:static/'

default_settings = (
    ('enabled', asbool, 'true'),
    ('intercept_exc', asbool, 'true'),
    ('intercept_redirects', asbool, 'true'),
    ('panels', as_globals_list, default_panel_names),
    )

def parse_settings(settings, prefix='debugtoolbar.'):
    parsed = {}
    def populate(name, convert=None, default=None):
        if convert is None:
            convert = lambda x: x
        name = '%s%s' % (prefix, name)
        value = convert(settings.get(name, default))
        parsed[name] = value
    for name, convert, default in default_settings:
        populate(name, convert, default)
    return parsed

def includeme(config):
    settings = parse_settings(config.registry.settings)
    config.registry.settings.update(settings)
    config.include('pyramid_jinja2')
    j2_env = config.get_jinja2_environment()
    j2_env.filters['urlencode'] = url_quote
    config.add_static_view('_debug_toolbar/static', STATIC_PATH)
    config.add_request_handler(
        'pyramid_debugtoolbar.toolbar.toolbar_handler_factory',
        'debug_toolbar')
    config.add_subscriber(
        'pyramid_debugtoolbar.toolbar.beforerender_subscriber',
        'pyramid.events.BeforeRender')
    config.add_route('debugtoolbar.root', '/_debug_toolbar', static=True)
    config.add_route('debugtoolbar.source', '/_debug_toolbar/source')
    config.add_route('debugtoolbar.execute', '/_debug_toolbar/execute')
    config.add_route('debugtoolbar.console', '/_debug_toolbar/console')
    config.scan('pyramid_debugtoolbar.views')
        
