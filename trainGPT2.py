# Code adapted from gpt-2-simple: Usage on github.



print("Starting training script")

import gpt_2_simple as gpt2
import os
import sys


model_name = sys.argv[1].split()[0]
steps = int(sys.argv[2])
learningRate = float(sys.argv[3])
sampleEvery = int(sys.argv[4])
sampleLength = int(sys.argv[5])
batchSize = int(sys.argv[6])

# Check if model download is complete
if not os.path.isdir(os.path.join("models", model_name)):
	print("Downloading "+ model_name+ " model...")
	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/




print("Starting Tensorflow session")
sess = gpt2.start_tf_sess()

print("Starting finetuning")
gpt2.finetune(sess,
              "data.txt",
              model_name=model_name,
              steps=steps,
              batch_size=batchSize,
              only_train_transformer_layers=True,
              sample_every=sampleEvery,
              sample_length=sampleLength,
              overwrite=True,
              save_every=100,
              learning_rate=learningRate
              )   # steps is max number of training steps

gpt2.generate(sess)

