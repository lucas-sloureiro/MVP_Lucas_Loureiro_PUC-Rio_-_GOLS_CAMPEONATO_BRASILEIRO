from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Gol, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
gol_tag = Tag(name="Gol", description="Adição, visualização e remoção de gols à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um gol cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/gol', tags=[gol_tag],
          responses={"200": GolViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_gol(form: GolSchema):
    """Adiciona um novo Gol à base de dados

    Retorna uma representação dos gols e comentários associados.
    """
    gol = Gol(
        jogador=form.jogador,
        time_jogador=form.time_jogador,
        time_adversario=form.time_adversario,
        min_gol=form.min_gol,
        rodada=form.rodada)
    logger.debug(f"Adicionando gol de jogador: '{gol.jogador}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando gol
        session.add(gol)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado gol de jogador: '{gol.jogador}'")
        return apresenta_gol(gol), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Gol de mesmo jogador já salvo na base :/"
        logger.warning(f"Erro ao adicionar gol '{gol.jogador}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar gol '{gol.jogador}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/gols', tags=[gol_tag],
         responses={"200": ListagemGolsSchema, "404": ErrorSchema})
def get_gols():
    """Faz a busca por todos os Gol cadastrados

    Retorna uma representação da listagem de gols.
    """
    logger.debug(f"Coletando gols ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    gols = session.query(Gol).all()

    if not gols:
        # se não há gols cadastrados
        return {"gols": []}, 200
    else:
        logger.debug(f"%d gols econtrados" % len(gols))
        # retorna a representação de gol
        print(gols)
        return apresenta_gols(gols), 200


@app.get('/gol', tags=[gol_tag],
         responses={"200": GolViewSchema, "404": ErrorSchema})
def get_gol(query: GolBuscaSchema):
    """Faz a busca por um Gol a partir do nome do jogador

    Retorna uma representação dos gols e comentários associados.
    """
    gol_jogador = query.jogador
    logger.debug(f"Coletando dados sobre gol #{gol_jogador}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    gol = session.query(Gol).filter(Gol.jogador == gol_jogador).first()

    if not gol:
        # se o gol não foi encontrado
        error_msg = "Gol não encontrado na base :/"
        logger.warning(f"Erro ao buscar gol '{gol_jogador}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Gol econtrado: '{gol.jogador}'")
        # retorna a representação de gol
        return apresenta_gol(gol), 200


@app.get('/gol_id', tags=[gol_tag],
         responses={"200": GolViewSchema, "404": ErrorSchema})
def get_gol_id(query: GolidBuscaSchema):
    """Faz a busca por um Gol a partir do id do gol

    Retorna uma representação dos gols e comentários associados.
    """
    gol_id = query.id
    logger.debug(f"Coletando dados sobre gol #{gol_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    gol = session.query(Gol).filter(Gol.id == gol_id).first()

    if not gol:
        # se o gol não foi encontrado
        error_msg = "Gol não encontrado na base :/"
        logger.warning(f"Erro ao buscar gol '{gol_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Gol econtrado: '{gol.id}'")
        # retorna a representação de gol
        return apresenta_gol(gol), 200
    

@app.delete('/gol', tags=[gol_tag],
            responses={"200": GolDelSchema, "404": ErrorSchema})
def del_gol(query: GolidBuscaSchema):
    """Deleta um Gol a partir do id do gol

    Retorna uma mensagem de confirmação da remoção.
    """
    gol_id = query.id
    print(gol_id)
    logger.debug(f"Deletando dados sobre gol #{gol_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Gol).filter(Gol.id == gol_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado gol #{gol_id}")
        return {"mesage": "Gol removido", "id": gol_id}
    else:
        # se o gol não foi encontrado
        error_msg = "Gol não encontrado na base :/"
        logger.warning(f"Erro ao deletar gol #'{gol_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": GolViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um gols cadastrado na base identificado pelo id

    Retorna uma representação dos gols e comentários associados.
    """
    gol_id  = form.gol_id
    logger.debug(f"Adicionando comentários ao gol #{gol_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo gol
    gol = session.query(Gol).filter(Gol.id == gol_id).first()

    if not gol:
        # se gol não encontrado
        error_msg = "Gol não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao gol '{gol_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao gol
    gol.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao gol #{gol_id}")

    # retorna a representação de gol
    return apresenta_gol(gol), 200
