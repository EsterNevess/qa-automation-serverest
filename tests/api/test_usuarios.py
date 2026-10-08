"""Testes da rota /usuarios (cadastro, consulta, edição e exclusão)."""
import pytest

from utils.data_factory import novo_usuario
from utils.schema_validator import validar_schema

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_cadastrar_usuario_com_sucesso(api):
    dados = novo_usuario()

    resposta = api.cadastrar_usuario(dados)

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["message"] == "Cadastro realizado com sucesso"
    assert corpo["_id"]
    api.excluir_usuario(corpo["_id"])  # limpeza


def test_nao_cadastrar_usuario_com_email_ja_usado(api, usuario_cadastrado):
    dados = novo_usuario()
    dados["email"] = usuario_cadastrado["email"]  # e-mail repetido de propósito

    resposta = api.cadastrar_usuario(dados)

    assert resposta.status_code == 400
    assert resposta.json()["message"] == "Este email já está sendo usado"


@pytest.mark.parametrize("campo", ["nome", "email", "password", "administrador"])
def test_nao_cadastrar_usuario_sem_campo_obrigatorio(api, campo):
    dados = novo_usuario()
    dados.pop(campo)  # remove um campo obrigatório

    resposta = api.cadastrar_usuario(dados)

    assert resposta.status_code == 400
    assert campo in resposta.json()  # a API diz qual campo está faltando


def test_nao_cadastrar_usuario_com_email_invalido(api):
    dados = novo_usuario()
    dados["email"] = "email-sem-arroba.com"

    resposta = api.cadastrar_usuario(dados)

    assert resposta.status_code == 400
    assert resposta.json()["email"] == "email deve ser um email válido"


def test_buscar_usuario_por_id(api, usuario_cadastrado):
    resposta = api.buscar_usuario(usuario_cadastrado["_id"])

    assert resposta.status_code == 200
    corpo = resposta.json()
    validar_schema(corpo, "usuario.json")
    assert corpo["email"] == usuario_cadastrado["email"]
    assert corpo["nome"] == usuario_cadastrado["nome"]


def test_buscar_usuario_inexistente(api):
    # id no formato certo (16 letras/números), mas que não existe
    resposta = api.buscar_usuario("abcdefghij123456")

    assert resposta.status_code == 400
    assert resposta.json()["message"] == "Usuário não encontrado"


def test_buscar_usuario_com_id_em_formato_invalido(api):
    resposta = api.buscar_usuario("123")  # id curto demais

    assert resposta.status_code == 400
    assert "id" in resposta.json()


def test_listar_usuarios_filtrando_por_email(api, usuario_cadastrado):
    resposta = api.listar_usuarios(email=usuario_cadastrado["email"])

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["quantidade"] == 1
    validar_schema(corpo["usuarios"][0], "usuario.json")


def test_editar_usuario(api, usuario_cadastrado):
    novos_dados = {
        "nome": "Nome Editado pelo Teste",
        "email": usuario_cadastrado["email"],
        "password": usuario_cadastrado["password"],
        "administrador": "true",
    }

    resposta = api.editar_usuario(usuario_cadastrado["_id"], novos_dados)

    assert resposta.status_code == 200
    assert resposta.json()["message"] == "Registro alterado com sucesso"
    # confere se a alteração foi gravada de verdade
    assert api.buscar_usuario(usuario_cadastrado["_id"]).json()["nome"] == "Nome Editado pelo Teste"


def test_excluir_usuario(api):
    usuario_id = api.cadastrar_usuario(novo_usuario()).json()["_id"]

    resposta = api.excluir_usuario(usuario_id)

    assert resposta.status_code == 200
    assert resposta.json()["message"] == "Registro excluído com sucesso"
    assert api.buscar_usuario(usuario_id).status_code == 400  # não existe mais
