from getch import getch
import pwinput
import hashlib
import sys
import os
import random
import time
import shutil
import tarfile


class bcolors:
    PURPLE = '\033[95m' 
    BLUE = '\033[94m'
    BLUEL = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    UNDERLINE = '\033[4m'
    WHITE  = '\033[37m'
    ORANGE = '\33[33m'
    VIOLET = '\33[35m'

# Clear terminal
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
cls()

print("\n")                                                             
print(bcolors.GREEN+" ██╗      ██████╗██████╗ ██╗   ██╗██████╗ ████████╗")
print(bcolors.GREEN+" ██║     ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝")
print(bcolors.GREEN+" ██║     ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ")
print(bcolors.GREEN+" ██║     ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ")
print(bcolors.GREEN+" ███████╗╚██████╗██║  ██║   ██║   ██║        ██║   ")
print(bcolors.GREEN+" ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ")

sys.path.append(os.path.realpath("."))

def exit():
    sys.exit("\nExiting...")



def random_list(lenght, passwd):
    hash_obj = hashlib.sha256(passwd.encode())
    hash_int = int.from_bytes(hash_obj.digest(), byteorder='big')
    
    # Use passwd->number as seed to generate list
    random.seed(hash_int)
    random_list = list(range(1, lenght + 1))
    random.shuffle(random_list)  # Shuffle list
    return random_list

def reorganize_string(string, random_list):
    new_list = [None] * len(string)
    for i, index in enumerate(random_list):
        new_list[index - 1] = string[i]
    return ''.join(new_list)

def read_binary(file):
    with open(file, 'rb') as f:
        bytes = f.read()

    binary_content = ''.join(format(byte, '08b') for byte in bytes)
    return binary_content

def random_secuence(passwd):
    # generate first column with passwd dependency
    first_column = list(range(256))
    passwd_hash = hashlib.sha256(passwd.encode()).digest()
    random_seed = int.from_bytes(passwd_hash, 'big')
    random.seed(random_seed)
    random.shuffle(first_column)

    # generate second column fixed
    second_column = [format(i, '08b') for i in range(256)]

    # combine the 2 columns into list
    random_secuence = [f"{first_column[i]} {second_column[i]}" for i in range(256)]

    return random_secuence

def empty_file():
    with open(target, "w") as empty:
        empty.write("")


def tar_compression(file):
    print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + ' Compressing')
    try:
        # make tar file
        with tarfile.open(f"{file}.tar.gz", "w:gz") as tar:
            tar.add(file, arcname=os.path.basename(file))
        # Delete original file
        if os.path.isdir(file):
            shutil.rmtree(file)
        elif os.path.isfile(file):
            os.remove(file)
        shutil.move(f"{file}.tar.gz", f"{file}")
    except Exception as e:
        print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + f" Error on compression: {e}")
        exit()

def tar_decompression(file):
    print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + ' Decompressing')
    try:
        shutil.move(f"{file}", f"{file}.tar.gz")
        # extract tar.gz file
        with tarfile.open(f"{file}.tar.gz", "r:gz") as tar:
            tar.extractall(path=os.path.dirname(file))
            extracted_files = tar.getnames()

        # Obtenemos el nombre del último archivo extraído
        if extracted_files:
            last_extracted_file = extracted_files[-1]
            final_output_name = os.path.basename(last_extracted_file)
        os.remove(f"{file}.tar.gz")
        os.remove(f'{file}.backup')
        return final_output_name
    except Exception as e:
        print(bcolors.WHITE + "\n[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + f" Incorrect passwd | Backup file saved as {file}.backup")
        os.remove(f"{file}.tar.gz")
        exit()


# Menu
choice = ""
while choice != "3":
    print(bcolors.YELLOW+"\n Options:")
    print(bcolors.GREEN+"1. Encrypter")
    print(bcolors.BLUE+"2. Decrypter")
    print(bcolors.RED+"3. Quit")

    # Capture user num. input
    choice = getch()
    if isinstance(choice, bytes):
        choice = choice.decode("utf-8")

    if choice == "1":

        # Define the target to encryot [ file or folder ]
        target = input(bcolors.WHITE + "\n[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " Target name: ")
        password = pwinput.pwinput(bcolors.WHITE+"[" + bcolors.GREEN+"+" + bcolors.WHITE+"]" +bcolors.WHITE+ " Passwd: ")
        # Define the n of random bytes between original-encrypted ones
        padding = int(input(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Fill *bit value: "))
        start_time = time.time()
        if int(padding) < 1:
            print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be an integer equal to or greater than 1.")
            exit()
        
        print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + ' Executing Binary Shuffle')

        tar_compression(target)

        binary_content = read_binary(target)
        # Generate random list
        random_list = random_list(len(binary_content), password)
        # Reorganize bynary string
        binary_shuffle = reorganize_string(binary_content, random_list)

        def encriptar(file, padding):
 
            def insertar_aleatorios(padding):
                print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Injecting random bits")
                binary_shuffle
                encrypted_data = []
                random.seed(time.time())
                encrypted_data.extend(random.choices('01', k=padding))

                for bit in binary_shuffle:
                    encrypted_data.append('1' if bit == '0' else '0') # add reversed bit
                    encrypted_data.extend(random.choices('01', k=padding)) # generate random bit/s
                return ''.join(encrypted_data) # join all bits
            
            empty_file()
            with open(file, "wb") as f:
                encrypted_data = insertar_aleatorios(padding) # Call the function to invert and fill
                byte_data = bits_to_bytes(encrypted_data) # Call the function to convert bits to bytes
                f.write(byte_data)
                
        # function to convert bits to bytes
        def bits_to_bytes(bit_string):
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting bits to bytes") 
            return bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))

        encriptar(f"{target}", padding) # Binary Shuffle | invert | fill | bits->bytes

        random_secuence = random_secuence(password)

        with open("key", "w", encoding='utf-8') as f:
            for fila in random_secuence:
                f.write(f"{fila}\n")
            
        binary_data = read_binary(target)
        key = {}
        with open("key", "r") as key_file:
            for line in key_file:
                value, binary = line.strip().split()
                key[binary] = int(value)

        empty_file()
        with open(target, "ab") as encoded_file:
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting bytes to referenced decimal number") 
            block_size = 8
            for i in range(0, len(binary_data), block_size):
                block = binary_data[i:i+block_size]
                decimal_value = key.get(block)  
                decimal_output = str(decimal_value) + "\n"
                
                encoded_file.write(bytes([int(decimal_output)]))

        os.remove("key")
        print(bcolors.WHITE+"[" + bcolors.GREEN+"=" + bcolors.WHITE+"]" +bcolors.WHITE+ f" Encrypted file with padding {padding} & saved as '{target}'.")
        print(bcolors.WHITE + "[" + bcolors.GREEN + "#" + bcolors.WHITE + "]" + bcolors.WHITE + " Done ")
        end_time = time.time()
        elapsed_time = end_time - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print("\n{:.0f}h | {:.0f}m | {:.2f}s".format(hours, minutes, seconds))

        exit()
                
    if choice == "2": # Repeats 1 -> process is reversed

        def bits_to_bytes(bit_string):
            return bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))

        def decrypt(file, padding):
            
            with open(file, 'rb') as f:
                bytes = f.read()
                inverted_data = ''.join('1' if bit == '0' else '0' for byte in bytes for bit in format(byte, '08b'))

            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Removing random bits")    
            original_data = "".join(inverted_data[padding::(padding+1)])
            numeroactual = 0
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting bits to bytes")
            while numeroactual <= len(original_data):
                numeroactual += 8
            
            if numeroactual == len(original_data):
                decrypted_bytes = bits_to_bytes(original_data)
            else:
                numeroactual -= 8
                decrypted_bytes = bits_to_bytes(original_data[:-(len(original_data)-numeroactual)])


            empty_file()
            with open(file, "wb") as f:
                f.write(decrypted_bytes)
    
            

        target = input(bcolors.WHITE + "\n[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " Target name: ")
        password = pwinput.pwinput(bcolors.WHITE+"[" + bcolors.GREEN+"+" + bcolors.WHITE+"]" +bcolors.WHITE+ " Passwd: ")
        padding = int(input(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Fill *bit value: "))
        start_time = time.time()

        # Recover file in case of unsuccesfull decryption
        shutil.copy(f"{target}", f"{target}.backup")

        if int(padding) < 1:
            print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be an integer equal to or greater than 1.")
            exit()


        random_secuence = random_secuence(password)

        with open("key", "w", encoding='utf-8') as f:
            for fila in random_secuence:
                f.write(f"{fila}\n")

        with open(target, "rb") as encoded_file:
            # reads content as bytes secuence
            byte_content = encoded_file.read()
            decimal_values = []
            for byte in byte_content:
                decimal_values.append(str(byte))

        key = {}
        with open("key", "r") as key_file:
            for line in key_file:
                value, binary = line.strip().split()
                key[binary] = int(value)

        inverse_key = {value: binary for binary, value in key.items()}
        decimal_values = [value for value in decimal_values if value.strip()]

        empty_file()

        with open(target, "ab") as reconstructed_file:
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting decimal number to bytes referenced")
            for decimal_value in decimal_values:
                binary_block = inverse_key.get(int(decimal_value), "Unknown")  
                if binary_block != "Unknown":
                    decimal_value = int(binary_block, 2) 
                    reconstructed_file.write(bytes([decimal_value]))

   
        decrypt(f"{target}", padding)
        os.remove("key")
        
        def restaurar_string(string, random_list):
            string_original = [None] * len(string)
            for i, index in enumerate(random_list):
                string_original[i] = string[index - 1]
            return ''.join(string_original)
        
        print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + ' Reverting Binary Shuffle')
        binary_content = read_binary(target)
        random_list = random_list(len(binary_content), password)
        revert_binary_shuffle = restaurar_string(binary_content, random_list)

        empty_file()
        with open(target, "ab") as reconstructed_file:
            byte_data = bytes(int(revert_binary_shuffle[i:i+8], 2) for i in range(0, len(revert_binary_shuffle), 8))
            reconstructed_file.write(byte_data)
        
        file = tar_decompression(target)

        print(bcolors.WHITE+"[" + bcolors.GREEN+"=" + bcolors.WHITE+"]" +bcolors.WHITE+ f" Decrypted file saved as '{file}'")
        print(bcolors.WHITE + "[" + bcolors.GREEN + "#" + bcolors.WHITE + "]" + bcolors.WHITE + " Done ")
        end_time = time.time()
        elapsed_time = end_time - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print("\n{:.0f}h | {:.0f}m | {:.2f}s".format(hours, minutes, seconds))

        exit()
