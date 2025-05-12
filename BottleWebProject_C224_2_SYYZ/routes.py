"""
Routes and views for the bottle application.
"""

from bottle import route, view
from datetime import datetime

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )
