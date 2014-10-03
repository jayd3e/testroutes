from pyramid.security import (
    Allow,
    Authenticated
)
from pyramid.config import Configurator
from pyramid.security import remember
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.view import view_config, forbidden_view_config
from pyramid.response import Response


@forbidden_view_config(route_name='api_v1', renderer='string')
def api(request):
    return 'forbidden'


@view_config(route_name='api_posts', renderer='string', permission='authenticated')
def posts(request):
    return 'protected'


@view_config(route_name='api_login', renderer='string')
def login(request):
    headers = remember(request, 1)
    return Response('logged in', headers=headers)


class Site(object):
    __acl__ = [(Allow, Authenticated, 'authenticated')]

    def __init__(self, request):
        pass


def groupfinder(userid, request):
    return ['authenticated']


def main(global_config, **settings):
    authentication_policy = AuthTktAuthenticationPolicy('seekrit', callback=groupfinder)
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy)
    config.set_root_factory(Site)
    config.add_route('api_posts', '/api/1/posts')
    config.add_route('api_login', '/api/1/login')
    config.add_route('api_v1', '/api/1/*path')
    config.scan()
    return config.make_wsgi_app()
