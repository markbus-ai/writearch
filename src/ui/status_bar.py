"""
Status Bar - UI component for displaying application status
"""
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class StatusBar(Gtk.Label):
    """Status bar widget for displaying statistics and file info"""

    def __init__(self):
        super().__init__()
        self.set_halign(Gtk.Align.START)
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(5)
        self.set_margin_bottom(5)
        self.update({}, None)

    def update(self, stats, filename=None):
        """Update status bar with new statistics and filename"""
        lines = stats.get('lines', 0)
        words = stats.get('words', 0)
        chars = stats.get('chars', 0)

        status = f"Líneas: {lines} | Palabras: {words} | Caracteres: {chars}"
        if filename:
            status += f" | {filename}"

        self.set_text(status)