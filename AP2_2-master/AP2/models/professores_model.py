from config import db

class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(100))
    observacoes = db.Column(db.String(200))

    # Relacionamento com as turmas (uma lista de turmas para cada professor)
    turmas = db.relationship('Turma', back_populates='professor')

    def __init__(self, nome, idade, materia, observacoes):
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'materia': self.materia,
            'observacoes': self.observacoes
            }

class ProfessorNaoEncontrado(Exception):
    pass

def listar_professores():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]

def professor_por_id(id_professor):
    prof = Professor.query.get(id_professor)
    if not prof:
        raise ProfessorNaoEncontrado
    return prof.to_dict()

def adicionar_professor(professor_data):
    novo_profesor = Professor(
        nome=professor_data['nome'],
        idade=professor_data['idade'],
        materia=professor_data['materia'],
        observacoes=professor_data['observacoes']
        )
    db.session.add(novo_profesor)
    db.session.commit()

def atualizar_professor(id_professor, novos_dados):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    professor.nome = novos_dados.get('nome', professor.nome)
    professor.idade = novos_dados.get('idade', professor.idade)
    professor.materia = novos_dados.get('materia', professor.materia)
    professor.observacoes = novos_dados.get('observacoes', professor.observacoes)
    db.session.commit()
    return professor

def excluir_professor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    db.session.delete(professor)
    db.session.commit()