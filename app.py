from flask import Flask, render_template, request, jsonify
import prediction

app = Flask(__name__)

# Defina uma rota do aplicativo que renderiza a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota que aceita solicitações POST para prever sentimentos
@app.route('/predict', methods=['POST'])
def predict():
    review = request.json.get('customer_review')

    if not review:
        response = {'status': 'error', 'message': 'Avaliação em Branco'}
    else:
        # Chame o método predict do módulo prediction.py
        sentiment, path = prediction.predict(review)
        response = {'status': 'success', 'message': 'Got it', 'sentiment': sentiment, 'path': path}

    return jsonify(response)

# Rota para salvar a avaliação
@app.route('/save', methods=['POST'])
def save():
    # Extraindo dados, nome do produto, avaliação e sentimento associados dos dados JSON
    date = request.json.get('date')
    product = request.json.get('product')
    review = request.json.get('review')
    sentiment = request.json.get('sentiment')

    # Criando uma variável final separada por vírgulas
    data_entry = f"{date},{product},{review},{sentiment}\n"

    # Abrir o arquivo no modo 'append'
    with open('reviews.csv', 'a') as file:
        # Registrar os dados no arquivo
        file.write(data_entry)

    # Retornar uma mensagem de sucesso
    return jsonify({'status': 'success', 'message': 'Dados Registrados'})

if __name__ == "__main__":
    app.run(debug=True)
