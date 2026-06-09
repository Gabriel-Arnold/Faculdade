from __future__ import annotations

import argparse
import json
from pathlib import Path
from pickle import load

import pandas as pd


ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL = ROOT / "models" / "melhor_modelo_wine.pkl"
FEATURE_COLUMNS = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
]


def carregar_entrada(args: argparse.Namespace) -> pd.DataFrame:
    if args.csv:
        dados = pd.read_csv(args.csv)
    elif args.json:
        instancia = json.loads(args.json)
        dados = pd.DataFrame([instancia] if isinstance(instancia, dict) else instancia)
    else:
        raise SystemExit("Informe --csv caminho.csv ou --json '{...}'.")

    colunas_ausentes = [coluna for coluna in FEATURE_COLUMNS if coluna not in dados.columns]
    if colunas_ausentes:
        raise SystemExit(f"Entrada sem as colunas obrigatorias: {colunas_ausentes}")
    return dados[FEATURE_COLUMNS]


def main() -> None:
    parser = argparse.ArgumentParser(description="Inferencia do modelo Wine Quality.")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--json")
    args = parser.parse_args()

    if not args.model.exists():
        raise SystemExit(f"Modelo nao encontrado: {args.model}. Execute train.py primeiro.")

    dados = carregar_entrada(args)
    modelo = load(open(args.model, "rb"))
    saida = dados.copy()
    saida["predicted_quality"] = modelo.predict(dados)

    if hasattr(modelo, "predict_proba"):
        saida["prediction_confidence"] = modelo.predict_proba(dados).max(axis=1)

    print(saida.to_json(orient="records", indent=2))


if __name__ == "__main__":
    main()
