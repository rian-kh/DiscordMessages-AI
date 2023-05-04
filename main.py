
# Code adapted from:
# Threaded tasks: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Multithreaded_Long_Tasks.py
# Run other python scripts: https://stackoverflow.com/questions/57200315/connect-process-a-script-to-pysimplegui-button/57228060#57228060

import subprocess
import sys
import PySimpleGUI as sg
import signal
import generateData


# This function does the actual "running" of the command.  Also watches for any output. If found output is printed
def runCommand(cmd, window):
    global p
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None


trainTab = [
            [sg.Text('Enter path to Discord package (.zip): ')],
            [sg.Input(key='_zippath_')],  # Replace with drag and drop
            [sg.Button('Generate dataset')],
            [sg.Canvas()], # Figure out how to add space between
            [sg.Canvas()],
            [sg.Text("Model training settings (can leave default)")],
            [sg.Column([[sg.Text("1")], [sg.Text("2")], [sg.Text("3")]], element_justification="right", expand_x=True)],
            [
                sg.Text("Model size: "),
                sg.Combo(["124M (Small)", "355M (Medium)", "774M (Large)"], key='_modelsize_', readonly=True, default_value="124M (Small)")
            ],
            [
                sg.Text("Steps: "),
                sg.Input(key='_steps_', default_text='200', size=(10,10))
            ],
            [
                sg.Text("Learning rate (0.0000 - 1.0000):"),
                sg.Input(key='_learningrate_', default_text='0.0001', size=(10,10))
            ],
            [
                sg.Text("Generate sample after # of steps: "),
                sg.Input(key='_sampleevery_', default_text='100', size=(10,10))
            ],
            [
                sg.Text("Sample length (characters): "),
                sg.Input(key='_samplelength_', default_text='1024', size=(10,10))
            ],
            [
                sg.Text("Batch size: "),
                sg.Input(key='_batchsize_', default_text='1', size=(10,10))
            ],
            [sg.Canvas()],
            [sg.Canvas()],
            [sg.Output(size=(60,15), key='_output_')], # Can't block user input?
            [sg.Button('Start training'), sg.Button('Stop training')]
           ]




testTab = [[sg.Text("hi")]]
layout = [
            [sg.TabGroup([[
                sg.Tab("Generate/Train", trainTab),
                sg.Tab("Test model", testTab)
            ]])]

         ]


window = sg.Window('Discord Messages to AI', layout, size=(700,700))

trainingStarted = False
# Event loop
while True:
    event, values = window.Read()

    if event in (None, "Exit"):
        exit
        break

    if event == 'Start training':
        window.find_element('_output_').Update('')
        trainingStarted = True

        args = "\"" + values['_modelsize_'] + "\"" + " " + values['_steps_'] + " " + values['_learningrate_'] +\
               " " + values['_sampleevery_'] + " " + values['_samplelength_'] + " " + values['_batchsize_']


        window.start_thread(lambda: runCommand(cmd="python trainGPT2.py " + args, window=window), ('', ''))


    if event == 'Stop training' and trainingStarted:
        p.send_signal(signal.SIGINT)


    if event == 'Generate dataset':
        try:
            generateData.generateDataset(values['_zippath_'])
            sg.popup("Dataset generated successfully.", title="Success")
        except:
            sg.popup("Error: Invalid package path.", title="Error")

window.Close()




