import os
import subprocess
import sublime
import sublime_plugin

class ExtendScriptCommand(sublime_plugin.TextCommand):
    def active_view(self):
        return self.view
    def run_command(self, command):
        print('ExtendScript Command')
        s = sublime.load_settings("ExtendScript.sublime-settings")
        if s.get('save_first') and self.active_view() and self.active_view().is_dirty():
            self.active_view().run_command('save')
        msg = 'Execute '
        software_folder=""
        software_name=""
        script_folder=""

        if command[1] == 'ae':
            software_folder=s.get('AE_folder')
            software_folder += "\Support Files"
            script_folder= software_folder+"\Scripts"
            software_name="AfterFX"
        elif command[1] == 'ai':
            software_folder = s.get('AI_folder')
            script_folder = software_folder+"\Scripting"
            software_folder += "\Support Files\Contents\Windows"
            software_name = "Illustrator"
        elif command[1] == 'ps':
            software_folder=s.get('PS_folder')
            software_name="Photoshop"
            script_folder=software_folder+"\Presets\Scripts"

        script_folder+="\\"

        file_name = self.active_view().file_name()
        if s.get('coffee_mode'):
            if(file_name.split('.')[-1] == 'coffee'):
                file_name = file_name.split('.')[0]+'.js'
        msg+= ' Script: ' + file_name

        only_file_name = s.get('file_export_prefix') + file_name.split('\\')[len(file_name.split('\\'))-1]
        batch ='@echo'
        if s.get('copy_to_software_scripts'):
            batch+='& copy /D "' + file_name +'" "'+script_folder+only_file_name.split('.')[0]+'.jsx'+'"'
            batch+='& cd /D "' + software_folder+'"'
            batch+='& '+ software_name + ' -r "' + script_folder+only_file_name.split('.')[0]+'.jsx'+'"'
        else:
            batch+='& cd /D "' + software_folder+'"'
            batch+='& '+ software_name + ' -r "' + file_name +'"'
        # For debugging batch execution
        #batch+='& pause'

        os.system(batch)

class ExecuteAeScriptCommand(ExtendScriptCommand):
    def run(self, edit):
        command = ['extend_script', 'ae']
        self.run_command(command)

class ExecuteAiScriptCommand(ExtendScriptCommand):
    def run(self, edit):
        command = ['extend_script', 'ai']
        self.run_command(command)

class ExecutePsScriptCommand(ExtendScriptCommand):
    def run(self, edit):
        command = ['extend_script', 'ps']
        self.run_command(command)