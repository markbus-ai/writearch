"""
Context Manager - Core component for context-aware functionality
"""
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import GObject, GLib

class ContextManager(GObject.Object):
    """Manages context-aware features like automatic note activation"""

    __gsignals__ = {
        'context_changed': (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
        'note_suggestion': (GObject.SignalFlags.RUN_FIRST, None, (str, str))
    }

    def __init__(self):
        super().__init__()
        self.current_context = {}
        self.context_hooks = {}

        # Initialize context monitoring
        self._setup_context_monitoring()

    def _setup_context_monitoring(self):
        """Setup monitoring of system context"""
        # Monitor active window/application
        self._monitor_active_window()

        # Monitor current working directory (for terminal integration)
        self._monitor_working_directory()

        # Monitor time-based context (morning routine, work hours, etc.)
        self._monitor_time_context()

    def _monitor_active_window(self):
        """Monitor which application window is currently active"""
        # This would use D-Bus or GTK APIs to track active windows
        # For now, we'll simulate with a timer
        GLib.timeout_add_seconds(5, self._check_active_window)

    def _monitor_working_directory(self):
        """Monitor current working directory for context"""
        # This would integrate with terminal/shell to know current dir
        pass

    def _monitor_time_context(self):
        """Monitor time-based context"""
        import datetime
        current_hour = datetime.datetime.now().hour

        if 6 <= current_hour < 12:
            context = "morning"
        elif 12 <= current_hour < 18:
            context = "afternoon"
        elif 18 <= current_hour < 22:
            context = "evening"
        else:
            context = "night"

        self.current_context['time'] = context
        self._trigger_context_hooks('time', context)

    def _check_active_window(self):
        """Check currently active window (simplified)"""
        # In a real implementation, this would use D-Bus or GTK APIs
        # For demo purposes, we'll just emit a generic context
        return True  # Continue timer

    def add_context_hook(self, context_type, condition, callback):
        """Add a hook that triggers based on context conditions"""
        if context_type not in self.context_hooks:
            self.context_hooks[context_type] = []

        self.context_hooks[context_type].append({
            'condition': condition,
            'callback': callback
        })

    def _trigger_context_hooks(self, context_type, value):
        """Trigger hooks for a specific context type"""
        if context_type in self.context_hooks:
            for hook in self.context_hooks[context_type]:
                if hook['condition'](value):
                    hook['callback'](context_type, value)

    def suggest_note(self, context_type, context_value):
        """Suggest a note based on current context"""
        # Simple suggestion logic - could be enhanced with AI
        suggestions = {
            'time': {
                'morning': 'Morning routine and tasks',
                'afternoon': 'Work progress and meetings',
                'evening': 'Evening reflection and planning',
                'night': 'Night thoughts and ideas'
            },
            'application': {
                'firefox': 'Web research and bookmarks',
                'code': 'Programming notes and code snippets',
                'terminal': 'Command history and system notes'
            }
        }

        if context_type in suggestions and context_value in suggestions[context_type]:
            title = suggestions[context_type][context_value]
            content = f"# {title}\n\nContext: {context_value}\n\n"
            self.emit('note_suggestion', title, content)

    def get_smart_templates(self):
        """Get smart templates based on context"""
        templates = {
            'meeting': "# Meeting Notes\n\n**Attendees:**\n- \n\n**Agenda:**\n- \n\n**Action Items:**\n- \n\n**Decisions:**\n- \n\n**Next Steps:**\n- \n\n",
            'project': "# Project Plan\n\n**Objective:**\n\n**Scope:**\n\n**Timeline:**\n\n**Resources:**\n- \n\n**Risks:**\n- \n\n**Milestones:**\n- \n\n",
            'research': "# Research Notes\n\n**Topic:**\n\n**Sources:**\n- \n\n**Key Findings:**\n- \n\n**Questions:**\n- \n\n**Conclusions:**\n\n",
            'code_review': "# Code Review\n\n**Files Reviewed:**\n- \n\n**Issues Found:**\n- \n\n**Suggestions:**\n- \n\n**Approved:** Yes/No\n\n"
        }
        return templates