from __future__ import annotations

import json
from pathlib import Path
from pickle import dump

import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, cross_val_predict
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parent
RED_FILE = ROOT / "winequality-red.csv"
WHITE_FILE = ROOT / "winequality-white.csv"
DATA_DIR = ROOT / "data"
MODELS_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"

TARGET = "quality"
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


def carregar_dados() -> pd.DataFrame:
    vinhos_tintos = pd.read_csv(RED_FILE, sep=";")
    vinhos_brancos = pd.read_csv(WHITE_FILE, sep=";")
    dados = pd.concat([vinhos_tintos, vinhos_brancos], ignore_index=True)
    return dados[FEATURE_COLUMNS + [TARGET]]


def acuracia_por_classe(classe_teste, classe_predita, labels: list[int]) -> dict[str, float]:
    matriz = confusion_matrix(classe_teste, classe_predita, labels=labels)
    resultado = {}
    for indice, classe in enumerate(labels):
        total = matriz[indice].sum()
        resultado[str(classe)] = float(matriz[indice][indice] / total) if total else 0.0
    return resultado


def escrever_relatorio(relatorio: dict, caminho: Path) -> None:
    melhor = relatorio["melhor_modelo"]
    labels = melhor["labels"]
    linhas = [
        "# Wine Quality - Relatorio",
        "",
        "## Melhor Modelo",
        "",
        f"- Modelo: `{melhor['nome']}`",
        f"- Arquivo salvo: `{melhor['caminho_modelo']}`",
        f"- Acuracia global: `{melhor['acuracia_global']:.4f}`",
        f"- F1 macro: `{melhor['f1_macro']:.4f}`",
        f"- F1 ponderado: `{melhor['f1_weighted']:.4f}`",
        f"- Melhores parametros: `{melhor['melhores_parametros']}`",
        "",
        "## Comparacao dos Classificadores",
        "",
        "| Modelo | Acuracia | F1 macro | F1 ponderado |",
        "|---|---:|---:|---:|",
    ]

    for nome, metricas in relatorio["modelos"].items():
        linhas.append(
            f"| `{nome}` | {metricas['acuracia_global']:.4f} | "
            f"{metricas['f1_macro']:.4f} | {metricas['f1_weighted']:.4f} |"
        )

    linhas.extend(["", "## Acuracia por Classe", "", "| Classe quality | Acuracia |", "|---:|---:|"])
    for classe, acuracia in melhor["acuracia_por_classe"].items():
        linhas.append(f"| {classe} | {acuracia:.4f} |")

    linhas.extend(
        [
            "",
            "## Matriz de Confusao",
            "",
            "Linhas representam a classe real; colunas representam a classe prevista.",
            "",
            "| Real \\ Previsto | " + " | ".join(str(label) for label in labels) + " |",
            "|---|" + "|".join("---:" for _ in labels) + "|",
        ]
    )
    for classe, linha in zip(labels, melhor["matriz_confusao"]):
        linhas.append(f"| {classe} | " + " | ".join(str(valor) for valor in linha) + " |")

    linhas.append("")
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def montar_pipeline(classificador, random_state: int) -> Pipeline:
    return Pipeline(
        steps=[
            ("normalizacao", StandardScaler()),
            ("balanceamento", SMOTE(k_neighbors=1, random_state=random_state)),
            ("classificador", classificador),
        ]
    )


def treinar(random_state: int = 42, test_size: float = 0.3) -> dict:
    DATA_DIR.mkdir(exist_ok=True)
    MODELS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

    dados = carregar_dados()
    caminho_dados = DATA_DIR / "winequality-combined.csv"
    dados.to_csv(caminho_dados, index=False)

    atributos = dados[FEATURE_COLUMNS]
    classe = dados[TARGET]
    labels = sorted(classe.unique().tolist())
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

    classificadores = {
        "random_forest": {
            "pipeline": montar_pipeline(RandomForestClassifier(random_state=random_state), random_state),
            "parametros": {
                "classificador__n_estimators": [100],
                "classificador__max_depth": [None, 30],
                "classificador__min_samples_split": [2, 5],
                "classificador__max_features": ["sqrt"],
            },
            "n_iter": 2,
        },
        "extra_trees": {
            "pipeline": montar_pipeline(ExtraTreesClassifier(random_state=random_state), random_state),
            "parametros": {
                "classificador__n_estimators": [100],
                "classificador__max_depth": [None, 30],
                "classificador__min_samples_split": [2, 5],
                "classificador__max_features": ["sqrt"],
            },
            "n_iter": 2,
        },
        "gradient_boosting": {
            "pipeline": montar_pipeline(GradientBoostingClassifier(random_state=random_state), random_state),
            "parametros": {
                "classificador__n_estimators": [50],
                "classificador__learning_rate": [0.05, 0.1],
                "classificador__max_depth": [2],
            },
            "n_iter": 2,
        },
    }

    resultados = {}
    modelos_treinados = {}

    for nome, configuracao in classificadores.items():
        busca = RandomizedSearchCV(
            estimator=configuracao["pipeline"],
            param_distributions=configuracao["parametros"],
            n_iter=configuracao["n_iter"],
            cv=3,
            scoring="f1_macro",
            random_state=random_state,
            n_jobs=1,
        )
        modelo = busca.fit(atributos, classe).best_estimator_
        classe_predita = cross_val_predict(modelo, atributos, classe, cv=cv, n_jobs=1)
        modelo.fit(atributos, classe)
        caminho_modelo = MODELS_DIR / f"{nome}.pkl"
        dump(modelo, open(caminho_modelo, "wb"))
        modelos_treinados[nome] = modelo

        resultados[nome] = {
            "nome": nome,
            "caminho_modelo": str(caminho_modelo),
            "melhores_parametros": busca.best_params_,
            "acuracia_global": float(accuracy_score(classe, classe_predita)),
            "f1_macro": float(f1_score(classe, classe_predita, average="macro")),
            "f1_weighted": float(f1_score(classe, classe_predita, average="weighted")),
            "acuracia_por_classe": acuracia_por_classe(classe, classe_predita, labels),
            "matriz_confusao": confusion_matrix(classe, classe_predita, labels=labels).tolist(),
            "labels": labels,
        }

    melhor_nome = max(
        resultados,
        key=lambda nome: (resultados[nome]["f1_macro"], resultados[nome]["acuracia_global"]),
    )
    caminho_melhor_modelo = MODELS_DIR / "melhor_modelo_wine.pkl"
    dump(modelos_treinados[melhor_nome], open(caminho_melhor_modelo, "wb"))

    melhor_modelo = {
        **resultados[melhor_nome],
        "caminho_modelo": str(caminho_melhor_modelo),
    }

    relatorio = {
        "dataset": {
            "dados_combinados": str(caminho_dados),
            "linhas": int(len(dados)),
            "atributos": FEATURE_COLUMNS,
            "classe": TARGET,
        },
        "validacao": {
            "metodo": "StratifiedKFold",
            "n_splits": 5,
        },
        "modelos": resultados,
        "melhor_modelo": melhor_modelo,
    }

    caminho_json = REPORTS_DIR / "metrics.json"
    caminho_md = REPORTS_DIR / "metrics.md"
    caminho_json.write_text(json.dumps(relatorio, indent=2), encoding="utf-8")
    escrever_relatorio(relatorio, caminho_md)

    print(f"Dados combinados: {caminho_dados}")
    print(f"Melhor modelo: {melhor_nome}")
    print(f"Modelo salvo: {caminho_melhor_modelo}")
    print(f"Acuracia global: {melhor_modelo['acuracia_global']:.4f}")
    print(f"F1 macro: {melhor_modelo['f1_macro']:.4f}")
    print(f"Relatorio: {caminho_md}")
    return relatorio


def main() -> None:
    treinar()


if __name__ == "__main__":
    main()
