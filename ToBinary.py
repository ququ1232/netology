import sublime
import os, re
# import sys
# sys.path.insert(0, 'D:\\Users\\nikolaev_v\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\')
import pyperclip
import sublime_plugin

class ToBinaryCommand(sublime_plugin.TextCommand):
    def hide_popup(self):
      self.view.window().run_command('hide_popup')

    def navigate(self, href):
      pyperclip.copy(href)
      self.hide_popup()

    def run(self, edit):
      view=self.view;
      content = ''

      word = view.substr(view.sel()[-1])

      if re.match("^$",word):
        view.window().run_command('find_under_expand')
        word = view.substr(view.sel()[-1])

      if re.search("[. ]",word):
        word = re.sub('[. ]','',word)

      if re.match("^$",word):
        content += 'empty selection<br>'
      elif re.search("[^0-9A-F]",word):
        content += 'only 0123456789ABCDEF accepted<br>'
      else:
        # content += '--7654 3210<br>'
        odd = 1
        for letter in word :
          content = content + (str(odd/2+.5)[:1] if odd % 2 else '')
          content = content + ' ' + bin(int(letter, 16))[2:].zfill(4) 
          odd += 1
          content += '<br>' if odd % 2 else ''
          if odd > 20:
            content += '<br> too much symbols'
            break

      link = '<a href="' + re.sub('<br>','\n',content) + '">copy me</a>'
      content += link
      view.show_popup(content, on_navigate=self.navigate)
          
    def done(self):
      pass