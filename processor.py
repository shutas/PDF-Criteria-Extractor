import os
from config import *

def main():
    # List that we will eventually write to file
    master_list = []
    
    # For all .txt files in input2 directory
    file_list = [file for file in os.listdir(OUTPUT1_DIR) if file.endswith(".txt")]
    for file in file_list:
        print("Starting", file)
        # Read each line
        input_fp = open(os.path.join(OUTPUT1_DIR, file), "rb")
        line = input_fp.readline()

        while line:
            # Omit blank lines
            if line.isspace():
                line = input_fp.readline()
                continue

            # Append to list
            master_list.append(line.strip())

            # Read next line
            line = input_fp.readline()

        # Print list to file
        output_fp = open(os.path.join(OUTPUT2_DIR, file), "wb+")
        output_fp.write(str(master_list).encode("utf-8"))

        input_fp.close()
        output_fp.close()

        print("Done")


if __name__ == "__main__":
    main()
