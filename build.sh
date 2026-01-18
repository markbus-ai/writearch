#!/bin/bash
set -e

APP_NAME="notas"
VERSION="1.0.0"

echo "🔨 Construyendo paquete para Arch..."
makepkg -f

echo "✅ Paquete .pkg.tar.zst generado."

echo "💻 Creando build de Windows..."
rm -rf dist/ build/
pyinstaller --noconfirm \
    --onefile \
    --name="${APP_NAME}" \
    --hidden-import=gi \
    --hidden-import=gi.repository \
    --hidden-import=gi.repository.Gtk \
    --hidden-import=gi.repository.Adw \
    --hidden-import=gi.repository.Gio \
    --hidden-import=gi.repository.GLib \
    --add-data "notas.desktop:." \
    --add-data "dev.writearch.Notas.metainfo.xml:." \
    notas.py

echo "✅ Ejecutable generado en dist/${APP_NAME}.exe"

