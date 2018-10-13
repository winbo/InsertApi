import sublime, sublime_plugin
from ..insert_api import ParseHeaderFile
from ..insert_api import apis
from ..insert_api import snips
from ..insert_api import settings

class InsertApiTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("start InsertApi Testing...")        
        expect_apis  = []
        expect_snips = []
        settings['show_macro_function'] = True
        succeeded = True

        hfile = sublime.packages_path() + "/InsertApi/Test/c.h"
        rfile = sublime.packages_path() + "/InsertApi/Test/c.h.expect"
        apis.clear()
        snips.clear()
        ParseHeaderFile(hfile, "[Test] c.h")

        with open(rfile, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break;
                expect_apis.append([line.strip(), "[Test] c.h"])
                line = f.readline()
                if not line:
                    break;
                expect_snips.append(line.strip())

        if len(expect_apis) != len(expect_snips):
            succeeded = False
            print("expect results not correct, length of apis and snips not match,"
                "apis: %d, snips: %d." % (len(expect_apis), len(expect_snips)))

        if len(snips) != len(expect_snips):
            succeeded = False
            print("length of snips not match, expect: %d, actually: %d." 
                % (len(expect_snips), len(snips)))

        if len(apis) != len(expect_apis):
            succeeded = False
            print("length of apis not match, expect: %d, actually: %d"
                % (len(expect_apis), len(apis)))

        for i in range(0, len(apis)):
            if apis[i][0] != expect_apis[i][0]:
                succeeded = False
                print("api index %d not match\n\texpect: %s\n\tactually: %s" 
                    % (i, expect_apis[i][0], apis[i][0]))
            if snips[i] != expect_snips[i]:
                succeeded = False
                print("snip index %d not match\n\texpect: %s\n\tactually: %s"
                    %(i, expect_snips[i], snips[i]))
        if succeeded:
            print("Pass\n")
        else:
            print("Fail\n")

        
