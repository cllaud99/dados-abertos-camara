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
    email: Optional[str]


class Gabinete(BaseModel):
    nome: Optional[str]
    predio: Optional[str]
    sala: Optional[str]
    andar: Optional[str]
    telefone: Optional[str]
    email: Optional[str]


class UltimoStatus(BaseModel):
    id: int
    uri: str
    nome: str
    siglaPartido: str
    uriPartido: str
    siglaUf: str
    idLegislatura: int
    urlFoto: Optional[str]
    email: Optional[str]
    data: Optional[str]
    nomeEleitoral: Optional[str]
    gabinete: Gabinete
    situacao: str
    condicaoEleitoral: str
    descricaoStatus: Optional[str]

    def to_dict(self):
        return self.model_dump()


class DadosDeputado(BaseModel):
    id: int
    uri: str
    nomeCivil: str
    ultimoStatus: UltimoStatus
    cpf: str
    sexo: str
    urlWebsite: Optional[str]
    redeSocial: List[str]
    dataNascimento: date
    dataFalecimento: Optional[str]
    ufNascimento: str
    municipioNascimento: Optional[str]
    escolaridade: Optional[str]


class Links(BaseModel):
    rel: str
    href: str


class DeputadoHistorico(BaseModel):
    condicaoEleitoral: Optional[str]
    dataHora: datetime
    descricaoStatus: Optional[str]
    email: Optional[str]
    id: int
    idLegislatura: int
    nome: str
    nomeEleitoral: Optional[str]
    siglaPartido: str
    siglaUf: str
    situacao: Optional[str]
    uri: Optional[str]
    uriPartido: Optional[str]
    urlFoto: Optional[str]
