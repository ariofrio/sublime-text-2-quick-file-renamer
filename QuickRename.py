import os
import shutil
import sublime
import sublime_plugin


class QuickRenameCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        file_name = self.get_file_name(view)
        self.window.show_input_panel("Rename:", file_name, lambda s: self.rename(view, s), None, None)

    def get_file_name(self, view):
        return view.file_name().rsplit(os.sep, 1)[1]

    def rename(self, view, new_file):
        old_file = view.file_name()
        if old_file is None:
            print("ABORT: The file hasn't been saved to disk yet. Performing regular save instead of rename.")
            view.window().run_command("save")
            return
        old_file = old_file.rsplit(os.sep, 1)[1]
        if not self.validateFileName(view, old_file, new_file):
            return
        if view.is_dirty():
            view.window().run_command("save")
        window = view.window()
        self.fileOperations(window, old_file, new_file)
        self.setSelection(view, window.active_view())

    def validateFileName(self, view, old_file, new_file):
        if len(new_file) is 0:
            sublime.error_message("Error: No new filename given.")
            return False
        if view.is_loading():
            sublime.error_message("Error: The file is still loading.")
            return False
        if view.is_read_only():
            sublime.error_message("Error: The file is read-only.")
            return False
        if(new_file == old_file):
            sublime.error_message("Error: The new file name was the same as the old one.")
            return False
        return True

    def fileOperations(self, window, old_file, new_file):
        window.run_command("close")
        shutil.move(old_file, new_file)
        window.open_file(new_file)
        if old_file.endswith(".py"):
            os.remove(old_file + "c")

    def setSelection(self, old_view, new_view):
        new_view.sel().clear()
        new_view.sel().addAll(old_view.sel())
