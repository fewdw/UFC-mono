from flask import Blueprint

test_bp = Blueprint('test', __name__)


@test_bp.route('/')
def home():
    return 'test from test controller!',200


