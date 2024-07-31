from flask import Flask, request, jsonify
import random
from flask_mail import Mail, Message

app = Flask(__name__)

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'daniucs.teste1@gmail.com'
app.config['MAIL_PASSWORD'] = 'ciarkhyrkbqlwxyv'  # Use a senha de aplicativo gerada

mail = Mail(app)

def generate_verification_code():
    return str(random.randint(1000, 9999))

def send_email(recipient, code):
    with app.app_context():
        msg = Message('Your Verification Code',
                      sender='daniucs.teste1@gmail.com',
                      recipients=[recipient])
        msg.body = f'Your verification code is DH-{code}'
        mail.send(msg)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    code = generate_verification_code()
    try:
        send_email(email, code)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'verification_code': code}), 200

def test_send_email():
    test_email = 'daniucs@gmail.com'
    test_code = generate_verification_code()
    try:
        send_email(test_email, test_code)
        print(f'Email sent successfully to {test_email} with code {test_code}')
    except Exception as e:
        print(f'Failed to send email: {e}')

if __name__ == '__main__':
    with app.app_context():
        #test_send_email()  # Testa o envio de email localmente
        app.run(port=5001)


