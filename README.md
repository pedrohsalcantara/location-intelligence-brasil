# PFC Location Intelligence - Data Discovery

PoC inicial para validar a viabilidade técnica de uma solução de inteligência territorial municipal usando dados públicos oficiais do IBGE.

## Objetivo desta etapa

- Conectar em APIs oficiais do IBGE/SIDRA.
- Ler metadados e dados municipais reais.
- Avaliar linhas, colunas, períodos, variáveis e cobertura municipal.
- Gerar uma primeira tabela Gold com uma linha por município.

## Execução com uv (recomendado)

Requer Python 3.11 ou superior e o [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python -m src.ingestion.run_ibge_discovery
```

O `uv sync` cria o ambiente virtual local e instala as dependências a partir
do `pyproject.toml` e do `uv.lock`.

## Execução com venv/pip

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.ingestion.run_ibge_discovery
```

Os resultados são gravados em:

- `data/bronze/`: respostas brutas e metadados da consulta.
- `data/silver/`: dados tabulares padronizados.
- `data/gold/`: primeira tabela municipal integrada.
- `docs/data_discovery.md`: resumo técnico da descoberta.
