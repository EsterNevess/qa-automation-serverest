"""Geração de dados de teste.

Usamos a biblioteca Faker para criar nomes, e-mails e produtos diferentes
a cada execução. Assim um teste não "esbarra" nos dados de outro
(por exemplo, dois testes tentando usar o mesmo e-mail).
"""
import uuid

from faker import Faker

fake = Faker("pt_BR")


def novo_usuario(administrador: bool = True) -> dict:
    """Retorna os dados de um usuário novo, com e-mail único."""
    return {
        "nome": fake.name(),
        "email": f"qa_{uuid.uuid4().hex[:10]}@teste.com",
        "password": fake.password(length=10),
        "administrador": "true" if administrador else "false",
    }


def novo_produto() -> dict:
    """Retorna os dados de um produto novo, com nome único."""
    return {
        "nome": f"Produto QA {uuid.uuid4().hex[:8]}",
        "preco": fake.random_int(min=10, max=5000),
        "descricao": fake.sentence(nb_words=5),
        "quantidade": fake.random_int(min=1, max=100),
    }
