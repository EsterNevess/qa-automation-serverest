"""Validação de contrato (schema) das respostas da API.

O schema é um "molde" em JSON que descreve como a resposta deve ser:
quais campos existem, de que tipo são e quais são obrigatórios.
Se a API mudar o formato da resposta, o teste avisa.
"""
import json
from pathlib import Path

from jsonschema import validate

PASTA_SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"


def validar_schema(dados: dict, nome_arquivo: str) -> None:
    """Compara a resposta com o schema. Se não bater, o teste falha."""
    schema = json.loads((PASTA_SCHEMAS / nome_arquivo).read_text(encoding="utf-8"))
    validate(instance=dados, schema=schema)
