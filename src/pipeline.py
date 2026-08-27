
import argparse
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

DATA_FILE = "Planilha_de_correspondencia_20_Rev1.xlsx"
SHEET_NAME = "DATASET_NLP"
HEADER_ROW = 2  # cabeçalho na terceira linha da aba, contando a partir de zero
TEXT_COLUMN = "TEXTO_SERVICO"
TARGET_COLUMN = "Classificação NBR 15965"
SEEDS = (7, 21, 42, 84, 123)
TEST_SIZE = 0.20

def carregar_dataset(caminho: Path) -> pd.DataFrame:
    """Lê a aba DATASET_NLP e mantém somente registros completos."""
    df = pd.read_excel(
        caminho,
        sheet_name=SHEET_NAME,
        header=HEADER_ROW,
    )
    # Remove colunas sem nome geradas pela primeira coluna vazia da planilha.
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed:")].copy()
    colunas_necessarias = {TEXT_COLUMN, TARGET_COLUMN}
    ausentes = colunas_necessarias.difference(df.columns)
    if ausentes:
        raise ValueError(
            "Colunas obrigatórias ausentes na aba DATASET_NLP: "
            + ", ".join(sorted(ausentes))
        )
    df[TEXT_COLUMN] = df[TEXT_COLUMN].astype("string").str.strip()
    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype("string").str.strip()
    df = df.dropna(subset=[TEXT_COLUMN, TARGET_COLUMN]).copy()
    df = df[(df[TEXT_COLUMN] != "") & (df[TARGET_COLUMN] != "")].copy()
    return df.reset_index(drop=True)

def filtrar_classes_unitarias(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Remove classes com uma única ocorrência e retorna suas frequências."""
    frequencias = df[TARGET_COLUMN].value_counts()
    classes_unitarias = frequencias[frequencias < 2].index
    filtrado = df[~df[TARGET_COLUMN].isin(classes_unitarias)].copy()
    return filtrado.reset_index(drop=True), frequencias

def criar_modelo(seed: int) -> Pipeline:
    """Cria um pipeline TF-IDF + LinearSVC para uma repetição."""
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    lowercase=True,
                    strip_accents="unicode",
                    stop_words=None,
                ),
            ),
            ("svm", LinearSVC(random_state=seed)),
        ]
    )
def executar_benchmark(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Executa as cinco repetições e retorna resultados por semente e resumo."""
    X = df[TEXT_COLUMN]
    y = df[TARGET_COLUMN]
    resultados = []

    for seed in SEEDS:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=TEST_SIZE,
            random_state=seed,
            stratify=y,
        )
        modelo = criar_modelo(seed)
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        resultados.append(
            {
                "semente": seed,
                "treino_n": len(X_train),
                "teste_n": len(X_test),
                "acuracia": accuracy_score(y_test, y_pred),
                "f1_macro": f1_score(
                    y_test, y_pred, average="macro", zero_division=0
                ),
                "f1_ponderado": f1_score(
                    y_test, y_pred, average="weighted", zero_division=0
                ),
                "balanced_accuracy": balanced_accuracy_score(y_test, y_pred),
            }
        )
    por_semente = pd.DataFrame(resultados)
    metricas = [
        "acuracia",
        "f1_macro",
        "f1_ponderado",
        "balanced_accuracy",
    ]
    resumo = pd.DataFrame(
        {
            "media": por_semente[metricas].mean(),
            "desvio_padrao": por_semente[metricas].std(ddof=1),
        }
    ).reset_index(names="metrica")
    return por_semente, resumo

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Executa o benchmark TF-IDF + LinearSVC da aba DATASET_NLP."
    )
    parser.add_argument(
        "planilha",
        type=Path,
        help="Caminho da planilha de correspondência (.xlsx).",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=Path("resultados_benchmark"),
        help="Pasta para salvar os resultados (padrão: resultados_benchmark).",
    )
    args = parser.parse_args()

    df_bruto = carregar_dataset(args.planilha)
    df_filtrado, frequencias = filtrar_classes_unitarias(df_bruto)

    classes_unitarias = int((frequencias < 2).sum())
    registros_unitarios = int(frequencias[frequencias < 2].sum())
    classes_finais = int(df_filtrado[TARGET_COLUMN].nunique())

    por_semente, resumo = executar_benchmark(df_filtrado)

    args.saida.mkdir(parents=True, exist_ok=True)
    por_semente.to_csv(args.saida / "resultados_por_semente.csv", index=False)
    resumo.to_csv(args.saida / "resumo_metricas.csv", index=False)

    auditoria = pd.DataFrame(
        [
            {
                "aba": SHEET_NAME,
                "registros_brutos": len(df_bruto),
                "classes_brutas": int(df_bruto[TARGET_COLUMN].nunique()),
                "classes_unitarias_removidas": classes_unitarias,
                "registros_unitarios_removidos": registros_unitarios,
                "registros_finais": len(df_filtrado),
                "classes_finais": classes_finais,
                "textos_TEXTO_SERVICO_unicos": int(df_bruto[TEXT_COLUMN].nunique()),
            }
        ]
    )

    auditoria.to_csv(args.saida / "auditoria_dataset.csv", index=False)

    print(f"Registros brutos: {len(df_bruto)}")
    print(f"Classes brutas: {df_bruto[TARGET_COLUMN].nunique()}")
    print(f"Classes unitárias removidas: {classes_unitarias}")
    print(f"Registros finais: {len(df_filtrado)}")
    print(f"Classes finais: {classes_finais}")
    print("\nResultados por semente:")
    print(por_semente.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\nResumo:")
    print(resumo.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

if __name__ == "__main__":
    main()
