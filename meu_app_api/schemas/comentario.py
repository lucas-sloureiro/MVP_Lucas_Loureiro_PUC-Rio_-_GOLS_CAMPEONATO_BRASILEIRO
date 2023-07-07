from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    gol_id: int = 1
    texto: str = "Hoje tem gol do Gabigol! |_O_|"
