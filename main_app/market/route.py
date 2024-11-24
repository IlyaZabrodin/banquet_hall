from flask import Blueprint


blueprint_market = Blueprint('bp_market', __name__)


@blueprint_market.route('/', methods=['GET', 'POST'])
def market() -> str:
    return 'Make your order'
