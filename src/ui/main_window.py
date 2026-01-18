"""
Main Window - UI component for the main application window
"""
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, Gdk

class MainWindow(Gtk.ApplicationWindow):
    """Main application window"""

    def __init__(self, app):
        super().__init__(application=app)
        self.app = app

        self.set_title('Notas')
        self.set_default_size(800, 600)

        # UI components
        self.text_view = None
        self.text_buffer = None
        self.status_bar = None

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        """Build the user interface"""
        # Header bar
        header_bar = Gtk.HeaderBar()
        self.set_titlebar(header_bar)

        # Buttons
        open_button = Gtk.Button()
        open_button.set_icon_name('document-open-symbolic')
        open_button.set_tooltip_text('Abrir archivo (Ctrl+O)')
        open_button.connect('clicked', lambda b: self.app.on_open_file())
        header_bar.pack_start(open_button)

        save_button = Gtk.Button()
        save_button.set_icon_name('document-save-symbolic')
        save_button.set_tooltip_text('Guardar archivo (Ctrl+S)')
        save_button.connect('clicked', lambda b: self.app.on_save_file())
        header_bar.pack_start(save_button)

        # Menu button
        menu_button = self._create_menu_button()
        header_bar.pack_end(menu_button)

        # Text view
        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.set_margin_start(20)
        self.text_view.set_margin_end(20)
        self.text_view.set_margin_top(20)
        self.text_view.set_margin_bottom(20)

        # CSS for monospace font
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"textview { font-family: monospace; font-size: 11pt; }")
        self.text_view.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.text_buffer = self.text_view.get_buffer()

        # Scrolled window
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_child(self.text_view)
        scrolled_window.set_vexpand(True)

        # Main layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.main_box.append(scrolled_window)

        self.set_child(self.main_box)

        # Drag and drop
        self._setup_drag_and_drop()

        # Shortcuts
        self._setup_shortcuts()

    def _setup_drag_and_drop(self):
        """Setup drag and drop for files"""
        drop_target = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)
        drop_target.connect('drop', self._on_file_drop)
        self.text_view.add_controller(drop_target)

    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        controller = Gtk.ShortcutController()
        self.add_controller(controller)

        # Ctrl+O - Open
        shortcut = Gtk.Shortcut()
        shortcut.set_trigger(Gtk.ShortcutTrigger.parse_string('<Control>o'))
        shortcut.set_action(Gtk.CallbackAction.new(lambda w, a: self.app.on_open_file()))
        controller.add_shortcut(shortcut)

        # Ctrl+S - Save
        shortcut = Gtk.Shortcut()
        shortcut.set_trigger(Gtk.ShortcutTrigger.parse_string('<Control>s'))
        shortcut.set_action(Gtk.CallbackAction.new(lambda w, a: self.app.on_save_file()))
        controller.add_shortcut(shortcut)

        # Ctrl+Shift+N - Quick Capture
        shortcut = Gtk.Shortcut()
        shortcut.set_trigger(Gtk.ShortcutTrigger.parse_string('<Control><Shift>n'))
        shortcut.set_action(Gtk.CallbackAction.new(lambda w, a: self.app.quick_capture.show_capture_dialog()))
        controller.add_shortcut(shortcut)

    def _connect_signals(self):
        """Connect signals"""
        self.text_buffer.connect('changed', self._on_text_changed)

    def _on_text_changed(self, buffer):
        """Handle text changes"""
        start, end = buffer.get_bounds()
        text = buffer.get_text(start, end, False)
        self.app.on_text_changed(self.app.text_processor, text)

    def _on_file_drop(self, drop_target, value, x, y):
        """Handle file drops"""
        if isinstance(value, Gdk.FileList):
            files = value.get_files()
            for file in files:
                file_path = file.get_path()
                if file_path:
                    cursor_iter = self.text_buffer.get_iter_at_offset(
                        self.text_buffer.get_cursor_position()
                    )
                    self.text_buffer.insert(cursor_iter, f"{file_path}\n")
        return True

    def set_text(self, text):
        """Set text content"""
        self.text_buffer.set_text(text)

    def get_text(self):
        """Get current text content"""
        start, end = self.text_buffer.get_bounds()
        return self.text_buffer.get_text(start, end, False)

    def set_status_bar(self, status_bar):
        """Set the status bar component"""
        self.status_bar = status_bar
        self.main_box.append(status_bar)

    def _create_menu_button(self):
        """Create the menu button with advanced options"""
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name('open-menu-symbolic')

        # Create menu
        menu = Gio.Menu()

        # File submenu
        file_menu = Gio.Menu()
        file_menu.append('Nuevo', 'app.new')
        file_menu.append('Abrir', 'app.open')
        file_menu.append('Guardar', 'app.save')
        file_menu.append('Guardar como...', 'app.save-as')
        menu.append_submenu('Archivo', file_menu)

        # Edit submenu
        edit_menu = Gio.Menu()
        edit_menu.append('Buscar', 'app.search')
        edit_menu.append('Ejecutar comando...', 'app.terminal-command')

        # Quick capture submenu
        quick_menu = Gio.Menu()
        quick_menu.append('Captura Rápida', 'app.quick-capture')
        quick_menu.append('Reunión', 'app.quick-meeting')
        quick_menu.append('Proyecto', 'app.quick-project')
        quick_menu.append('Investigación', 'app.quick-research')
        quick_menu.append('Idea', 'app.quick-idea')
        quick_menu.append('Bug', 'app.quick-bug')
        quick_menu.append('TODO', 'app.quick-todo')
        edit_menu.append_submenu('Captura Rápida', quick_menu)

        menu.append_submenu('Editar', edit_menu)

        # View submenu
        view_menu = Gio.Menu()
        view_menu.append('Modo oscuro', 'app.dark-mode')
        view_menu.append('Vista previa Markdown', 'app.markdown-preview')
        menu.append_submenu('Ver', view_menu)

        menu_button.set_menu_model(menu)
        return menu_button