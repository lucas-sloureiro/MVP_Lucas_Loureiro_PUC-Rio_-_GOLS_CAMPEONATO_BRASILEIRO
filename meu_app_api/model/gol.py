from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Gol(Base):
    __tablename__ = 'gol'

    id = Column("pk_gol", Integer, primary_key=True)
    jogador = Column(String(140))
    time_jogador = Column(String(140))
    time_adversario = Column(String(140))
    min_gol = Column(Integer)
    rodada = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o gol e o comentário.
    # Essa relação é implicita, não está salva na tabela 'gol',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, jogador:str, time_jogador:str, time_adversario:str,
                 min_gol:int, rodada:int,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Gol

        Arguments:
            jogador: Nome do Jogador.
            time_jogador: Time do jogador que marcou o gol.
            time_jogador: Time que sofreu o gol.
            min_gol: Minuto que o gol foi marcado no formato internacional.
            rodada: Rodada do Campeonato Brasileiro que o gol foi marcado.
            data_insercao: Data de quando o gol foi inserido à base.
        """
        self.jogador = jogador
        self.time_jogador = time_jogador
        self.time_adversario = time_adversario
        self.min_gol = min_gol
        self.rodada = rodada
       
        # Se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Gol
        """
        self.comentarios.append(comentario)

