import zipfile
import csv

# Create zip file object of package, and path object relating to zip
zip = zipfile.ZipFile("package.zip", "r")
path = zipfile.Path(zip, "package/messages/")

# Create initial data file to store messages
file = open("data.txt", "w")
# Loop through each folder in the messages directory
i = 0



for channel in path.iterdir():
    i += 1

    # Create CSV reader for each channel's messages
    file = channel.joinpath("messages.csv")
    reader = csv.reader(file.open("r"))

    # Skip initial line of CSV (Contents, etc)
    next(reader)

    print("Channel " + str(i) + ":")

    j = 0

    # Go through each line of current CSV and output to data file
    for row in reader:
        j += 1
        print("Line " + str(j) + ": " + row[2])

        with open("data.txt", 'a') as dataFile:
            dataFile.write(row[2])
            dataFile.write("\n")

    print("\n")

# Close zip file
zip.close()
