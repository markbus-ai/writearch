"""
Quick Capture - UI component for instant note creation
"""
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

class QuickCapture:
    """Quick capture dialog for instant note creation"""

    def __init__(self, app):
        self.app = app
        self.window = None
        self.templates = self._get_smart_templates()

    def _get_smart_templates(self):
        """Get smart templates based on context"""
        return {
            'meeting': "# Meeting Notes\n\n**Attendees:**\n- \n\n**Agenda:**\n- \n\n**Action Items:**\n- \n\n**Decisions:**\n- \n\n**Next Steps:**\n- \n\n",
            'project': "# Project Plan\n\n**Objective:**\n\n**Scope:**\n\n**Timeline:**\n\n**Resources:**\n- \n\n**Risks:**\n- \n\n**Milestones:**\n- \n\n",
            'research': "# Research Notes\n\n**Topic:**\n\n**Sources:**\n- \n\n**Key Findings:**\n- \n\n**Questions:**\n- \n\n**Conclusions:**\n\n",
            'code_review': "# Code Review\n\n**Files Reviewed:**\n- \n\n**Issues Found:**\n- \n\n**Suggestions:**\n- \n\n**Approved:** Yes/No\n\n",
            'idea': "# Idea\n\n**What:**\n\n**Why:**\n\n**How:**\n\n**Next Steps:**\n\n",
            'bug': "# Bug Report\n\n**Description:**\n\n**Steps to Reproduce:**\n1. \n\n**Expected Result:**\n\n**Actual Result:**\n\n**Environment:**\n\n",
            'todo': "# TODO\n\n**Tasks:**\n- [ ] \n- [ ] \n- [ ] \n\n**Priority:** High/Medium/Low\n\n**Deadline:**\n\n"
        }

    def show_capture_dialog(self, template_type=None):
        """Show the quick capture dialog"""
        self.window = Gtk.Window()
        self.window.set_title("Quick Capture")
        self.window.set_default_size(600, 400)
        self.window.set_modal(True)
        self.window.set_transient_for(self.app.main_window)

        # Main box
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_start(20)
        box.set_margin_end(20)
        box.set_margin_top(20)
        box.set_margin_bottom(20)

        # Template selector
        template_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        template_label = Gtk.Label(label="Template:")
        template_combo = Gtk.ComboBoxText()

        for template_name in self.templates.keys():
            template_combo.append_text(template_name)

        template_combo.set_active(0 if not template_type else list(self.templates.keys()).index(template_type) if template_type in self.templates else 0)
        template_combo.connect('changed', self._on_template_changed)

        template_box.append(template_label)
        template_box.append(template_combo)
        box.append(template_box)

        # Title entry
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        title_label = Gtk.Label(label="Title:")
        self.title_entry = Gtk.Entry()
        self.title_entry.set_placeholder_text("Enter note title...")
        title_box.append(title_label)
        title_box.append(self.title_entry)
        box.append(title_box)

        # Text view
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        self.capture_text = Gtk.TextView()
        self.capture_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.capture_text.set_margin_start(10)
        self.capture_text.set_margin_end(10)
        self.capture_text.set_margin_top(10)
        self.capture_text.set_margin_bottom(10)

        # CSS for monospace font
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"textview { font-family: monospace; font-size: 11pt; }")
        self.capture_text.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        scrolled.set_child(self.capture_text)
        box.append(scrolled)

        # Buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.END)

        save_button = Gtk.Button(label="Save")
        save_button.get_style_context().add_class("suggested-action")
        save_button.connect('clicked', self._on_save_clicked)

        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect('clicked', lambda b: self.window.destroy())

        button_box.append(cancel_button)
        button_box.append(save_button)
        box.append(button_box)

        self.window.set_child(box)

        # Set initial template
        self._set_template(template_combo.get_active_text())

        # Setup keyboard shortcuts
        controller = Gtk.ShortcutController()
        self.window.add_controller(controller)

        # Ctrl+Enter to save
        shortcut = Gtk.Shortcut()
        shortcut.set_trigger(Gtk.ShortcutTrigger.parse_string('<Control>Return'))
        shortcut.set_action(Gtk.CallbackAction.new(lambda w, a: self._on_save_clicked(None)))
        controller.add_shortcut(shortcut)

        # Escape to cancel
        shortcut = Gtk.Shortcut()
        shortcut.set_trigger(Gtk.ShortcutTrigger.parse_string('Escape'))
        shortcut.set_action(Gtk.CallbackAction.new(lambda w, a: self.window.destroy()))
        controller.add_shortcut(shortcut)

        self.window.present()

    def _on_template_changed(self, combo):
        """Handle template selection change"""
        template_name = combo.get_active_text()
        self._set_template(template_name)

    def _set_template(self, template_name):
        """Set the template content"""
        if template_name in self.templates:
            content = self.templates[template_name]
            self.capture_text.get_buffer().set_text(content)

            # Suggest title based on template
            if not self.title_entry.get_text():
                self.title_entry.set_text(f"{template_name.title()} Notes")

    def _on_save_clicked(self, button):
        """Handle save button click"""
        title = self.title_entry.get_text().strip()
        if not title:
            title = "Untitled Note"

        buffer = self.capture_text.get_buffer()
        start, end = buffer.get_bounds()
        content = buffer.get_text(start, end, False)

        # Create filename from title
        filename = self._sanitize_filename(title) + ".md"

        # Save the file
        self.app.file_manager.save_file(filename, content)

        self.window.destroy()

    def _sanitize_filename(self, filename):
        """Sanitize filename to be filesystem-safe"""
        import re
        # Replace invalid characters with underscores
        return re.sub(r'[<>:"/\\|?*]', '_', filename).strip()

    def capture_with_context(self, context_type=None, context_value=None):
        """Capture with context awareness"""
        template_type = None

        # Suggest template based on context
        if context_type == 'time':
            if context_value == 'morning':
                template_type = 'todo'
            elif context_value == 'afternoon':
                template_type = 'meeting'
        elif context_type == 'application':
            if 'code' in context_value.lower():
                template_type = 'code_review'
            elif 'firefox' in context_value.lower():
                template_type = 'research'

        self.show_capture_dialog(template_type)