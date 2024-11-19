from flask import render_template
from app.modules.email import email_bp


@email_bp.route('/email', methods=['GET'])
def index():
    return render_template('email/index.html')
