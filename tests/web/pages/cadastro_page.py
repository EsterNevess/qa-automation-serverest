"""Page Object da tela de Cadastro de usuário."""
from tests.web.pages.base_page import BasePage


class CadastroPage(BasePage):
    caminho = "/cadastrarusuarios"

    def cadastrar(self, nome: str, email: str, senha: str, administrador: bool = False):
        self.elemento("nome").fill(nome)
        self.elemento("email").fill(email)
        self.elemento("password").fill(senha)
        if administrador:
            self.elemento("checkbox").check()
        self.elemento("cadastrar").click()

    def mensagem(self):
        return self.page.locator(".alert").first
