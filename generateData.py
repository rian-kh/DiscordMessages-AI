import zipfile
import csv
import os

def textContainsSpaces(text):
    for item in text:
        if (item == ''):
            return True

    return False

def generateDataset(zipPath):
    # Create zip file object of package, and path object relating to zip

    zip = zipfile.ZipFile(zipPath, "r")
    path = zipfile.Path(zip, "messages/")


    # Create initial data file to store messages
    if not os.path.exists('data/'):
        os.makedirs('data/')

    file = open("data/data.txt", "w", encoding="utf8")


    # Used to ensure that no blank lines are left during the writing process
    firstRun = True

    # Loop through each item in the messages directory
    for channel in path.iterdir():

        # If current item is a file (not a messages directory), continue to the next folder
        if (channel.is_file()): continue

        # Create CSV reader for each channel folder's messages
        file = channel.joinpath("messages.csv")
        reader = csv.reader(file.open("r", encoding="utf8"))



        # Skip initial line of CSV (Contents, etc)
        next(reader)


        # Go through each line of current CSV and output to data file
        for row in reader:
            with open("data/data.txt", 'a', encoding="utf8") as dataFile:

                # Clean up text
                text = row[2].rstrip().lstrip().strip().splitlines()

                # Clean up empty lines in multi-line messages
                while (textContainsSpaces(text)):
                    for line in text:
                        if (line == ''):
                            text.remove(line)

                # Only write the starting newline character for lines that aren't the first
                # (No blank lines will be left, can cause errors in training due to encoding?)
                for line in text:
                    if not firstRun:
                        dataFile.write("\n")
                    else:
                        firstRun = False

                    dataFile.write(line)

    # Close zip file
    zip.close()

