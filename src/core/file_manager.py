"""
File Manager - Core component for file operations
"""
import os
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import GObject

class FileManager(GObject.Object):
    """Manages file operations with event-driven architecture"""

    __gsignals__ = {
        'file_loaded': (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
        'file_saved': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        'file_error': (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }

    def __init__(self):
        super().__init__()
        self.current_file = None
        self.notes_dir = os.path.expanduser('~/Notas')

        # Create notes directory if it doesn't exist
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)

    def load_file(self, filename):
        """Load file content"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.current_file = filename
            self.emit('file_loaded', filename, content)
        except Exception as e:
            self.emit('file_error', f"Error al cargar archivo: {e}")

    def save_file(self, filename, content=""):
        """Save content to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            self.current_file = filename
            self.emit('file_saved', filename)
        except Exception as e:
            self.emit('file_error', f"Error al guardar archivo: {e}")

    def get_notes_dir(self):
        """Get the default notes directory"""
        return self.notes_dir