import gpt_2_simple as gpt2



sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)
# To pick a trained model, do checkpoint="model number"
# Leave blank for most recent




x = input("Modes:\n1. Generate with number of samples as input\n2. Generate with a prompt to start generation with\n\nEnter nothing to exit.\n\nEnter mode number: ")

if not (x == "1" or x == "2"):
    exit()

args = {
        "sess": sess,
        "run_name":'run1',
        "checkpoint_dir":'checkpoint',
        "model_name":None,
        "model_dir":'models',
        "sample_dir":'samples',
        "return_as_list":False,
        "truncate":None,
        "destination_path":None,
        "sample_delim":'='*20 +'\n',
        "prefix":None,
        "seed":None,
        "nsamples":1,
        "batch_size":1,
        "length":100,
        "temperature":0.7,
        "top_k":0,
        "top_p":0.0,
        "include_prefix":True
        }


if (x == "1"):
    while (True):
        inp = input("\nEnter number of samples, enter nothing to quit: ")
        print("")
        if (inp == "" or not inp.isdigit()):
            print("A")
            break;

        args.update({"nsamples": int(inp)})
        gpt2.generate(**args)
        print("\n")

elif (x == "2"):
    while (True):
        inp = input("\nEnter prompt to start generation with, enter nothing to quit: ")
        if (inp == ""):
            break;

        print("")
        args.update({"prefix": inp})
        args.update({"include_prefix": False})
        gpt2.generate(**args)
        print("\n")







# Generation: Use short length and more nsamples for more speed
# temperature: 0.0 - 1.0. Higher value = More random. 0.7 is somewhat normal





