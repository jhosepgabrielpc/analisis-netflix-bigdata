import pandas as pd
import glob
import os

archivos = glob.glob('resultados_hadoop/part-*')
dfs = []

for archivo in archivos:
    if os.path.getsize(archivo) > 0:
        df = pd.read_csv(archivo, sep='\t', header=None, names=['actor', 'cantidad_titulos'], dtype={'actor': str, 'cantidad_titulos': int})
        dfs.append(df)

if dfs:
    df_final = pd.concat(dfs, ignore_index=True)
    # Ordenar por cantidad descendente, luego nombre ascendente
    df_final = df_final.sort_values(by=['cantidad_titulos', 'actor'], ascending=[False, True])
    df_final.to_csv('mapreduce_actores.csv', index=False, encoding='utf-8')
    print("=== TABLA 2: RESULTADO DE MAPREDUCE (TOP 10) ===")
    print(df_final.head(10).to_string(index=False))