"""
File Dialogs - UI component for file operations dialogs
"""
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

class FileDialogs:
    """Handles file operation dialogs"""

    def __init__(self, notes_dir=None):
        self.notes_dir = notes_dir or "~/Notas"
        self._expand_notes_dir()

    def _expand_notes_dir(self):
        """Expand the notes directory path"""
        import os
        self.notes_dir = os.path.expanduser(self.notes_dir)

    def open_file(self, callback):
        """Show open file dialog"""
        dialog = Gtk.FileChooserDialog(
            title='Abrir archivo',
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            'Cancelar', Gtk.ResponseType.CANCEL,
            'Abrir', Gtk.ResponseType.ACCEPT
        )

        # Set default directory
        dialog.set_current_folder(Gio.File.new_for_path(self.notes_dir))

        def on_response(dialog, response):
            filename = None
            if response == Gtk.ResponseType.ACCEPT:
                filename = dialog.get_filename()
            dialog.destroy()
            callback(filename)

        dialog.connect('response', on_response)
        dialog.present()

    def save_file(self, callback):
        """Show save file dialog"""
        dialog = Gtk.FileChooserDialog(
            title='Guardar archivo',
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_buttons(
            'Cancelar', Gtk.ResponseType.CANCEL,
            'Guardar', Gtk.ResponseType.ACCEPT
        )

        # Set default directory
        dialog.set_current_folder(Gio.File.new_for_path(self.notes_dir))

        def on_response(dialog, response):
            filename = None
            if response == Gtk.ResponseType.ACCEPT:
                filename = dialog.get_filename()
            dialog.destroy()
            callback(filename)

        dialog.connect('response', on_response)
        dialog.present()

    def show_error(self, message):
        """Show error dialog"""
        dialog = Gtk.MessageDialog(
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )

        def on_response(dialog, response):
            dialog.destroy()

        dialog.connect('response', on_response)
        dialog.present()