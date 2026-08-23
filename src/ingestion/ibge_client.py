from __future__ import annotations

import logging
from typing import Any

import requests


LOGGER = logging.getLogger(__name__)


class IBGEClient:
    """Small HTTP client for official IBGE services used in this PoC."""

    def __init__(self, timeout: int = 60) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "pfc-location-intelligence-poc/0.1"})

    def get_json(self, url: str) -> Any:
        LOGGER.info("GET %s", url)
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_municipalities(self) -> list[dict[str, Any]]:
        return self.get_json("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")

    def get_aggregate_metadata(self, table_id: str) -> Any:
        return self.get_json(f"https://servicodados.ibge.gov.br/api/v3/agregados/{table_id}/metadados")

    def get_aggregate_periods(self, table_id: str) -> Any:
        return self.get_json(f"https://servicodados.ibge.gov.br/api/v3/agregados/{table_id}/periodos")

    def get_sidra_values(
        self,
        table_id: str,
        period: str,
        variables: list[str],
        territory_level: str = "6",
        territories: str = "all",
    ) -> list[dict[str, Any]]:
        variables_part = ",".join(variables)
        url = (
            "https://apisidra.ibge.gov.br/values"
            f"/t/{table_id}/n{territory_level}/{territories}"
            f"/v/{variables_part}/p/{period}/h/y/f/a/d/m"
        )
        return self.get_json(url)
