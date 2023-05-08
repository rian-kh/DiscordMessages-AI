import os.path

print("Starting message generation...")
if not os.path.exists('checkpoint/run1'):
    print("No model found. Please train a model first.")
    exit()

import gpt_2_simple as gpt2
import sys

print("Starting TensorFlow session...")



sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)
# To pick a trained model, do checkpoint="model number"
# Leave blank for most recent


prefix = sys.argv[1]
sampleNum = int(sys.argv[2])
sampleLen = int(sys.argv[3])
batchSize = int(sys.argv[4])
temperature = float(sys.argv[5])
topK = int(sys.argv[6])
topP = float(sys.argv[7])


gpt2.generate(sess,
              prefix=prefix,
              nsamples=sampleNum,
              length=sampleLen,
              batch_size=batchSize,
              temperature=temperature,
              top_k=topK,
              top_p=topP)

print("\nSample generation complete.")










# Generation: Use short length and more nsamples for more speed
# temperature: 0.0 - 1.0. Higher value = More random. 0.7 is somewhat normal





