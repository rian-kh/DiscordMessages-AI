# DiscordMessages-AI
A program that uses your Discord message information from your Discord Data Package to create AI-generated messages trained using GPT-2. 

<img width="450" alt="Screen Shot 2023-05-09 at 10 54 34 PM" src="https://github.com/rian-kh/DiscordMessages-AI/assets/128095876/bfe08e71-a6e1-43b5-bf4c-d7f35a5a366e">

<img width="450" alt="Screen Shot 2023-05-09 at 8 48 52 PM" src="https://github.com/rian-kh/DiscordMessages-AI/assets/128095876/6a149f94-7cc5-4fbd-a338-511df8de0ea2">

**Important Notes:**
- This program uses [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple/) and [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI).
- gpt_2_simple/gpt_2.py was modified to display steps of training/generation **(Issue #1)**
- Do NOT exit/terminate training during saving, as this has a chance of reverting **all** training done no matter the steps.
-   Process management is REALLY bad in this, make sure to check for any python3.9 processes still running after exiting!!!

## Installation

### Windows (using CPU)
1. Set up a Python virtual environment with the following:
 - Python (latest)
 - gpt_2_simple (latest)
 - PySimpleGUI (latest)
2. Unzip the DiscordMessages-AI repository **into** an IDE's project folder (like PyCharm).
3. Go to your environment executable folder and drag the **site-packages** folder from the unzipped repository into it. **(Will replace some files)**
4. Run main<area>.py using the respective Python environment.

### Windows (using GPU)
1. Set up a conda virtual environment with the following (refer to [Tensorflow w/ GPU installation](https://www.tensorflow.org/install/pip#windows-native)):
 - Python 3.9
 - Tensorflow 2.10 
 - CUDA Toolkit 11.2
 - cuDNN 8.1.0
 - gpt_2_simple (latest)
 - PySimpleGUI (latest)
2. Unzip the DiscordMessages-AI repository **into** an IDE's project folder (like PyCharm).
3. Go to your environment executable folder and drag the **site-packages** folder from the unzipped repository into it. **(Will replace some files)**
4. Run main<area>.py using the respective Python environment.

### macOS (Apple Silicon)
1. Set up a conda virtual environment with the following (refer to [tensorflow-metal Installation](https://developer.apple.com/metal/tensorflow-plugin/)):
 - Python 3.9
 -  gpt_2_simple (latest). **Make sure to uninstall the tensorflow dependency it'll come with, and use tensorflow-macos instead!**
 - tensorflow-deps (Latest)
 - tensorflow-macos (Latest)
 - tensorflow-metal (Latest)
 - PySimpleGUI (latest)
2. Unzip the DiscordMessages-AI repository **into** an IDE's project folder (like PyCharm).
3. Go to your environment executable folder and drag the **site-packages** folder from the unzipped repository into it. **(Will replace some files)**
4. Run main<area>.py using the respective Python environment.

## Usage

### Training the model
1. Download your Discord Data Package as package.zip.
2. Browse for your package and generate your dataset.
3. Set training parameters and train for however many steps you want. Train for at least 200 steps for it to adopt your messaging patterns, and ~5000 for best output (less randomness, less out-of-character messages)
4. Press "Save and end training" when you want to finish training, before moving on.

### Generating messages with the model
1. Switch to the "Test model" tab and set generation parameters.  Keep the number of samples higher (>5) as it's faster to generate more samples in a row than generate them individually.
2. If you want to end sample generation prematurely, press "End text generation".


