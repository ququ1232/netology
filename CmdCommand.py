import sublime
import os
import sublime_plugin

class CmdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # os.system("cd " + self.view.file_name() + " & start cmd")
        # todo: open FAR
        file_name=self.view.file_name()
        if file_name is None:
          os.system("cd D:\ & start cmd")
        else:
          path=file_name.split("\\")
          current_driver=path[0]
          path.pop()
          current_directory="\\".join(path)
          command= "cd "+current_directory+" & "+current_driver+" & start cmd"
          os.system(command)
