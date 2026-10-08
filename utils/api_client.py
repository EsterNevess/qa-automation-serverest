"""Cliente da API do ServeRest.

Em vez de repetir requests.post(...) em todos os testes, juntamos aqui
as chamadas da API. Assim os testes ficam curtos e fáceis de ler, e se
um endereço mudar, só precisamos alterar este arquivo.
"""
import requests

from utils.config import API_URL


class ServeRestClient:
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = 15  # segundos de espera máxima por resposta

    def _url(self, caminho: str) -> str:
        return f"{self.base_url}{caminho}"

    # ---------- Usuários ----------
    def cadastrar_usuario(self, dados: dict) -> requests.Response:
        return self.session.post(self._url("/usuarios"), json=dados, timeout=self.timeout)

    def buscar_usuario(self, usuario_id: str) -> requests.Response:
        return self.session.get(self._url(f"/usuarios/{usuario_id}"), timeout=self.timeout)

    def listar_usuarios(self, **filtros) -> requests.Response:
        return self.session.get(self._url("/usuarios"), params=filtros, timeout=self.timeout)

    def editar_usuario(self, usuario_id: str, dados: dict) -> requests.Response:
        return self.session.put(self._url(f"/usuarios/{usuario_id}"), json=dados, timeout=self.timeout)

    def excluir_usuario(self, usuario_id: str) -> requests.Response:
        return self.session.delete(self._url(f"/usuarios/{usuario_id}"), timeout=self.timeout)

    # ---------- Login ----------
    def login(self, email: str, senha: str) -> requests.Response:
        return self.session.post(
            self._url("/login"), json={"email": email, "password": senha}, timeout=self.timeout
        )

    # ---------- Produtos ----------
    def cadastrar_produto(self, dados: dict, token: str | None = None) -> requests.Response:
        headers = {"Authorization": token} if token else {}
        return self.session.post(self._url("/produtos"), json=dados, headers=headers, timeout=self.timeout)

    def buscar_produto(self, produto_id: str) -> requests.Response:
        return self.session.get(self._url(f"/produtos/{produto_id}"), timeout=self.timeout)

    def editar_produto(self, produto_id: str, dados: dict, token: str) -> requests.Response:
        return self.session.put(
            self._url(f"/produtos/{produto_id}"), json=dados,
            headers={"Authorization": token}, timeout=self.timeout,
        )

    def excluir_produto(self, produto_id: str, token: str) -> requests.Response:
        return self.session.delete(
            self._url(f"/produtos/{produto_id}"), headers={"Authorization": token}, timeout=self.timeout
        )
