import pandas as pd
import json
from pathlib import Path

BASE = Path(__file__).parent

ARQUIVO = BASE / "BASE TESTE ITABAIANA OS SGM.xlsx"

df = pd.read_excel(
    ARQUIVO,
    engine="openpyxl"
)

df.columns = df.columns.str.strip()

for c in ["Latitude","Longitude"]:
    df[c] = pd.to_numeric(
        df[c],
        errors="coerce"
    )

df = df.dropna(
    subset=["Latitude","Longitude"]
)

if df.empty:
    raise Exception("Nenhuma coordenada encontrada.")

if "CodSetor" in df.columns:
    df["CodSetor"] = (
        df["CodSetor"]
        .fillna("")
        .astype(str)
        .str.replace(".0","",regex=False)
    )

campos = [
    "OSNumero",
    "Localidade",
    "Categoria",
    "CodSetor",
    "Abrangência",
    "Observação",
    "TIPO EQUIPE EXEC.",
    "Latitude",
    "Longitude"
]

campos = [c for c in campos if c in df.columns]

df = df[campos].fillna("")

saida = {
    "estatisticas":{
        "total":len(df),
        "categorias":df["Categoria"].nunique(),
        "equipes":df["TIPO EQUIPE EXEC."].nunique(),
        "localidades":df["Localidade"].nunique()
    },
    "dados":df.to_dict("records")
}

with open(
    BASE/"dados"/"os.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        saida,
        f,
        ensure_ascii=False,
        indent=2
    )

print("JSON criado.")