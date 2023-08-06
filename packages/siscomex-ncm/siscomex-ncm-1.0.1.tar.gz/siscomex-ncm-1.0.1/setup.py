# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ncm']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'siscomex-ncm',
    'version': '1.0.1',
    'description': 'API access to the NCM (Nomenclatura Comum do Mercosul) by Siscomex',
    'long_description': "## siscomex-ncm\n[![PyPI](https://img.shields.io/pypi/v/siscomex-ncm)](https://pypi.org/project/siscomex-ncm/) ![pyversions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue) ![https://github.com/leogregianin/siscomex-ncm/actions](https://github.com/leogregianin/siscomex-ncm/workflows/CI/badge.svg?branch=main)\n\n## NCM (Nomenclatura Comum do Mercosul)\n\n`NCM` é a sigla para `Nomenclatura Comum do Mercosul`, toda e qualquer mercadoria que circula no Brasil deve ter este código. A NCM permite a identificação padronizada das mercadorias comercializadas, ou seja todo produto possui uma NCM.\n\nO código deve ser informado no preenchimento da nota fiscal e outros documentos de comércio exterior.\n\nA NCM é adotada por todos os países membros do Mercosul desde janeiro de 1995 e tem como base o método internacional de classificação de mercadoria, chamado como SH (Sistema Harmonizado de Designação e de Codificação de Mercadorias).\n\nO código é usado nas operações de exportação e importação de mercadorias desde 1995, já no mercado interno é obrigatório desde 2013.\n\n## Como funciona?\n\nA Nomenclatura Comum do Mercosul obedece à seguinte estrutura de código: 0000.00.00\n\nOu seja, é um código de oito dígitos que correspondem ao produto. Cada um dos numerais representa algo diferente, conforme abaixo:\n\n * Os dois primeiros caracterizam o produto (capítulo);\n * Os dois números seguintes abrangem mais sobre a característica do produto (posição);\n * O quinto e sexto definem a subcategoria do mesmo (ou subposição);\n * O sétimo o classifica (item); e\n * O oitavo se refere ao subitem, que descreve especificamente do que se trata a mercadoria.\n\nPara exemplificar, veja a NCM `4820.20.00`, deve ser entendido da seguinte forma:\n\n * Capítulo 48: Papel e cartão; obras de pasta de celulose, de papel ou de cartão.\n\n * Posição 48.20: Livros de registro e de contabilidade, blocos de notas, de encomendas, de recibos, de apontamentos, de papel para cartas, agendas e artigos semelhantes, cadernos, pastas para documentos, classificadores, capas para encadernação (de folhas soltas ou outras), capas de processos e outros artigos escolares, de escritório ou de papelaria, incluindo os formulários em blocos tipo manifold, mesmo com folhas intercaladas de papel-carbono (papel químico), de papel ou cartão; álbuns para amostras ou para coleções e capas para livros, de papel ou cartão.\n\n * Subposição: Neste exemplo não tem.\n\n * Item: Neste exemplo não tem.\n\n * Subitem 4820.20.00 – Cadernos\n\n\n\n## Como instalar a biblioteca pelo PyPI?\n\n * `pip install siscomex-ncm`\n\n\n## Como instalar a biblioteca pelo código-fonte?\n\n * Faça fork deste projeto\n * Instale o [poetry](https://python-poetry.org/docs/#installation)\n * Instale as dependências do projeto: `poetry install`\n\n\n## Como executar os testes?\n\n * Executar os testes: `make test`\n\n\n## Como usar essa biblioteca?\n\n### Importar a biblioteca\n\n```python\nfrom ncm.entities import Ncm, NcmList\nfrom ncm.client import FetchNcm\n```\n\n### Download do arquivo JSON\n\n```python\nfetch_ncm = FetchNcm()\nfetch_ncm.download_json()\n```\n\n\n### Gravar do arquivo JSON localmente\n\n```python\nfetch_ncm = FetchNcm()\nfetch_ncm.download_json()\nfetch_ncm.save_json(json_data)\njson_data = fetch_ncm.load_json()\n```\n\n### Consulta código NCM específico\n\n```python\nfetch_ncm = FetchNcm()\nobj_dict = fetch_ncm.get_codigo_ncm('01031000')\nprint(obj_dict.descricao_ncm)  # result: '- Reprodutores de raça pura'\n```\n\n### Consulta toda a lista de NCMs\n\n```python\nfetch_ncm = FetchNcm()\nncm_list = fetch_ncm.get_all()\nprint(ncm_list.ncm_list)\n```\n\n### Consulta toda a lista de NCMs e retorno somente os códigos com 8 dígitos\n\n```python\nfetch_ncm = FetchNcm()\nfetch_ncm.only_ncm_8_digits = True\nncm_list = fetch_ncm.get_all()\nprint(ncm_list.ncm_list)\n```\n\n## Licença\n\n  MIT License",
    'author': 'Leonardo Gregianin',
    'author_email': 'leogregianin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leogregianin/siscomex-ncm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
