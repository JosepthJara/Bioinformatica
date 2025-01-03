# -*- coding: utf-8 -*-
"""codigo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gfNWqF_oTgK6WusiZLI7QSBPEKMm_MXr
"""

pip install -r requirements.txt

# Importación de bibliotecas
import streamlit as st
from Bio.Seq import Seq
from Bio.SeqUtils import seq3

# Función para procesar secuencias de ADN/ARN
def analyze_dna(sequence):
    sequence = Seq(sequence.strip().upper())
    if not all(base in "ACGTU" for base in sequence):
        return Markdown("**Error:** La secuencia contiene caracteres no válidos. Solo se permiten A, C, G, T, U.")

    length = len(sequence)
    gc_content = 100 * (sequence.count("G") + sequence.count("C")) / length
    complement = sequence.complement()
    transcribed = sequence.transcribe() if "T" in sequence else "No aplica (ARN)"

    return Markdown(f"""
    ### Resultados del análisis de ADN/ARN:
    - **Longitud de la secuencia:** {length} bases
    - **Contenido GC:** {gc_content:.2f}%
    - **Complemento:** {complement}
    - **Transcripción:** {transcribed}
    """)

# Función para procesar secuencias de proteínas
def analyze_protein(sequence):
    sequence = Seq(sequence.strip().upper())
    if not all(residue in "ACDEFGHIKLMNPQRSTVWY" for residue in sequence):
        return Markdown("**Error:** La secuencia contiene caracteres no válidos. Usa el formato de una letra para aminoácidos.")

    length = len(sequence)
    hydrophobic = sum(sequence.count(res) for res in "AILMFWV")
    hydrophilic = sum(sequence.count(res) for res in "RNDQEGKH")
    seq_three_letter = seq3(str(sequence))

    return Markdown(f"""
    ### Resultados del análisis de proteínas:
    - **Longitud de la secuencia:** {length} aminoácidos
    - **Residuos hidrofóbicos:** {hydrophobic} ({100 * hydrophobic / length:.2f}%)
    - **Residuos hidrofílicos:** {hydrophilic} ({100 * hydrophilic / length:.2f}%)
    - **Secuencia en formato de tres letras:** {seq_three_letter}
    """)

# Widgets interactivos
analysis_type = widgets.ToggleButtons(
    options=["Análisis de ADN/ARN", "Análisis de Proteínas"],
    description="Tipo:",
    style={"description_width": "initial"}
)
sequence_input = widgets.Textarea(
    value="",
    placeholder="Introduce la secuencia aquí...",
    description="Secuencia:",
    layout=widgets.Layout(width="100%", height="100px")
)
output = widgets.Output()

# Función para actualizar los resultados
def update_analysis(change):
    with output:
        output.clear_output()
        if analysis_type.value == "Análisis de ADN/ARN":
            display(analyze_dna(sequence_input.value))
        else:
            display(analyze_protein(sequence_input.value))

# Configurar eventos
sequence_input.observe(update_analysis, names="value")
analysis_type.observe(update_analysis, names="value")

# Mostrar widgets
display(analysis_type, sequence_input, output)
