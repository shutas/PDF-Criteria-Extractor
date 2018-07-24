import os
from config import *

def main():
    # Delete all files in current output directory
    file_list = [file for file in os.listdir(OUTPUT2_DIR) if file.endswith(".txt")]
    for file in file_list:
        os.remove(os.path.join(OUTPUT2_DIR, file))
    
    # List that we will eventually write to file
    master_list = []
    
    # For all .txt files in input2 directory
    file_list = [file for file in os.listdir(OUTPUT1_DIR) if file.endswith(".txt")]
    for file in file_list:
        print("Starting", file)
        # Read each line
        input_fp = open(os.path.join(OUTPUT1_DIR, file), "rb")
        line = input_fp.readline().decode("utf-8")

        while line:
            # Omit blank lines
            if line.isspace():
                line = input_fp.readline().decode("utf-8")
                continue

            # Append to list
            master_list.append(line.strip())

            # Read next line
            line = input_fp.readline().decode("utf-8")

        # Print list to file
        output_fp = open(os.path.join(OUTPUT2_DIR, file), "w+")
        output_fp.write(str(master_list))

        input_fp.close()
        output_fp.close()

        print("Done")


if __name__ == "__main__":
    main()
