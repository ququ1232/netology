import sublime
import os
import sublime_plugin
import re

class _ReopenWithEncodingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
      # print current encoding in concole
      encoding = self.view.encoding();
      print(encoding)
      # if current encoding 1251, then reopen with 866
      if encoding == "Cyrillic (Windows 1251)":
        print(1)
        self.view.run_command("reopen", {"encoding": "Cyrillic (Windows 866)"})
      # if current encoding  866, then reopen with 1251
      elif encoding == "Cyrillic (Windows 866)":
        print(2)
        self.view.run_command("reopen", {"encoding": "Cyrillic (Windows 1251)"})
      else:
      # else show popup encoding ... is not 866 either 1251
        self.view.show_popup(
          'Enc is not 866 or 1251', 
          on_hide=self.done)

    def done(self):
      pass