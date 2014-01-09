from bottle import get, view, app, request, redirect, route, abort, post


@get('/')
@view('index')
def index():
    return {'title': 'Tribe Server'}
