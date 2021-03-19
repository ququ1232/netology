import sublime
import sublime_plugin

items = [' (ESC) 0x[1B] 27','  (SO) 0x[0E] 14','  (SI) 0x[0F] 15','  (FF) 0x[0C] 12','   (FS) 0x[1C] 28','   (GS) 0x[1D] 29','  (VT) 0x[0B] 11', '   (DC1) 0x11','']

class UnicodeCharacterSelectCommand(sublime_plugin.TextCommand):
    def on_choice_symbol(self, symbol):
        self.view.run_command("insert", {"characters": items[symbol][0]})
        self.view.hide_popup()

    def run(self, edit):
        # self.view.show_popup_menu(items, on_select=self.on_choice_symbol)
        sublime.active_window().show_quick_panel(items, on_select=self.on_choice_symbol)

    def done(self):
      pass
