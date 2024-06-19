import getch
import pwinput
import hashlib
import sys
import os
import random
import secrets
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

def logo():    
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
def random_sequence(passwd, padding):
    passwd += str(padding)
    sha256 = hashlib.sha256()
    sha256.update(passwd.encode('utf-8'))
    current_hash = sha256.hexdigest()
    
    large_number_str = current_hash
    while len(large_number_str) < 10000:
        sha256 = hashlib.sha256()
        sha256.update(large_number_str.encode('utf-8'))
        current_hash = sha256.hexdigest()
        large_number_str += current_hash
    
    passwd_hash = large_number_str[:10000]
    # Initialize the random generator with a hash-based seed
    random.seed(passwd_hash)

    # Random column
    first_column = list(range(256))
    random.shuffle(first_column)

    # Second static column
    second_column = [format(i, '08b') for i in range(256)]
    random.shuffle(second_column)

    # Combine two columns into a list
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


def gkey(random_sequence, source, target, block_size=(500 * 1024 * 1024)*2):
    # Crear la clave en memoria
    key = generate_key(random_sequence)

    buffer_size = (500 * 1024 * 1024)*2  # 1G
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

def rkey(random_sequence, source, target, block_size=(500 * 1024 * 1024)*2):
    # Crear la clave en memoria
    key = generate_key(random_sequence)
    inverse_key = {value: binary for binary, value in key.items()}

    buffer_size = (500 * 1024 * 1024)*2  # 1G
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

def generate_hash_key(passwd, key_length):
    sha256 = hashlib.sha256()
    sha256.update(passwd.encode('utf-8'))
    current_hash = sha256.digest()
    
    large_number_str = current_hash
    while len(large_number_str) < key_length:
        sha256 = hashlib.sha256()
        sha256.update(large_number_str)
        current_hash = sha256.digest()
        large_number_str += current_hash
    
    return large_number_str[:key_length]

def xor_crypt_file(input_file, output_file, password, mode='encrypt'):

    file_size = os.path.getsize(input_file)
    # Key from passwd hash
    key = generate_hash_key(password, file_size)


    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        key_index = 0
        while chunk := f_in.read(1):
            byte = chunk[0]
            key_byte = key[key_index]
            if mode == 'encrypt':
                result_byte = byte ^ key_byte
            elif mode == 'decrypt':
                result_byte = byte ^ key_byte

            f_out.write(bytes([result_byte]))
            key_index += 1

# Function to invert bits (1 to 0 and 0 to 1)
def invert_bits(bit_string):
    return ''.join('1' if char == '0' else '0' for char in bit_string)

def generate_random_sequence(password, length):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    digest = sha256.digest()
    random.seed(digest)
    return random.sample(range(length), length)


def process_byte_padding(byte, positions, padding):
    scrambled_byte = ['0'] * 8
    for i, pos in enumerate(positions):
        scrambled_byte[i] = ''.join('1' if bit == '0' else '0' for bit in byte[pos])
        # Add random padding
        scrambled_byte[i] = ''.join(random.choices('01', k=padding)) + scrambled_byte[i]
    return ''.join(scrambled_byte)

def process_byte(byte, positions):
    scrambled_byte = ['0'] * 8
    for i, pos in enumerate(positions):
        scrambled_byte[i] = '1' if byte[pos] == '0' else '0'
    return ''.join(scrambled_byte)

def reverse_byte(byte, positions):
    unscrambled_byte = ['0'] * 8
    for i, pos in enumerate(positions):
        unscrambled_byte[pos] = '1' if byte[i] == '0' else '0'
    return ''.join(unscrambled_byte)


def process_block(args):
    block, positions, scramble, padding = args
    if scramble:
        if padding != 0:
            processed_block = [process_byte_padding(format(byte, '08b'), positions, padding) for byte in block]
        else:
            processed_block = [process_byte(format(byte, '08b'), positions) for byte in block]
    else:
        processed_block = [reverse_byte(format(byte, '08b'), positions) for byte in block]
    return ''.join(processed_block)

# Binary Shuffle
def process_file(source, target, password, padding, scramble=True, progress_interval=0.1, block_size=1, num_processes=int(os.cpu_count()), batch_size=100000):
    total_size = os.path.getsize(source)
    if padding != 0 and scramble == False:
        total_size = total_size
    elif padding != 0 and scramble == True:
        total_size = total_size * (padding + 1)

    interval_bytes = max(1, int(total_size * progress_interval))
    start_time = time.time()
    processed_bytes = 0

    pool = multiprocessing.Pool(processes=num_processes)

    with open(source, 'rb') as src, open(target, 'ab') as tgt:
        buffer = deque()
        buffer_size = 0
        max_buffer_size = 1024   # buffer size

        block_index = 0
        while True:
            blocks = []
            for _ in range(batch_size):
                block = src.read(block_size)
                if not block:
                    break
                positions = generate_random_sequence(str(password) + str(block_index), 8)
                blocks.append((block, positions, scramble, padding))
                block_index += 1

            if not blocks:
                break

            # Map
            processed_blocks = pool.map(process_block, blocks)

            # Reduce
            for processed_block in processed_blocks:
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

    pool.close()
    pool.join()

# Function to scramble a file
def scramble_file(source, target, password, padding, progress_interval=0.01, block_size=1):
    process_file(source, target, password, padding, scramble=True, progress_interval=progress_interval, block_size=block_size)

# Function to unscramble a file
def unscramble_file(source, target, password, padding, progress_interval=0.01, block_size=1):
    process_file(source, target, password, padding, scramble=False, progress_interval=progress_interval, block_size=block_size)

def main():
    cls()
    logo()
        
    # Menu
    choice = ""
    while choice != "4":
        print(bcolors.YELLOW+"\n Options:")
        print(bcolors.GREEN+"1. Encrypter")
        print(bcolors.BLUE+"2. Decrypter")
        print(bcolors.PURPLE+"3. Passwd generator")
        print(bcolors.RED+"4. Quit")

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
                padding = int(input(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Fill *bit value (0-∞): "))
            except:
                print(bcolors.WHITE + "\n[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be a positive integer.")
                exit()

            start_time = time.time()
            tar_compression(target)

            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + f' Shuffling & Inverting')
            # Binary Shuffle | invert | fill | bits->bytes | bytes->decimal
            target_scrambled_file = target+'.temp'
            hash_obj = hashlib.sha256(password.encode())
            hash_int = int.from_bytes(hash_obj.digest(), byteorder='big')
            scramble_file(target, target_scrambled_file, hash_int, padding)
            os.replace(target_scrambled_file, target)

            gkey(random_sequence(password,padding), target, target+".temp")
            os.replace(target+".temp", target)
            
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Applying XOR key")
            target_xor = target+'.temp'
            xor_crypt_file(target, target_xor, password, mode='encrypt')
            os.replace(target_xor, target)

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
                print(bcolors.WHITE + "\n[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be a positive integer.")
                exit()
            start_time = time.time()

            # Recover file in case of unsuccessful decryption
            shutil.copy(target, f"{target}.backup")

            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Reversing XOR key")
            target_xor = target+'.temp'
            xor_crypt_file(target, target_xor, password, mode='decrypt')
            os.replace(target_xor, target)

            rkey(random_sequence(password,padding), target, target+".temp")
            os.replace(target+".temp", target)


            def ajustment(data):
                length = len(data)
                remainder = length % 8
                if remainder == 0:
                    decrypted_bytes = bits_to_bytes(data)
                else:
                    decrypted_bytes = bits_to_bytes(data[:-remainder])
                open(target, 'wb').close() 
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
            hash_obj = hashlib.sha256(password.encode())
            hash_int = int.from_bytes(hash_obj.digest(), byteorder='big')
            unscramble_file(target, target_unscrambled_file, hash_int, padding)
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


        if choice == "3":
            
            passwd = input(bcolors.WHITE+"\n[" + bcolors.GREEN+"+" + bcolors.WHITE+"] Passwd lenght 0-∞: ")
            print(bcolors.GREEN+"\n     1."+bcolors.WHITE+"Only lowe case\n"+bcolors.GREEN+"     2."+bcolors.WHITE+"Only letters\n"+bcolors.GREEN+"     3."+bcolors.WHITE+"Letters & numbers\n"+bcolors.GREEN+"     4."+bcolors.WHITE+ "All\n")
            choice = getch.getch()
            choice = int(choice)

            if choice == 1:
                characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z']
            if choice == 2:
                characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            elif choice == 3:
                characters = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            elif choice == 4:
                characters = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','"','#','$','%','&','(',')',',','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','^','_','`','{','|','}','~']

            tested = ['']
            
            cls()
            limit = input(bcolors.WHITE+"[" + bcolors.GREEN+"+" + bcolors.WHITE+"]  passwd's to generate: ")

            global counter
            counter=0
            seed = input(bcolors.WHITE+"[" + bcolors.RED+"!" + bcolors.WHITE+"] Enter the seed for ranom function (as long as possible): ")
            cls()

            random.seed(seed)
            def crack(passwd,characters):
                large = passwd
                def passwd_():
                    passwd = ''

                    number = random.randint(0,len(characters)-1)
                    letter = characters[number]
                    while len(passwd) < int(large):
                        number = random.randint(0,len(characters)-1)
                        letter = characters[number]
                        passwd += str(letter)
                    global counter
                    if counter < (int(limit)):
                        print(bcolors.WHITE+"[" + bcolors.GREEN+"=" + bcolors.WHITE+"]",str(counter)+"." ,passwd +"\n")
                        formato = (passwd)
                        tested.append(formato)
                        counter += 1
                    else:
                        print(bcolors.WHITE+"[" + bcolors.GREEN+"=" + bcolors.WHITE+"]",str(counter)+"." ,passwd +"\n")
                
                while int(counter) != int(limit):
                    passwd_()
 
            crack(passwd,characters)
            print(bcolors.WHITE+"[" + bcolors.RED+"+" + bcolors.WHITE+"]. Succesfully created "+limit+" passwd combinations:")
            exit()
            
if __name__ == "__main__":
    main()
