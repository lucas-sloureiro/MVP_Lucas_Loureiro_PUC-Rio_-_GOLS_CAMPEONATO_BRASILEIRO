from pydantic import BaseModel
from typing import Optional, List
from model.gol import Gol

from schemas import ComentarioSchema


class GolSchema(BaseModel):
    """ Define como um novo gol a ser inserido deve ser representado
    """
    jogador: str = "Gabriel Barbosa"
    time_jogador: str = "Flamengo"
    time_adversario: str = "River Plate"
    min_gol: int = 92
    rodada: int = 38

class GolBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do jogador.
    """
    jogador: str = "Gabriel Barbosa"
    
class GolidBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do gol.
    """
    id: int = 1

class ListagemGolsSchema(BaseModel):
    """ Define como uma listagem de gols será retornada.
    """
    gols:List[GolSchema]


def apresenta_gols(gols: List[Gol]):
    """ Retorna uma representação do gol seguindo o schema definido em
        GolViewSchema.
    """
    result = []
    for gol in gols:
        result.append({
            "jogador": gol.jogador,
            "time_jogador": gol.time_jogador,
            "time_adversario": gol.time_adversario,
            "min_gol": gol.min_gol,
            "rodada": gol.rodada,
            "id": gol.id,
        })

    return {"gols": result}


class GolViewSchema(BaseModel):
    """ Define como um gol será retornado: gol + comentários.
    """
    id: int = 1
    jogador: str = "Gabriel Barbosa"
    time_jogador: str = "Flamengo"
    time_adversario: str = "River Plate"
    min_gol: int = 92
    rodada: int = 38
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class GolDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    jogador: str

def apresenta_gol(gol: Gol):
    """ Retorna uma representação do gol seguindo o schema definido em
        GolViewSchema.
    """
    return {
        "jogador": gol.jogador,
        "time_jogador": gol.time_jogador,
        "time_adversario": gol.time_adversario,
        "min_gol": gol.min_gol,
        "rodada": gol.rodada,
        "total_cometarios": len(gol.comentarios),
        "comentarios": [{"texto": c.texto} for c in gol.comentarios]
    }
