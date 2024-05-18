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

def verify_exists(file):
    if os.path.exists(file):
        pass
    else:
        print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + f" File '{file}' not found")
        exit()

def read_binary(file):
    with open(file, 'rb') as f:
        bytes = f.read()
    binary_content = ''.join(format(byte, '08b') for byte in bytes)
    return binary_content


def empty_file():
    open(target, 'wb').close()


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
    print(bcolors.WHITE + "\n[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + ' Decompressing')
    try:
        shutil.move(f"{file}", f"{file}.tar.gz")
        # extract tar.gz file
        with tarfile.open(f"{file}.tar.gz", "r:gz") as tar:
            tar.extractall(path=os.path.dirname(file))
            extracted_files = tar.getnames()

        # Obtain extracted file name
        if extracted_files:
            last_extracted_file = extracted_files[-1]
            final_output_name = os.path.basename(last_extracted_file)
        os.remove(f"{file}.tar.gz")
        os.remove(f'{file}.backup')
        return final_output_name
    except Exception as e:
        print(bcolors.WHITE + "\n[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + f" Incorrect passwd or padding | Backup file saved as {file}.backup")
        os.remove(f"{file}.tar.gz")
        exit()

# function to convert bits to bytes
def bits_to_bytes(bit_string):
    return bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))

# Function to generate a random sequence based on a password
def random_secuence(passwd):
    # Generate first column with password dependency
    first_column = list(range(256))
    passwd_hash = hashlib.sha256(passwd.encode()).digest()
    random_seed = int.from_bytes(passwd_hash, 'big')
    random.seed(random_seed)
    random.shuffle(first_column)

    # Generate second column fixed
    second_column = [format(i, '08b') for i in range(256)]

    # Combine the two columns into a list
    random_secuence = [f"{first_column[i]} {second_column[i]}" for i in range(256)]
    return random_secuence

def gkey(random_secuence):
    # Create key in memory
    key = {}
    for line in random_secuence:
        value, binary = line.strip().split()
        key[binary] = int(value)

    binary_data = read_binary(target)

    empty_file()
    with open(target, "ab") as encoded_file:
        if padding != 0:
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting bytes to referenced decimal number") 
        else:
            print(bcolors.WHITE + "\n[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting bytes to referenced decimal number") 
        block_size = 8
        for i in range(0, len(binary_data), block_size):
            block = binary_data[i:i+block_size]
            decimal_value = key.get(block)  
            decimal_output = str(decimal_value) + "\n"
            encoded_file.write(bytes([int(decimal_output)]))

def rkey(random_secuence):
    # Create key in memory
    key = {}
    for line in random_secuence:
        value, binary = line.strip().split()
        key[binary] = int(value)

    with open(target, "rb") as encoded_file:
        # reads content as bytes sequence
        byte_content = encoded_file.read()
        decimal_values = [byte for byte in byte_content]

    inverse_key = {value: binary for binary, value in key.items()}

    empty_file()
    with open(target, "ab") as reconstructed_file:

        print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting decimal number to bytes referenced")
        for decimal_value in decimal_values:
            binary_block = inverse_key.get(decimal_value, "Unknown")  
            if binary_block != "Unknown":
                decimal_value = int(binary_block, 2) 
                reconstructed_file.write(bytes([decimal_value]))

# Function to invert bits (1 to 0 and 0 to 1)
def invert_bits(bit_string):
    return ''.join('1' if char == '0' else '0' for char in bit_string)

# Function to generate a random sequence based on a password and length
def generate_random_sequence(password, length):
    random.seed(password)
    return [random.randint(0, length - 1) for _ in range(length)]

# Function to shuffle a file
def scramble_file(source, target, password, progress_interval=0.01):
    total_size = os.path.getsize(source)
    processed_bytes = 0
    interval_bytes = max(1, int(total_size * progress_interval))
    start_time = time.time()
    
    with open(source, 'rb') as src, open(target, 'ab') as tgt:
        byte = src.read(1)
        while byte:
            byte_str = bin(int.from_bytes(byte, "big"))[2:].zfill(8)
            scrambled_byte = process_byte(byte_str, password, scramble=True)
            tgt.write(bits_to_bytes(scrambled_byte))
            processed_bytes += 1
            if processed_bytes % interval_bytes == 0 or processed_bytes == total_size:
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    speed = processed_bytes / elapsed_time
                    remaining_bytes = total_size - processed_bytes
                    remaining_time = remaining_bytes / speed
                else:
                    remaining_time = 0
                progress = int(processed_bytes / total_size * 100)
                print(bcolors.WHITE + "[" + bcolors.RED + "~" + bcolors.WHITE + "]" + bcolors.WHITE +f" Progress: "+bcolors.VIOLET+f"{progress}"+bcolors.WHITE+f"% competed | "+bcolors.BLUEL+f"{processed_bytes}"+bcolors.WHITE+f"/"+bcolors.ORANGE+f"{total_size}"+bcolors.WHITE+f" bytes | Time left: "+bcolors.GREEN+f"{remaining_time:.2f}"+bcolors.WHITE+" sec", end="\r")
            byte = src.read(1)

# Function to unshuffle a file
def unscramble_file(source, target, password, progress_interval=0.01):
    total_size = os.path.getsize(source)
    processed_bytes = 0
    interval_bytes = max(1, int(total_size * progress_interval))
    start_time = time.time()
    
    with open(source, 'rb') as src, open(target, 'ab') as tgt:
        byte = src.read(1)
        while byte:
            byte_str = bin(int.from_bytes(byte, "big"))[2:].zfill(8)
            unscrambled_byte = process_byte(byte_str, password, scramble=False)
            tgt.write(bits_to_bytes(unscrambled_byte))
            processed_bytes += 1
            if processed_bytes % interval_bytes == 0 or processed_bytes == total_size:
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    speed = processed_bytes / elapsed_time
                    remaining_bytes = total_size - processed_bytes
                    remaining_time = remaining_bytes / speed
                else:
                    remaining_time = 0
                progress = int(processed_bytes / total_size * 100)
                print(bcolors.WHITE + "[" + bcolors.RED + "~" + bcolors.WHITE + "]" + bcolors.WHITE +f" Progress: "+bcolors.VIOLET+f"{progress}"+bcolors.WHITE+f"% competed | "+bcolors.BLUEL+f"{processed_bytes}"+bcolors.WHITE+f"/"+bcolors.ORANGE+f"{total_size}"+bcolors.WHITE+f" bytes | Time left: "+bcolors.GREEN+f"{remaining_time:.2f}"+bcolors.WHITE+" sec", end="\r")
            byte = src.read(1)

# Function to process a byte based on a password and scramble or unscramble it
def process_byte(byte_str, password, scramble=True):
    length = len(byte_str)
    positions = generate_random_sequence(password, length)
    processed_byte = list(invert_bits(byte_str))
    if scramble:
        for i in range(length):
            pos = positions[i]
            processed_byte[i], processed_byte[pos] = processed_byte[pos], processed_byte[i]
    else:
        for i in range(length - 1, -1, -1):
            pos = positions[i]
            processed_byte[i], processed_byte[pos] = processed_byte[pos], processed_byte[i]

    return ''.join(processed_byte)


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
        # Define the target to encrypt [ file or folder ]
        target = input(bcolors.WHITE + "\n[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " Target name: ")
        verify_exists(target)
        password = pwinput.pwinput(bcolors.WHITE+"[" + bcolors.GREEN+"+" + bcolors.WHITE+"]" +bcolors.WHITE+ " Passwd: ")

        # Define the n of random bytes between original-encrypted ones
        try:
            global padding
            padding = int(input(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Fill *bit value (0-∞): "))
        except:
            print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be a positive integer.")
            exit()

        start_time = time.time()
        tar_compression(target)

        print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + f' Shuffling & Inverting')

        # Binary Shuffle | invert | fill | bits->bytes | bytes->decimal
        target_scrambled_file = target+'.temp'
        scramble_file(target, target_scrambled_file, password)
        os.replace(target_scrambled_file, target)

        if padding != 0:
            print(bcolors.WHITE + "\n[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + f' Injecting bits')
            with open(target, 'rb') as f_input:
                with open(target + ".temp", 'wb') as f_output:
                    original_bytes = f_input.read()
                    bit_string = ''.join(format(byte, '08b') for byte in original_bytes)
                    modified_bit_string = ''.join(''.join(random.choices('01', k=padding)) + bit for bit in bit_string)
                    modified_bit_string += ''.join(random.choices('01', k=padding))
                    f_output.write(bits_to_bytes(''.join(modified_bit_string)))

            # Replace original file
            os.replace(target + ".temp", target)

        random_secuence = random_secuence(password)
        gkey(random_secuence)

        state = 'without' if padding == 0 else 'with'
        print(bcolors.WHITE+"[" + bcolors.GREEN+"=" + bcolors.WHITE+"]" +bcolors.WHITE+ f" Encrypted file {state} padding & saved as '{target}'.")
        print(bcolors.WHITE + "[" + bcolors.GREEN + "#" + bcolors.WHITE + "]" + bcolors.WHITE + " Done ")
        end_time = time.time()
        elapsed_time = end_time - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print("\n{:.0f}h | {:.0f}m | {:.2f}s".format(hours, minutes, seconds))

        exit()

                
    if choice == "2":  # Decrypt
        target = input(bcolors.WHITE + "\n[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " Target name: ")
        verify_exists(target)
        password = pwinput.pwinput(bcolors.WHITE + "[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " Passwd: ")
        try:
            padding = int(input(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Fill *bit value (0-∞): "))
        except:
            print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be a positive integer.")
            exit()
        start_time = time.time()

        # Recover file in case of unsuccessful decryption
        shutil.copy(target, f"{target}.backup")

        random_secuence = random_secuence(password)
        rkey(random_secuence)

        with open(target, 'rb') as f:
            content = f.read()
        plain = ''.join('1' if bit == '1' else '0' for byte in content for bit in format(byte, '08b'))

        def ajustment(data):
            length = len(data)
            remainder = length % 8
            if remainder == 0:
                decrypted_bytes = bits_to_bytes(data)
            else:
                decrypted_bytes = bits_to_bytes(data[:-remainder])
            empty_file() 
            with open(target, "wb") as f:
                f.write(decrypted_bytes)

        if padding != 0:
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Removing random bits")
            original_data = plain
            adjusted_data = "".join(original_data[i] for i in range(padding, len(original_data), padding + 1))
            ajustment(adjusted_data)
        else:
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Not removing random bits")
            ajustment(plain)

        # Unscramble the file
        print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + ' Inverting & Reverting Binary Shuffle')
        target_unscrambled_file = target+'.temp'
        unscramble_file(target, target_unscrambled_file, password)
        os.replace(target_unscrambled_file, target)
        file = tar_decompression(target)

        print(bcolors.WHITE+"[" + bcolors.GREEN+"=" + bcolors.WHITE+"]" +bcolors.WHITE+ f" Decrypted file saved as '{file}'")
        print(bcolors.WHITE + "[" + bcolors.GREEN + "#" + bcolors.WHITE + "]" + bcolors.WHITE + " Done ")
        end_time = time.time()
        elapsed_time = end_time - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print("\n{:.0f}h | {:.0f}m | {:.2f}s".format(hours, minutes, seconds))

        exit()
