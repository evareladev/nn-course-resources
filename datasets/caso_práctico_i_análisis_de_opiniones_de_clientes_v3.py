# Importando librerías
import pandas as pd
import re
from textblob import TextBlob

# Copiamos el dataset de entrada a un DataFrame de trabajo
df = dataset.copy()

# Analizando columnas categóricas nominales
columnas = ['Division Name', 'Department Name', 'Class Name']

# Asegurarte de que las columnas existan (en caso de que no todas estén en dataset)
for col in columnas:
    if col not in df.columns:
        df[col] = 'Unknown'

# Rellenando valores nulos con una categoría especial
df[columnas] = df[columnas].fillna('Unknown')

# Convertir a tipo categórico
for col in columnas:
    df[col] = df[col].astype('category')

# Rellenando valores nulos en la columna Title
if 'Title' in df.columns and 'Class Name' in df.columns:
    df['Title'] = df['Title'].fillna(df['Class Name'])

# Tratando los valores nulos en la columna "Review Text"
if 'Review Text' in df.columns:
    df = df.dropna(subset=['Review Text'])

# ---------------------------------------------------------
# Tarea 1: Clasificación del ajuste (Fit_Feedback)
# ---------------------------------------------------------
def categorize_fit(text):
    if not isinstance(text, str):
        return 'No Info'
    text = text.lower()
    if re.search(r'runs large|too big|size down', text):
        return 'Grande'
    if re.search(r'runs small|too tight|size up', text):
        return 'Pequeño'
    if re.search(r'true to size|perfect fit', text):
        return 'Perfecto'
    return 'No Info'

df['Fit_Feedback'] = df['Review Text'].apply(categorize_fit)

# ---------------------------------------------------------
# Tarea 2: Análisis de Sentimiento (Feeling)
# ---------------------------------------------------------
def get_feeling(text):
    if not isinstance(text, str):
        return 'Neutral'
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return 'Positivo'
    elif polarity < -0.1:
        return 'Negativo'
    else:
        return 'Neutral'

df['Feeling'] = df['Review Text'].apply(get_feeling)

# Devuelve el DataFrame final a Power BI
dataset = df
del df
dataset