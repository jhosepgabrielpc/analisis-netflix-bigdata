import pandas as pd
import numpy as np

# 1. Leer el archivo original
df = pd.read_csv('netflix_titles.csv')
initial_rows, initial_cols = df.shape

# 2. Eliminar espacios al inicio y al final de los campos de texto
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].astype(str).str.strip()
    # Revertir los 'nan' generados por la conversión de nulos a string
    df[col] = df[col].replace('nan', np.nan)

# 3. Sustituir saltos de línea y tabulaciones por espacios
df = df.replace(to_replace=[r'\n', r'\t'], value=' ', regex=True)

# 4. Convertir textos vacíos en valores nulos
df = df.replace(r'^\s*$', np.nan, regex=True)

# 5. Eliminar filas completamente duplicadas
rows_before = len(df)
df = df.drop_duplicates()
duplicadas_eliminadas = rows_before - len(df)

# 6. Eliminar registros sin show_id
rows_before = len(df)
df = df.dropna(subset=['show_id'])
sin_show_id_eliminadas = rows_before - len(df)

# 7. Eliminar registros con show_id repetido (conservando la primera aparición)
rows_before = len(df)
df = df.drop_duplicates(subset=['show_id'], keep='first')
show_id_repetidos_eliminados = rows_before - len(df)

# 8. Convertir date_added al formato dd/mm/aaaa
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce').dt.strftime('%d/%m/%Y')

# 9. Crear duration_min (solo para Movies, entero que admite nulos)
df['duration_min'] = pd.NA
movies_mask = df['type'] == 'Movie'
# Extraer solo los números de la columna duration
df.loc[movies_mask, 'duration_min'] = df.loc[movies_mask, 'duration'].str.extract(r'(\d+)')[0]
# Convertir a Int64 de Pandas (entero que soporta nulos)
df['duration_min'] = df['duration_min'].astype('Int64')

# 10. Guardar netflix_clean.csv (UTF-8, con cabecera, separado por comas, sin índice)
df.to_csv('netflix_clean.csv', encoding='utf-8', index=False)

# 11. Cálculos para la Tabla 1
registros_finales = len(df)
peliculas_con_duracion = df[(df['type'] == 'Movie') & (df['duration_min'] > 0)].shape[0]
peliculas_sin_duracion = df[(df['type'] == 'Movie') & (df['duration_min'].isna() | (df['duration_min'] <= 0))].shape[0]

# 12. Mostrar en pantalla los resultados para llenar la tabla
print("=== TABLA 1: RESULTADO DE LA LIMPIEZA ===")
print(f"Registros del archivo original, sin cabecera: {initial_rows}")
print(f"Columnas del archivo original: {initial_cols}")
print(f"Filas completamente duplicadas eliminadas: {duplicadas_eliminadas}")
print(f"Registros sin show_id eliminados después de retirar duplicados: {sin_show_id_eliminadas}")
print(f"Registros con show_id repetido eliminados posteriormente: {show_id_repetidos_eliminados}")
print(f"Registros del archivo limpio: {registros_finales}")
print(f"Películas con duration_min numérica mayor que cero: {peliculas_con_duracion}")
print(f"Películas sin una duración numérica mayor que cero: {peliculas_sin_duracion}")