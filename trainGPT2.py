# Code adapted from gpt-2-simple: Usage on github.



print("Starting training script...")
import os

if not (os.path.exists('data/data.txt')):
    print("No dataset found. Please generate a dataset")
    exit()

import gpt_2_simple as gpt2
import sys


model_name = sys.argv[1].split()[0]
steps = int(sys.argv[2])
learningRate = float(sys.argv[3])
sampleEvery = int(sys.argv[4])
batchSize = int(sys.argv[5])


# Check if model download is FULLY complete
if not os.path.exists('models/' + model_name + '/downloadComplete'):
    print("Downloading "+ model_name+ " model...")
    gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/
    print(model_name + " model downloaded.")



print("Starting TensorFlow session...")
sess = gpt2.start_tf_sess()

print("Starting finetuning...")


gpt2.finetune(sess,
              "data/data.txt",
              model_name=model_name,
              steps=steps,
              batch_size=batchSize,
              only_train_transformer_layers=True,
              sample_every=sampleEvery,
              sample_length=100,
              overwrite=True,
              save_every=100,
              learning_rate=learningRate
              )   # steps is max number of training steps



