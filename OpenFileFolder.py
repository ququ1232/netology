import sublime
import os
import sublime_plugin

class OpenFileFolderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name=self.view.file_name()
        if file_name is None:
          pass
        else:
          path=file_name.split("\\")
          current_driver=path[0]
          path.pop()
          current_directory="\\".join(path)
          command= "cd "+current_directory+" & "+current_driver+" & start ."
          os.system(command)
