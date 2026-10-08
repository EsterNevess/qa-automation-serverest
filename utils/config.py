"""Endereços do sistema testado.

Por padrão, os testes usam a versão pública do ServeRest.
Para usar outro endereço (por exemplo, o ServeRest rodando no seu computador),
defina as variáveis de ambiente API_URL e WEB_URL antes de rodar os testes.
"""
import os

API_URL = os.getenv("API_URL", "https://serverest.dev").rstrip("/")
WEB_URL = os.getenv("WEB_URL", "https://front.serverest.dev").rstrip("/")
