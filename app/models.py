from datetime import date
from typing import Optional, List

from pydantic import BaseModel, HttpUrl

class Despesa(BaseModel):
    ano: int
    mes: int
    tipoDespesa: str
    codDocumento: int
    tipoDocumento: str
    codTipoDocumento: int
    dataDocumento: date
    numDocumento: str
    valorDocumento: float
    urlDocumento: Optional[str]
    nomeFornecedor: str
    cnpjCpfFornecedor: str
    valorLiquido: float
    valorGlosa: float
    numRessarcimento: str
    codLote: int
    parcela: int

class Deputado(BaseModel):
    id: int
    uri: str
    nome: str
    siglaPartido: str
    uriPartido: str
    siglaUf: str
    idLegislatura: int
    urlFoto: str
    email: str
