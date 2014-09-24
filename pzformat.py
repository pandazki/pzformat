import sublime, sublime_plugin
import functools

class PzformatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # load setting
        settings = sublime.load_settings('pzformat.sublime-settings')
        saparator = settings.get('saparator')
        if not saparator:
            saparator = [",", "，", ";"]
        
        # split all regions into lines
        lineregions = []
        [lineregions.extend(self.view.split_by_newlines(x)) for x in self.view.sel()]
        
        # reverse process all line regions
        [self.process(edit, sublime.get_clipboard(), saparator, r) for r in lineregions[::-1]]
        
        # clear all selection
        self.view.sel().clear()

    def process(self, edit, formatstr, saparator, region):
        s = self.view.substr(region)
        for x in saparator:
            s = s.replace(x,' ')
        if len(s) == 0:
            return
        self.view.replace(edit, region, formatstr.format(*(s.split())))