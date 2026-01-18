# Maintainer: Markbusking <markbustos1912@gmail>
pkgname=notas
pkgver=1.0.0
pkgrel=1
pkgdesc="Aplicación simple y moderna de notas con GTK4"
arch=('any')
url="https://github.com/tuusuario/notas"
license=('MIT')
depends=('python' 'gtk4' 'libadwaita' 'python-gobject' 'gtksourceview5' 'gspell' 'python-markdown')
makedepends=()
source=("notas.desktop"
         "dev.writearch.Notas.metainfo.xml"
         "dev.writearch.Notas.gschema.xml")
sha256sums=('SKIP' 'SKIP' 'SKIP')

package() {
    # Instalar el ejecutable principal
    install -Dm755 "${srcdir}/notas.py" "${pkgdir}/usr/bin/notas"

    # Instalar archivo .desktop
    install -Dm644 "${srcdir}/notas.desktop" \
        "${pkgdir}/usr/share/applications/notas.desktop"

    # Instalar metainfo
    install -Dm644 "${srcdir}/dev.writearch.Notas.metainfo.xml" \
        "${pkgdir}/usr/share/metainfo/dev.writearch.Notas.metainfo.xml"

    # Instalar schema de GSettings
    install -Dm644 "${srcdir}/dev.writearch.Notas.gschema.xml" \
        "${pkgdir}/usr/share/glib-2.0/schemas/dev.writearch.Notas.gschema.xml"

    # Instalar módulos Python
    install -Dm755 "${srcdir}/notas.py" "${pkgdir}/usr/share/notas/notas.py"
    install -Dm644 "${srcdir}/core/__init__.py" "${pkgdir}/usr/share/notas/core/__init__.py"
    install -Dm644 "${srcdir}/core/file_manager.py" "${pkgdir}/usr/share/notas/core/file_manager.py"
    install -Dm644 "${srcdir}/core/text_processor.py" "${pkgdir}/usr/share/notas/core/text_processor.py"
    install -Dm644 "${srcdir}/core/context_manager.py" "${pkgdir}/usr/share/notas/core/context_manager.py"
    install -Dm644 "${srcdir}/ui/__init__.py" "${pkgdir}/usr/share/notas/ui/__init__.py"
    install -Dm644 "${srcdir}/ui/main_window.py" "${pkgdir}/usr/share/notas/ui/main_window.py"
    install -Dm644 "${srcdir}/ui/status_bar.py" "${pkgdir}/usr/share/notas/ui/status_bar.py"
    install -Dm644 "${srcdir}/ui/file_dialogs.py" "${pkgdir}/usr/share/notas/ui/file_dialogs.py"
    install -Dm644 "${srcdir}/ui/quick_capture.py" "${pkgdir}/usr/share/notas/ui/quick_capture.py"

    # Instalar código fuente en /usr/share/notas
    install -Dm755 "${srcdir}/../src/notas.py" "${pkgdir}/usr/share/notas/notas.py"
}