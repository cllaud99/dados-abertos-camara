from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


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


class Gabinete(BaseModel):
    nome: str
    predio: str
    sala: str
    andar: str
    telefone: str
    email: str


class UltimoStatus(BaseModel):
    id: int
    uri: str
    nome: str
    siglaPartido: str
    uriPartido: str
    siglaUf: str
    idLegislatura: int
    urlFoto: str
    email: str
    data: str
    nomeEleitoral: str
    gabinete: Gabinete
    situacao: str
    condicaoEleitoral: str
    descricaoStatus: Optional[str]


class Dados(BaseModel):
    id: int
    uri: str
    nomeCivil: str
    ultimoStatus: UltimoStatus
    cpf: str
    sexo: str
    urlWebsite: Optional[str]
    redeSocial: List[str]
    dataNascimento: str
    dataFalecimento: Optional[str]
    ufNascimento: str
    municipioNascimento: str
    escolaridade: str


class Links(BaseModel):
    rel: str
    href: str


class DadosDeputado(BaseModel):
    dados: Dados
    links: List[Links]
