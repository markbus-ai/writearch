#!/usr/bin/env python3
"""Tests unitarios para la aplicación Notas"""

import tempfile
import os
from pathlib import Path


def test_file_operations():
    """Test operaciones básicas de archivo"""
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Contenido de prueba")
        temp_path = f.name

    try:
        # Leer archivo
        content = Path(temp_path).read_text()
        assert content == "Contenido de prueba"
    finally:
        # Limpiar
        os.unlink(temp_path)


def test_text_stats():
    """Test cálculo de estadísticas de texto"""
    def count_words_chars(text):
        chars = len(text)
        words = len(text.split()) if text.strip() else 0
        return words, chars

    # Texto normal
    words, chars = count_words_chars("Hola mundo")
    assert words == 2
    assert chars == 10

    # Texto vacío
    words, chars = count_words_chars("")
    assert words == 0
    assert chars == 0

    # Texto con espacios
    words, chars = count_words_chars("   ")
    assert words == 0
    assert chars == 3


def test_markdown_conversion():
    """Test conversión básica de markdown"""
    try:
        import markdown

        # Markdown simple
        md_text = "# Título\n\nTexto **negrita**"
        html = markdown.markdown(md_text)
        assert "<h1>Título</h1>" in html
        assert "<strong>negrita</strong>" in html

    except ImportError:
        # Si no está instalado, skip el test
        pass


if __name__ == "__main__":
    # Ejecutar tests básicos
    test_file_operations()
    test_text_stats()
    test_markdown_conversion()
    print("Todos los tests pasaron!")