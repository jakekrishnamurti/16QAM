#Jake Krishnamurti

#Dictionary to convert 16QAM voltage pairs to binary
conversion = {(1,1) : '1101', (1,3) : '1100', (1,-1) : '1111', (1,-3) : '1110', (3,1) : '1001', (3,3) : '1000', (3,-1) : '1011', (3,-3) : '1010', (-1,1) : '0101', (-1,3) : '0100', (-1,-1) : '0111', (-1,-3) : '0110', (-3,1) : '0001', (-3,3) : '0000', (-3,-1) : '0011', (-3,-3) : '0010'}

def main():
    #Open the file containing the nibbles expressed as voltage pairs
    nibbles_list = load_nibbles("nibbles.txt") 

    #Convert each voltage pair into binary and combine to create bytes
    binary_nibbles_list, bytes_list = convert_nibbles(nibbles_list) 
    
    #Print the decoded message
    for character in bytes_list:
        print(chr(int(character, 2)), end = '') 

    #Print information showing the decoding process
    show_decode_info(nibbles_list, binary_nibbles_list, bytes_list) 


def load_nibbles(filename):
    nibbles = open(filename, "r")

    nibbles_list = []

    for line in nibbles:
        nibbles_list.append(line.strip("\n"))

    return nibbles_list


def convert_nibbles(nibbles_list):
    binary_nibbles_list = []

    #Round each voltage to either +/-1 or +/-3
    for nibble in nibbles_list:
        values = nibble.split(', ')

        I = float(values[0])
        x = 0

        if 0 <= I < 2:
            x = 1
        if I >= 2:
            x = 3
        if -2 < I < 0:
            x = -1
        if I <= -2:
            x = -3 
        
        Q = float(values[1])
        y = 0

        if 0 <= Q < 2:
            y = 1
        if Q >= 2:
            y = 3
        if -2 < Q < 0:
            y = -1
        if Q <= -2:
            y = -3

        #Convert nibbles to binary
        binary_nibbles_list.append(conversion[(x,y)])

    bytes_list = []

    #Each consecutive pair of nibbles becomes one byte
    for i in range(0, len(binary_nibbles_list), 2):
        bytes_list.append(binary_nibbles_list[i] + binary_nibbles_list[i+1])

    return binary_nibbles_list, bytes_list


def show_decode_info(nibbles_list, binary_nibbles_list, bytes_list):
    print()
    nibble_count = 0
    byte_count = 0
    
    for nibble in nibbles_list:
        #Print the binary nibble that the voltage pair decodes to
        if nibble_count % 2 == 0:
            print("(", nibble, ")", sep='', end = '')
            print(" decodes as", binary_nibbles_list[nibble_count])

        #Print the binary nibble that the voltage pair decodes to and also the character that the combined byte represents
        if nibble_count % 2 == 1:
            print("(", nibble, ")", sep='', end = '')
            print(" decodes as", binary_nibbles_list[nibble_count], "- together, ", end = '')

            #If the character is not a space then print it, otherwise print [ ]
            if chr(int(bytes_list[byte_count], 2)) != " ":
                print(bytes_list[byte_count], " gives ", "\"", chr(int(bytes_list[byte_count], 2)), "\"", sep = '')
            else:
                print(bytes_list[byte_count], " gives ", "\"", '[ ]', "\"", sep = '')
                       
            byte_count = byte_count + 1
    
        nibble_count = nibble_count + 1  

main()
