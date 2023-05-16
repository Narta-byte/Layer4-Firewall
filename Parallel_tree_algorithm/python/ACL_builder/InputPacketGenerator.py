# %%
import random

random.seed(1)
outputFile = open("output_packets.txt", "w")
flag = False
gibberishFile = ""
# with open("input_packets.txt", "r") as file:
#     lines = file.readlines()
#     for line in lines:
#         line = line.split()
#         if line[1] == "0" or flag == True:
#             flag = True
#             gibberishFile += line[0] + " " + "1\n"
#             if line[1] == "1":
#                 flag = False
with open("input_packets.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.split()
        if line[1] == "1" or flag == True:
            flag = True
            outputFile.write(line[0] + " 1 " + line[1] +" "+ line[2] + "\n")
            if line[2] == "1":
                for i in range(random.randint(0, 64)):
                    random_byte = random.randint(0, 255)
                    hex_string = format(random_byte, '02x')
                    outputFile.write(hex_string + " " + "0" + " 0" + " 0\n")

                flag = False



        #     continue
        # if line[2] == "1":
        #     flag = False
        # flag = True
        # outputFile.write(line[0] + " " + "1\n")


outputFile.close()

# %%
