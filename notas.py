#!/usr/bin/env python3
"""
Aplicación de notas simple con GTK4 - Primera Versión
"""
import sys
import os
import gi

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, Gio, GLib, Gdk

# Asegurar que podemos importar módulos locales
sys.path.insert(0, os.path.dirname(__file__))
from core.file_manager import FileManager
from core.text_processor import TextProcessor
from core.context_manager import ContextManager
from ui.main_window import MainWindow
from ui.status_bar import StatusBar
from ui.file_dialogs import FileDialogs
from ui.quick_capture import QuickCapture

class NotasApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='dev.writearch.Notas')

        # Core components
        self.file_manager = FileManager()
        self.text_processor = TextProcessor()
        self.context_manager = ContextManager()
        self.file_dialogs = FileDialogs(self.file_manager.get_notes_dir())
        self.quick_capture = QuickCapture(self)

        # GSettings
        try:
            self.settings = Gio.Settings.new('dev.writearch.Notas')
        except Exception:
            self.settings = None

        # UI components
        self.main_window = None
        self.status_bar = None

    def do_activate(self):
        """Activate the application"""
        self.main_window = MainWindow(self)
        self.main_window.present()

        # Initialize status bar
        self.status_bar = StatusBar()
        self.main_window.set_status_bar(self.status_bar)

        # Connect core components
        self._connect_components()

    def _connect_components(self):
        """Connect all components together"""
        # File manager events
        self.file_manager.connect('file_loaded', self.on_file_loaded)
        self.file_manager.connect('file_saved', self.on_file_saved)
        self.file_manager.connect('file_error', self.on_file_error)

        # Text processor events
        self.text_processor.connect('text_changed', self.on_text_changed)

        # Context manager events
        self.context_manager.connect('note_suggestion', self.on_note_suggestion)

        # Setup actions
        self._setup_actions()

        # Load settings
        self._load_settings()

    def _setup_actions(self):
        """Setup menu actions"""
        # File actions
        new_action = Gio.SimpleAction.new('new', None)
        new_action.connect('activate', lambda a, p: self.on_new_file())
        self.add_action(new_action)

        open_action = Gio.SimpleAction.new('open', None)
        open_action.connect('activate', lambda a, p: self.on_open_file())
        self.add_action(open_action)

        save_action = Gio.SimpleAction.new('save', None)
        save_action.connect('activate', lambda a, p: self.on_save_file())
        self.add_action(save_action)

        save_as_action = Gio.SimpleAction.new('save-as', None)
        save_as_action.connect('activate', lambda a, p: self.on_save_as_clicked())
        self.add_action(save_as_action)

        # Edit actions
        search_action = Gio.SimpleAction.new('search', None)
        search_action.connect('activate', lambda a, p: self.on_search())
        self.add_action(search_action)

        term_action = Gio.SimpleAction.new('terminal-command', GLib.VariantType.new('s'))
        term_action.connect('activate', self.on_terminal_command_activate)
        self.add_action(term_action)

        # View actions
        dark_mode_action = Gio.SimpleAction.new_stateful('dark-mode', None, GLib.Variant.new_boolean(False))
        dark_mode_action.connect('change-state', self.on_dark_mode_changed)
        self.add_action(dark_mode_action)

        markdown_action = Gio.SimpleAction.new_stateful('markdown-preview', None, GLib.Variant.new_boolean(False))
        markdown_action.connect('change-state', self.on_markdown_preview_changed)
        self.add_action(markdown_action)

        # Quick capture actions
        quick_capture_action = Gio.SimpleAction.new('quick-capture', None)
        quick_capture_action.connect('activate', lambda a, p: self.quick_capture.show_capture_dialog())
        self.add_action(quick_capture_action)

        # Template-specific quick capture
        for template in ['meeting', 'project', 'research', 'idea', 'bug', 'todo']:
            action = Gio.SimpleAction.new(f'quick-{template}', None)
            action.connect('activate', lambda a, p, t=template: self.quick_capture.show_capture_dialog(t))
            self.add_action(action)

    def on_open_file(self):
        """Handle open file action"""
        def callback(filename):
            if filename:
                self.file_manager.load_file(filename)
        self.file_dialogs.open_file(callback)

    def on_save_file(self):
        """Handle save file action"""
        if self.file_manager.current_file:
            content = self.main_window.get_text()
            self.file_manager.save_file(self.file_manager.current_file, content)
        else:
            self.on_save_file_as()

    def on_save_file_as(self):
        """Handle save as action"""
        def callback(filename):
            if filename:
                content = self.main_window.get_text()
                self.file_manager.save_file(filename, content)
        self.file_dialogs.save_file(callback)

    def on_file_loaded(self, manager, filename, content):
        """Handle file loaded event"""
        self.main_window.set_text(content)
        self.main_window.set_title(f'Notas - {os.path.basename(filename)}')
        self.update_status()

    def on_file_saved(self, manager, filename):
        """Handle file saved event"""
        self.main_window.set_title(f'Notas - {os.path.basename(filename)}')
        self.update_status()

    def on_file_error(self, manager, error_msg):
        """Handle file error event"""
        self.file_dialogs.show_error(error_msg)

    def on_text_changed(self, processor, text):
        """Handle text changed event"""
        self.update_status()

    def update_status(self):
        """Update status bar with current statistics"""
        text = self.main_window.get_text()
        stats = self.text_processor.get_statistics(text)
        filename = os.path.basename(self.file_manager.current_file) if self.file_manager.current_file else None
        self.status_bar.update(stats, filename)

    def on_new_file(self):
        """Handle new file action"""
        self.main_window.set_text('')
        self.main_window.set_title('Notas')
        self.file_manager.current_file = None
        self.update_status()

    def on_save_as_clicked(self):
        """Handle save as action"""
        def callback(filename):
            if filename:
                content = self.main_window.get_text()
                self.file_manager.save_file(filename, content)
        self.file_dialogs.save_file(callback)

    def on_search(self):
        """Handle search action"""
        # Simple search implementation - could be enhanced
        pass

    def on_terminal_command_activate(self, action, parameter):
        """Handle terminal command action"""
        dialog = Gtk.Dialog(
            title='Ejecutar comando',
            transient_for=self.get_active_window(),
            modal=True
        )
        dialog.add_buttons(
            'Cancelar', Gtk.ResponseType.CANCEL,
            'Ejecutar', Gtk.ResponseType.OK
        )

        entry = Gtk.Entry()
        entry.set_placeholder_text('Ingrese comando de terminal...')
        entry.set_margin_start(10)
        entry.set_margin_end(10)
        entry.set_margin_top(10)
        entry.set_margin_bottom(10)

        content_area = dialog.get_content_area()
        content_area.append(entry)

        def on_response(dialog, response_id):
            if response_id == Gtk.ResponseType.OK:
                command = entry.get_text().strip()
                if command:
                    self.execute_terminal_command(command)
            dialog.destroy()

        dialog.connect('response', on_response)
        dialog.present()

    def execute_terminal_command(self, command):
        """Execute terminal command"""
        try:
            proc = Gio.Subprocess.new(
                ['bash', '-c', command],
                Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE
            )
            proc.wait_check_async(None, self.on_command_finished, command)
        except Exception as e:
            self.show_notification(f"Error ejecutando comando: {e}")

    def on_command_finished(self, proc, result, command):
        """Handle command completion"""
        try:
            proc.wait_check_finish(result)
            self.show_notification(f"Comando ejecutado: {command}")
        except Exception as e:
            self.show_notification(f"Error en comando '{command}': {e}")

    def show_notification(self, message):
        """Show desktop notification"""
        notification = Gio.Notification.new("Notas")
        notification.set_body(message)
        self.send_notification(None, notification)

    def on_dark_mode_changed(self, action, value):
        """Handle dark mode toggle"""
        dark_mode = value.get_boolean()
        action.set_state(value)

        # Apply dark mode
        gtk_settings = Gtk.Settings.get_default()
        gtk_settings.set_property('gtk-application-prefer-dark-theme', dark_mode)

        # Save to GSettings
        if self.settings:
            self.settings.set_boolean('dark-mode', dark_mode)

    def on_markdown_preview_changed(self, action, value):
        """Handle markdown preview toggle"""
        preview_enabled = value.get_boolean()
        action.set_state(value)

        if preview_enabled:
            try:
                import markdown
                text = self.main_window.get_text()
                html = markdown.markdown(text)
                # For now, just show a notification with preview
                self.show_notification(f"Markdown preview: {html[:100]}...")
            except ImportError:
                self.show_notification("Markdown no disponible - instala python-markdown")
        else:
            self.show_notification("Vista previa Markdown desactivada")

    def on_note_suggestion(self, manager, title, content):
        """Handle note suggestions from context manager"""
        # Show a notification with the suggestion
        self.show_notification(f"Sugerencia: {title}")

        # Optionally, create the note automatically or ask user
        # For now, just show the suggestion

    def _load_settings(self):
        """Load application settings"""
        if self.settings:
            try:
                # Load dark mode setting
                dark_mode = self.settings.get_boolean('dark-mode')
                gtk_settings = Gtk.Settings.get_default()
                gtk_settings.set_property('gtk-application-prefer-dark-theme', dark_mode)

                # Update action state
                dark_action = self.lookup_action('dark-mode')
                if dark_action:
                    dark_action.set_state(GLib.Variant.new_boolean(dark_mode))
            except Exception as e:
                print(f"Error loading settings: {e}")

def main():
    app = NotasApp()
    return app.run(sys.argv)

if __name__ == '__main__':
    sys.exit(main())