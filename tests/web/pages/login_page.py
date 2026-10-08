"""Page Object da tela de Login.

Page Object é uma classe que representa uma tela do sistema.
Ela guarda ONDE estão os elementos (campos, botões) e AÇÕES da tela
(fazer login). Se a tela mudar, ajustamos só aqui, e não em cada teste.
"""
from tests.web.pages.base_page import BasePage


class LoginPage(BasePage):
    caminho = "/login"

    def fazer_login(self, email: str, senha: str):
        self.elemento("email").fill(email)
        self.elemento("senha").fill(senha)
        self.elemento("entrar").click()

    def ir_para_cadastro(self):
        self.elemento("cadastrar").click()

    def mensagem_de_erro(self):
        return self.page.locator(".alert").first
