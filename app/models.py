from pydantic import BaseModel, HttpUrl, EmailStr
from typing import List

class Deputado(BaseModel):
    id: int
    uri: HttpUrl
    nome: str
    siglaPartido: str
    uriPartido: HttpUrl
    siglaUf: str
    idLegislatura: int
    urlFoto: HttpUrl
    email: EmailStr

class Deputados(BaseModel):
    dados: List[Deputado]

class Despesa(BaseModel):
    # Defina os campos com base na estrutura JSON da despesa
    pass

class Despesas(BaseModel):
    dados: List[Despesa]