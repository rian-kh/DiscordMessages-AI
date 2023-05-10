# Code adapted from:
# Run other python scripts: https://stackoverflow.com/questions/57200315/connect-process-a-script-to-pysimplegui-button/57228060#57228060

import subprocess
import sys
import PySimpleGUI as sg
import signal
import threading
import generateData
import os
import shutil


# Function for running training
def runTraining(args, window):
    global p

    p = subprocess.Popen("python trainGPT2.py " + args, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                         shell=True)

    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None


# Function for running message generation
def runMessage(args, window):
    global q

    q = subprocess.Popen("python generateMessage.py " + args, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         shell=True)

    output = ''
    for line in q.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None


# Function for finding model steps
def findModelSteps():
    if not os.path.exists('checkpoint/run1'):
        return None
    else:
        for file in os.listdir('checkpoint/run1'):

            # Find model file and get steps
            if file.startswith('model') and file.endswith('.index'):
                return file.split('-')[1].split('.')[0]

        # Model folder exists, but no model is found.
        return None


# Layout tabs

testTab = [
    [sg.Text("Text generation settings (can leave default)", font=("Helvetica", 12, "bold"))],
    [
        sg.Column([
            [sg.Text("Prefix to start generation with (optional): ")],
            [sg.Text("Number of samples: ")],
            [sg.Text("Sample length (characters): ")],
            [sg.Text("Batch size: ")],
            [sg.Text("Temperature (0.0 - 1.0): ")],
            [sg.Text("Top K: ")],
            [sg.Text("Top P (0.0 - 1.0): ")]
        ]),

        sg.Column([
            [sg.Input(key='_genPrefix_', default_text='', size=(30, 10))],
            [sg.Input(key='_genSampleNum_', default_text='5', size=(10, 10))],
            [sg.Input(key='_genSampleLen_', default_text='100', size=(10, 10))],
            [sg.Input(key='_genBatchSize_', default_text='1', size=(10, 10))],
            [sg.Input(key='_genTemp_', default_text='0.7', size=(10, 10))],
            [sg.Input(key='_genTopK_', default_text='0', size=(10, 10))],
            [sg.Input(key='_genTopP_', default_text='0.0', size=(10, 10))]
        ])
    ],

    [sg.Button('Start text generation'), sg.Button('End text generation')]

]

trainTab = [
    [sg.Text('Enter path to Discord package (.zip): ')],
    [sg.Input(key='_zippath_'), sg.FileBrowse('Browse', key='_browseFile_')],
    [sg.Button('Generate dataset')],
    [sg.Canvas()],  # Figure out how to add space between
    [sg.Canvas()],
    [sg.Text("Model training settings (can leave default)", font=("Helvetica", 12, "bold"))],
    [
        sg.Column([
            [sg.Text("Model size: ")],
            [sg.Text("Steps: ")],
            [sg.Text("Learning rate (0.0 - 1.0):")],
            [sg.Text("Generate sample after # of steps: ")],
            [sg.Text("Batch size: ")]

        ]),

        sg.Column([
            [sg.Combo(["124M (Small)", "355M (Medium)", "774M (Large)"], key='_modelsize_', readonly=True,
                      default_value="124M (Small)")],
            [sg.Input(key='_steps_', default_text='200', size=(10, 10))],
            [sg.Input(key='_learningrate_', default_text='0.0001', size=(10, 10))],
            [sg.Input(key='_sampleevery_', default_text='100', size=(10, 10))],
            [sg.Input(key='_batchsize_', default_text='1', size=(10, 10))]
        ])

    ],
    [sg.Canvas()],
    [sg.Canvas()],

    [sg.Button('Start training'), sg.Button('Save and end training'), sg.Canvas(), sg.Canvas(),
     sg.Button('Delete model', button_color='red')]
]

# Check if dataset is already generated
if os.path.exists('data/data.txt'):
    trainTab[0] = [sg.Text('Enter path to Discord package (.zip): '), sg.Text('Dataset found.', key='_foundData_')]
else:
    trainTab[0] = [sg.Text('Enter path to Discord package (.zip): '), sg.Text('Dataset not found.', key='_foundData_')]

# Check if model is already generated
stepText = findModelSteps()
if stepText is None:
    trainTab[5].append(sg.Text("Model not found.", key='_modelFound_'))
    testTab[0].append(sg.Text("Model not found.", key='_modelFound2_'))
else:
    trainTab[5].append(sg.Text("Model found, steps: " + stepText, key='_modelFound_'))
    testTab[0].append(sg.Text("Model found, steps: " + stepText, key='_modelFound2_'))

layout = [
    [sg.TabGroup([[
        sg.Tab("Generate/Train", trainTab, key='_trainTab_'),
        sg.Tab("Test model", testTab, key='_testTab_')
    ]], key='_tabGroup_')],

    [sg.Output(size=(70, 20), font=('Arial', 18), key='_output_')]

]

window = sg.Window('Discord Messages to AI', layout, size=(700, 700))

trainingStarted = False
generationStarted = False

# Event loop
while True:
    event, values = window.Read()

    if event in (None, "Exit"):

        if trainingStarted:
            p.terminate()

        if generationStarted:
            q.terminate()

        exit
        break

    # Always check for model steps
    if not stepText == findModelSteps():
        stepText = findModelSteps()
        if stepText is None:
            window['_modelFound_'].update("Model not found.")
            window['_modelFound2_'].update("Model not found.")
            window.refresh()
        else:
            window['_modelFound_'].update("Model found, steps: " + stepText)
            window['_modelFound2_'].update("Model found, steps: " + stepText)
            window.refresh()

    # Clear output box when a button is pressed. I don't know why this works
    if values['_tabGroup_'] == '_testTab_' or values['_tabGroup_'] == '_trainTab_':
        window.find_element('_output_').Update('')
        print()

    # Always check for dataset availability
    if os.path.exists('data/data.txt'):
        window['_foundData_'].update("Dataset found.")
    else:
        window['_foundData_'].update("Dataset not found.")

    if event == 'Browse':
        values['_zippath_'] = values['_browseFile_']

    if event == 'Start training':

        if generationStarted:
            q.terminate()
            generationStarted = False

        if trainingStarted:
            print("Please save before restarting training.")
        else:
            window.find_element('_output_').Update('')

            trainingStarted = True

            args = "\"" + values['_modelsize_'] + "\"" + " " + values['_steps_'] + " " + values['_learningrate_'] + \
                   " " + values['_sampleevery_'] + " " + values['_batchsize_']

            programComplete = False
            thread = threading.Thread(target=runTraining, args=[args, window])
            thread.setDaemon(True)
            thread.start()

    if event == 'Save and end training' and trainingStarted:
        p.send_signal(signal.SIGINT)

        trainingStarted = False

    if event == 'Delete model' and not trainingStarted and not generationStarted and os.path.exists('checkpoint/run1'):
        option = sg.popup_yes_no(
            'Are you sure you want to delete the trained model? \nYou will have to retrain from step 0.',
            title='Confirm model deletion', keep_on_top=True)

        if option == 'Yes':
            shutil.rmtree('checkpoint/run1')
            sg.popup('Model deleted.', keep_on_top=True)

    if event == 'Generate dataset':
        try:
            generateData.generateDataset(values['_zippath_'])
            sg.popup("Dataset generated successfully.", title="Success", keep_on_top=True)
            window['_foundData_'].update("Dataset found.")
        except:
            sg.popup("Error: Invalid package path.", title="Error", keep_on_top=True)

    if event == 'Start text generation':

        window.find_element('_output_').Update('')

        if generationStarted:
            q.terminate()

        if trainingStarted:
            print("Please wait for training to complete, or save + end training.")
        else:
            generationStarted = True

            genArgs = "\"" + values['_genPrefix_'] + "\"" + " " + values['_genSampleNum_'] + " " + values[
                '_genSampleLen_'] + \
                      " " + values['_genBatchSize_'] + " " + values['_genTemp_'] + " " + values['_genTopK_'] + " " + \
                      values['_genTopP_']

            genThread = threading.Thread(target=runMessage, args=[genArgs, window])
            genThread.setDaemon(True)
            genThread.start()

    if event == 'End text generation' and generationStarted:
        q.terminate()
        print("Text generation ended.")
        generationStarted = False

window.Close()