#!/usr/bin/env python3
"""Valida a integridade de dados/catalogo.csv."""

import csv
import sys
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "dados" / "catalogo.csv"

COLUNAS_OBRIGATORIAS = [
    "numero",
    "autor",
    "localidade",
    "tipo",
    "nota",
    "fonte",
    "pagina_inicial_pdf",
    "url_fonte",
    "data_acesso",
]


def validar(linhas):
    erros = []

    if not linhas:
        return ["catalogo.csv não contém nenhuma linha de dados."]

    cabecalho = linhas[0].keys()
    for coluna in COLUNAS_OBRIGATORIAS:
        if coluna not in cabecalho:
            erros.append(f"Coluna obrigatória ausente: '{coluna}'.")
    if erros:
        return erros

    numeros_vistos = set()
    esperado = 1
    for linha in linhas:
        numero = linha["numero"]

        if not numero.isdigit():
            erros.append(f"numero='{numero}' não é um inteiro válido.")
        else:
            if int(numero) != esperado:
                erros.append(
                    f"numero={numero} fora de sequência (esperado {esperado})."
                )
            esperado += 1
            if numero in numeros_vistos:
                erros.append(f"numero={numero} duplicado.")
            numeros_vistos.add(numero)

        if not linha["autor"].strip():
            erros.append(f"numero={numero}: campo 'autor' vazio.")

        if not linha["fonte"].strip():
            erros.append(f"numero={numero}: campo 'fonte' vazio.")

        pagina = linha["pagina_inicial_pdf"]
        if not pagina.isdigit() or int(pagina) < 1:
            erros.append(
                f"numero={numero}: 'pagina_inicial_pdf'='{pagina}' inválida."
            )

        url = linha["url_fonte"].strip()
        if not (url.startswith("http://") or url.startswith("https://")):
            erros.append(
                f"numero={numero}: 'url_fonte'='{url}' não é uma URL http(s) válida."
            )

        data_acesso = linha["data_acesso"].strip()
        partes = data_acesso.split("-")
        if len(partes) != 3 or not all(p.isdigit() for p in partes):
            erros.append(
                f"numero={numero}: 'data_acesso'='{data_acesso}' não está no formato AAAA-MM-DD."
            )

    return erros


def main():
    if not CSV_PATH.exists():
        print(f"Arquivo não encontrado: {CSV_PATH}", file=sys.stderr)
        return 1

    with CSV_PATH.open(newline="", encoding="utf-8") as arquivo:
        linhas = list(csv.DictReader(arquivo))

    erros = validar(linhas)

    if erros:
        print(f"❌ {len(erros)} problema(s) encontrado(s) em {CSV_PATH.name}:")
        for erro in erros:
            print(f"  - {erro}")
        return 1

    print(f"✅ {CSV_PATH.name} validado com sucesso ({len(linhas)} registros).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
