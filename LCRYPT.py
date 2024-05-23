import getch
import pwinput
import hashlib
import sys
import os
import random
import time
import shutil
import tarfile
import multiprocessing
from collections import deque
from io import BytesIO


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
def bits_to_bytes(bits):
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
        
# Function to generate a random sequence based on a password
def random_sequence(passwd):
    # Generate first column with password dependency
    first_column = list(range(256))
    passwd_hash = hashlib.sha256(passwd.encode()).digest()
    random_seed = int.from_bytes(passwd_hash, 'big')
    random.seed(random_seed)
    random.shuffle(first_column)

    # Generate second column fixed
    second_column = [format(i, '08b') for i in range(256)]

    # Combine the two columns into a list
    random_sequence = [f"{first_column[i]} {second_column[i]}" for i in range(256)]
    return random_sequence

# Función para leer datos binarios de un archivo en bloques
def read_binary_in_blocks(file_path, block_size):
    with open(file_path, "rb") as file:
        while True:
            block = file.read(block_size)
            if not block:
                break
            yield block

# Función global para procesar bloques en gkey
def process_block_gkey(block, key):
    block_size = 8
    result = []
    for byte in block:
        binary_byte = format(byte, '08b')
        decimal_value = key.get(binary_byte)
        if decimal_value is not None:
            result.append(decimal_value)
    return result

# Función global para procesar bloques en rkey
def process_block_rkey(block, inverse_key):
    result = []
    for byte in block:
        binary_block = inverse_key.get(byte, "Unknown")
        if binary_block != "Unknown":
            decimal_value = int(binary_block, 2)
            result.append(decimal_value)
    return result

# Función para generar la clave en memoria a partir de una secuencia aleatoria
def generate_key(random_sequence):
    key = {}
    for line in random_sequence:
        value, binary = line.strip().split()
        key[binary] = int(value)
    return key


def gkey(random_sequence, source, target, block_size=1024):
    # Crear la clave en memoria
    key = generate_key(random_sequence)

    buffer_size = 500 * 1024 * 1024  # 500 MB
    buffer = BytesIO()

    with open(target, "ab") as encoded_file:
        print(bcolors.WHITE + "\n[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting bytes to referenced decimal number") 

        pool = multiprocessing.Pool()

        for block in read_binary_in_blocks(source, block_size):
            result = process_block_gkey(block, key)
            for decimal_value in result:
                buffer.write(bytes([decimal_value]))

            if buffer.tell() >= buffer_size:
                buffer.seek(0)
                encoded_file.write(buffer.read())
                buffer.seek(0)
                buffer.truncate(0)

        if buffer.tell() > 0:
            buffer.seek(0)
            encoded_file.write(buffer.read())

        pool.close()
        pool.join()

def rkey(random_sequence, source, target, block_size=1024):
    # Crear la clave en memoria
    key = generate_key(random_sequence)
    inverse_key = {value: binary for binary, value in key.items()}

    buffer_size = 500 * 1024 * 1024  # 500 MB
    buffer = BytesIO()

    with open(target, "ab") as reconstructed_file:
        print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting decimal number to bytes referenced")

        pool = multiprocessing.Pool()

        for block in read_binary_in_blocks(source, block_size):
            result = process_block_rkey(block, inverse_key)
            for decimal_value in result:
                buffer.write(bytes([decimal_value]))

            if buffer.tell() >= buffer_size:
                buffer.seek(0)
                reconstructed_file.write(buffer.read())
                buffer.seek(0)
                buffer.truncate(0)

        if buffer.tell() > 0:
            buffer.seek(0)
            reconstructed_file.write(buffer.read())

        pool.close()
        pool.join()


# Function to invert bits (1 to 0 and 0 to 1)
def invert_bits(bit_string):
    return ''.join('1' if char == '0' else '0' for char in bit_string)

def generate_random_sequence(password, length):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    digest = sha256.digest()
    random.seed(digest)
    return random.sample(range(length), length)

def process_byte_padding(byte, positions):
    scrambled_byte = ['0'] * 8
    for i, pos in enumerate(positions):
        scrambled_byte[i] = ''.join(random.choices('01', k=padding)) + byte[pos]
    return ''.join(scrambled_byte)

def process_byte(byte, positions):
    scrambled_byte = ['0'] * 8
    for i, pos in enumerate(positions):
        scrambled_byte[i] = byte[pos]
    return ''.join(scrambled_byte)

def reverse_byte(byte, positions):
    unscrambled_byte = ['0'] * 8
    for i, pos in enumerate(positions):
        unscrambled_byte[pos] = byte[i]
    return ''.join(unscrambled_byte)

def process_block(args):
    block_index, block, positions, scramble = args
    if scramble:
        if padding != 0:
            processed_block = [process_byte_padding(format(byte, '08b'), positions) for byte in block]
        else:
            processed_block = [process_byte(format(byte, '08b'), positions) for byte in block]
    else:
        processed_block = [reverse_byte(format(byte, '08b'), positions) for byte in block]
    return block_index, ''.join(processed_block)


# Byte shuffle
def process_file(source, target, password, scramble=True, progress_interval=0.1, block_size=4096, num_processes=8):
    total_size = os.path.getsize(source)
    if padding != 0 and scramble == False:
        total_size = total_size
    elif padding != 0 and scramble == True:
        total_size = total_size * (padding + 1)

    interval_bytes = max(1, int(total_size * progress_interval))
    start_time = time.time()
    processed_bytes = 0

    with open(source, 'rb') as src:
        blocks = []
        block_index = 0
        while True:
            block = src.read(block_size)
            if not block:
                break
            positions = generate_random_sequence(password + str(block_index), 8)
            blocks.append((block_index, block, positions, scramble))
            block_index += 1

    with multiprocessing.Pool(processes=num_processes) as pool:
        processed_blocks = pool.map(process_block, blocks)

    processed_blocks.sort(key=lambda x: x[0])

    buffer = deque()
    buffer_size = 0
    max_buffer_size = 500 * 1024 * 1024  # 500MB buffer size

    with open(target, 'ab') as tgt:
        for block_index, processed_block in processed_blocks:
            buffer.append(bits_to_bytes(processed_block))
            buffer_size += len(processed_block) // 8

            if buffer_size >= max_buffer_size:
                while buffer:
                    tgt.write(buffer.popleft())
                buffer_size = 0

            processed_bytes += len(processed_block) // 8

            if processed_bytes >= interval_bytes or processed_bytes == total_size:
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    speed = processed_bytes / elapsed_time
                    remaining_bytes = total_size - processed_bytes
                    remaining_time = remaining_bytes / speed
                else:
                    remaining_time = 0
                progress = int(processed_bytes / total_size * 100)
                print(bcolors.WHITE + "[" + bcolors.RED + "~" + bcolors.WHITE + "]" + bcolors.WHITE +f" Progress: "+bcolors.VIOLET+f"{progress}"+bcolors.WHITE+f"% competed | "+bcolors.BLUEL+f"{processed_bytes}"+bcolors.WHITE+f"/"+bcolors.ORANGE+f"{total_size}"+bcolors.WHITE+f" bytes | Time left: "+bcolors.GREEN+f"{remaining_time:.2f}"+bcolors.WHITE+" sec", end="\r")

                interval_bytes += max(1, int(total_size * progress_interval))

        while buffer:
            tgt.write(buffer.popleft())

# Function to scramble a file
def scramble_file(source, target, password, progress_interval=0.01, block_size=4096):
    process_file(source, target, password, scramble=True, progress_interval=progress_interval, block_size=block_size)

# Function to unscramble a file
def unscramble_file(source, target, password, progress_interval=0.01, block_size=4096):
    process_file(source, target, password, scramble=False, progress_interval=progress_interval, block_size=block_size)


# Menu
choice = ""
while choice != "3":
    print(bcolors.YELLOW+"\n Options:")
    print(bcolors.GREEN+"1. Encrypter")
    print(bcolors.BLUE+"2. Decrypter")
    print(bcolors.RED+"3. Quit")

    # Capture user num. input
    choice = getch.getch()
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
        hash_obj = hashlib.sha256(password.encode())
        hash_int = int.from_bytes(hash_obj.digest(), byteorder='big')
        scramble_file(target, target_scrambled_file, password)
        os.replace(target_scrambled_file, target)

        

        random_sequence = random_sequence(password)
        gkey(random_sequence, target, target+".temp")
        os.replace(target+".temp", target)

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

        random_sequence = random_sequence(password)
        rkey(random_sequence, target, target+".temp")
        os.replace(target+".temp", target)


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

        if padding != 0: # Remove bit padding
            with open(target, 'rb') as f:
                content = f.read()
                plain = ''.join('1' if bit == '1' else '0' for byte in content for bit in format(byte, '08b'))
                
                print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Removing random bits")
                original_data = plain
                adjusted_data = "".join(original_data[i] for i in range(padding, len(original_data), padding + 1))
                ajustment(adjusted_data)


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
