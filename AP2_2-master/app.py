from flask import Flask, jsonify, request, abort
from config import app, db
from config import User

professores = []
turmas = []
alunos = []

@app.route('/professores', methods=['POST'])
def add_professor():
    data = request.json
    if 'nome' not in data or 'idade' not in data or 'materia' not in data:
        return jsonify({'error': 'Campos obrigatórios: nome, idade, materia.'}), 400

    novo_professor = {
        'id': len(professores) + 1,
        'nome': data['nome'],
        'idade': data['idade'],
        'materia': data['materia'],
        'observacoes': data.get('observacoes', '')
    }
    professores.append(novo_professor)
    return jsonify({'id': novo_professor['id']}), 201

@app.route('/turmas', methods=['POST'])
def add_turma():
    data = request.json
    if 'descricao' not in data or 'professor_id' not in data:
        return jsonify({'error': 'Campos obrigatórios: descricao, professor_id.'}), 400

    nova_turma = {
        'id': len(turmas) + 1,
        'descricao': data['descricao'],
        'professor_id': data['professor_id'],
        'ativo': data.get('ativo', True)
    }
    turmas.append(nova_turma)
    return jsonify({'id': nova_turma['id']}), 201

@app.route('/alunos', methods=['POST'])
def add_aluno():
    data = request.json
    required_fields = ['nome', 'idade', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo obrigatório: {field}.'}), 400

    media_final = (data['nota_primeiro_semestre'] + data['nota_segundo_semestre']) / 2
    novo_aluno = {
        'id': len(alunos) + 1,
        'nome': data['nome'],
        'idade': data['idade'],
        'turma_id': data['turma_id'],
        'data_nascimento': data['data_nascimento'],
        'nota_primeiro_semestre': data['nota_primeiro_semestre'],
        'nota_segundo_semestre': data['nota_segundo_semestre'],
        'media_final': media_final
    }
    alunos.append(novo_aluno)
    return jsonify({'id': novo_aluno['id']}), 201

@app.route('/professores', methods=['GET'])
def get_professores():
    return jsonify(professores)

@app.route('/turmas', methods=['GET'])
def get_turmas():
    return jsonify(turmas)

@app.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(alunos)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Campos obrigatórios: username, password.'}), 400

    username = data['username']
    password = data['password']
    new_user = User(username=username, password=password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'id': new_user.id, 'username': new_user.username}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(user_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True, port=8000)
