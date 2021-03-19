import sublime
import os
import sublime_plugin
import re

class ChangeValekCommand(sublime_plugin.TextCommand):
    def run(self, edit):
      # print(self.view.settings().get('valek'))
      self.view.run_command("toggle_setting", {"setting": "valek"})
      # print(self.view.settings().get('valek'))