# Cloud Resource Audit CLI

[English](../README.md) | [Español](README.es.md) | **Português**

Ferramenta de linha de comando desenvolvida em Python para auditar inventários simulados de recursos de nuvem, identificar problemas de configuração e gerar relatórios estruturados.

## Visão geral

Cloud Resource Audit CLI é uma aplicação leve em Python projetada para analisar inventários de infraestrutura em nuvem armazenados em arquivos JSON.

A aplicação valida os dados dos recursos, aplica regras de auditoria predefinidas, calcula estatísticas do inventário e gera um relatório legível diretamente no terminal.

O projeto demonstra competências práticas de engenharia de software, incluindo desenvolvimento modular em Python, validação de entradas, tratamento de exceções, testes automatizados e empacotamento de aplicações de linha de comando.

**Escopo atual:** A aplicação utiliza inventários simulados. Não se conecta ao Azure nem a outros provedores de nuvem.

## Funcionalidades

- Carregamento de inventários de recursos de nuvem a partir de arquivos JSON.
- Validação da estrutura do inventário e dos atributos dos recursos.
- Identificação de problemas de configuração e custos.
- Classificação das ocorrências por severidade.
- Cálculo da quantidade de recursos e dos custos mensais estimados.
- Geração de relatórios legíveis no terminal.
- Tratamento de arquivos e dados inválidos com mensagens de erro claras.
- Execução de auditorias com o comando `cloud-audit`.
- Testes automatizados com pytest.

## Tecnologias utilizadas

- **Python 3.12+** — Desenvolvimento da aplicação.
- **Biblioteca padrão do Python** — Processamento de JSON, argumentos de linha de comando e tratamento de erros.
- **pytest** — Testes automatizados.
- **setuptools** — Configuração e instalação do pacote Python.
- **Git e GitHub** — Controle de versão.

## Estrutura do projeto

```text
cloud-resource-audit/
├── data/                     # Inventários JSON de exemplo
├── src/
│   └── cloud_audit/
│       ├── loader.py         # Carregamento de arquivos JSON
│       ├── validator.py      # Validação do inventário
│       ├── auditor.py        # Regras de auditoria
│       ├── statistics.py     # Estatísticas do inventário
│       ├── report.py         # Formatação do relatório
│       └── cli.py            # Interface de linha de comando
├── tests/                    # Testes automatizados
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Instalação

### 1. Clonar o repositório

Por SSH:

```bash
git clone git@github.com:CloudIAIoT/cloud-resource-audit.git
cd cloud-resource-audit
```

Alternativamente, por HTTPS:

```bash
git clone https://github.com/CloudIAIoT/cloud-resource-audit.git
cd cloud-resource-audit
```

### 2. Criar um ambiente virtual

No Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar o projeto

```bash
python -m pip install -e .
```

A instalação em modo editável registra o comando `cloud-audit`.

## Uso

Executar uma auditoria informando o caminho do inventário JSON:

```bash
cloud-audit data/inventory_clean.json
```

Analisar um inventário que contém problemas de configuração:

```bash
cloud-audit data/inventory_findings.json
```

Exibir a ajuda do comando:

```bash
cloud-audit --help
```

## Tipos de recursos suportados

| Tipo de recurso | Estados suportados |
|---|---|
| `virtual_machine` | `running`, `stopped` |
| `storage_account` | `active` |

Cada recurso deve conter um identificador, tipo, estado, custo mensal e dicionário de etiquetas (`tags`).

O campo `environment` é opcional. Sua ausência gera uma ocorrência de auditoria, em vez de invalidar o inventário.

Os ambientes suportados são `production`, `development` e `test`.

## Regras de auditoria

A aplicação implementa quatro regras:

| Regra | Severidade | Descrição |
|---|---|---|
| `MISSING_OWNER` | Média | O recurso não possui a etiqueta `owner`. |
| `MISSING_ENVIRONMENT` | Média | O recurso não possui um ambiente definido. |
| `STOPPED_VM_COST` | Alta | Uma máquina virtual parada apresenta custo mensal positivo. |
| `MISSING_PRODUCTION_TAG` | Alta | Um recurso de produção não possui a etiqueta `criticality`. |

Um mesmo recurso pode gerar várias ocorrências.

## Exemplo de saída

O exemplo a seguir apresenta um relatório de inventário com problemas de configuração:

```text
INVENTORY SUMMARY
Total resources: 3
Virtual machines: 2
Storage accounts: 1
Total monthly cost: $140.75

AUDIT SUMMARY
Total findings: 5
High severity: 2
Medium severity: 3
Low severity: 0

FINDINGS

[MEDIUM] vm-test-01
Rule: MISSING_OWNER
Resource has no owner tag

[HIGH] vm-test-01
Rule: STOPPED_VM_COST
Stopped virtual machine has a positive monthly cost
```

As demais ocorrências são exibidas no mesmo formato. As mensagens da CLI permanecem em inglês, independentemente do idioma da documentação.

Os custos mensais são fornecidos pelo inventário de entrada. A aplicação não consulta dados reais de faturamento em nuvem.

## Tratamento de erros

A CLI trata erros comuns, incluindo:

- Arquivos de inventário inexistentes.
- Arquivos JSON malformados.
- Estrutura de inventário inválida.
- Ausência de atributos obrigatórios.
- Tipos de recursos ou estados não suportados.
- Valores inválidos de custo mensal.

A aplicação retorna o código de saída `0` quando a auditoria é executada corretamente, mesmo que encontre ocorrências.

Erros de entrada retornam o código `1`.

## Testes automatizados

O projeto utiliza pytest para verificar o carregamento, a validação, a auditoria, as estatísticas e a geração de relatórios.

Instalar pytest, caso ainda não esteja disponível:

```bash
python -m pip install pytest
```

Executar os testes a partir da raiz do repositório:

```bash
python -m pytest -v
```

## Limitações atuais

- Os inventários devem ser fornecidos em arquivos JSON locais.
- Os tipos de recursos e as regras de auditoria são predefinidos.
- Os custos mensais são estimativas informadas no inventário.
- A aplicação não se conecta à infraestrutura real de nuvem.
- Os relatórios são exibidos no terminal, sem exportação para arquivos.

## Melhorias futuras

- Integração com inventários de recursos do Azure.
- Regras adicionais de segurança, governança e otimização de custos.
- Políticas de auditoria configuráveis.
- Exportação de relatórios em JSON ou CSV.
- Execução automatizada em pipelines de CI/CD.

## Licença

Nenhuma licença foi especificada para este projeto.
