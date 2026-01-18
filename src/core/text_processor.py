"""
Text Processor - Core component for text processing and statistics
"""
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import GObject

class TextProcessor(GObject.Object):
    """Processes text content and provides statistics"""

    __gsignals__ = {
        'text_changed': (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }

    def __init__(self):
        super().__init__()

    def get_statistics(self, text):
        """Calculate text statistics"""
        if not text:
            return {'lines': 0, 'words': 0, 'chars': 0}

        lines = text.count('\n') + 1
        words = len(text.split()) if text.strip() else 0
        chars = len(text)

        return {
            'lines': lines,
            'words': words,
            'chars': chars
        }

    def process_text_change(self, text):
        """Process text changes and emit signal"""
        self.emit('text_changed', text)