from flask import Blueprint
from access import login_required


blueprint_order_make = Blueprint('bp_order_make', __name__)


@blueprint_order_make.route('/', methods=['GET', 'POST'])
@login_required(['client'])
def order_make() -> str:
    return 'Make your order'
