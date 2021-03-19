import sublime
import os
import sublime_plugin
import re

class ToLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
      view = self.view

      # get buffer
      text = sublime.get_clipboard()
      
      # remove COMMIT; string
      text = re.sub('COMMIT;','',text)

      # remove leading spaces for each line
      lines = text.split('\n')
      lines = [ line.strip() for line in lines ]
      text = '\n'.join(lines)

      # make one line
      text = re.sub('\n','',text)

      # make one statement per one line
      text = re.sub('\);', ');\n',text)

      # additional spaces over Values string
      text = re.sub('Values', ' Values ',text)

      # set buffer
      sublime.set_clipboard(text)

      # Ctrl + V
      view.run_command("paste")

## what's going on here

# get buffer
# remove COMMIT; string
# remove leading spaces for each line
# make one line
# make one statement per one line
# additional spaces over Values string
# set buffer
# Ctrl + V