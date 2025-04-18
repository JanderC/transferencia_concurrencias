from flask import Flask, render_template
from controllers.account_controller import account_bp
from controllers.transaction_controller import transaction_bp
from config.database import init_db, init_app  # Añade init_app aquí

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_for_demo'

# Registrar la función de cierre de conexión
init_app(app)  # Añade esta línea

# Registrar blueprints
app.register_blueprint(account_bp)
app.register_blueprint(transaction_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)