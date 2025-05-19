"""
Routes and views for the bottle application.
"""

from bottle import route, view
from datetime import datetime

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/direct_lpp_theory')
@view('direct_lpp_theory')
def direct_lpp_theory():
    """Renders the direct_lpp_theory page."""
    return dict(
        title='The direct linear programming program',
        year=datetime.now().year
    )

@route('/direct_lpp_practice')
@view('direct_lpp_practice')
def direct_lpp_practice():
    """Renders the direct_lpp_practice page."""
    return dict(
        title='The direct linear programming program',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        year=datetime.now().year
    )

@route('/purpose_theory')
@view('purpose_theory')
def direct_lpp_practice():
    """Renders the purpose_theory page."""
    return dict(
        title='The assignment problem',
        year=datetime.now().year
    )

@route('/purpose_practice')
@view('purpose_practice')
def direct_lpp_practice():
    """Renders the purpose_theory page."""
    return dict(
        title='The assignment problem',
        year=datetime.now().year
    )


@route('/dual_lpp_theory')
@view('dual_lpp_theory')
def dual_theory():
    """Renders the dual_theory page."""
    return dict(
        title='The dual linear programming problem',
        year=datetime.now().year
    )

@route('/dual_lpp_practice')
@view('dual_lpp_practice')
def direct_lpp_practice():
    """Renders the direct_lpp_practice page."""
    return dict(
        title='The dual linear programming program',
        year=datetime.now().year
    )

@route('/transport_theory')
@view('transport_theory')
def dual_theory():
    """Renders the transport_theory page."""
    return dict(
        title='The transport programming problem',
        year=datetime.now().year
    )

@route('/transport_practice')
@view('transport_practice')
def dual_theory():
    """Renders the transport_practice page."""
    return dict(
        title='The transport programming problem',
        year=datetime.now().year
    )


from bottle import route, request, view, redirect
from hungarian_solver import solve_assignment  
import json

@route('/purpose_practice', method=['GET', 'POST'])
@view('purpose_practice')
def purpose_practice():
    result = None
    matrix = None
    error = None
    task_labels = []
    worker_labels = []

    if request.method == 'POST':
        try:
            size = int(request.forms.get('size'))
            
            
            task_labels = [request.forms.get(f'label-x{j}', f'Task {j+1}') for j in range(size)]
            
            worker_labels = [request.forms.get(f'label-y{i}', f'Worker {i+1}') for i in range(size)]

            matrix = []
            for i in range(size):
                row = []
                for j in range(size):
                    val = request.forms.get(f'matrix-{i}-{j}')
                    row.append(int(val))
                matrix.append(row)

           
            result = solve_assignment(matrix)

        except Exception as e:
            error = str(e)

    return dict(
        title="The assignment problem",
        year=datetime.now().year,
        result=result,
        matrix=matrix,
        error=error,
        task_labels=task_labels,
        worker_labels=worker_labels
    )
