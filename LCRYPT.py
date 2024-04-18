from getch import getch
from getpass import getpass
import hashlib
import subprocess
import sys
import os
import random

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

# Menu
choice = ""
while choice != "3":
    print(bcolors.YELLOW+"\n Options:")
    print(bcolors.GREEN+"1. Encrypter")
    print(bcolors.BLUE+"2. Decrypter")
    print(bcolors.RED+"3. Quit")

    # Capture user num. input
    choice = getch()

    if choice == "1":

        # Define the target to encryot [ file or folder ]
        target = input(bcolors.WHITE + "\n[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " Target name: ")
        password = getpass(bcolors.WHITE+"[" + bcolors.GREEN+"+" + bcolors.WHITE+"]" +bcolors.WHITE+ " Passwd: ")
        # Set the AES-256 & remove original target
        cmd = f'tar -czvf - {target} | openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 1000000 -salt -out {target}.tar.enc -k "{password}" && rm -r {target}'
        print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + ' Executing AES-256')
        try:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(bcolors.RED + "Error:", e.stderr.decode())
            exit()

        # Define the n of random bytes between original-encrypted ones
        separacion = int(input(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Fill *bit value: "))
        if int(separacion) < 1:
            print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be an integer equal to or greater than 1.")
            exit()

        def encriptar(file, separacion):
            with open("tempfile", "w") as f: # grep the binary file content
                subprocess.run(["xxd -b "+f"{target}.tar.enc"+" | cut -d' ' -f2- | cut -d' ' -f1-7 | tr -d ' ' | tr -d '\n'"], shell=True, stdout=f)

            def insertar_aleatorios(separacion):
                print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Injecting random bits")
                with open("tempfile", "r") as f:
                    binary_data = f.read()
                encrypted_data = []
                encrypted_data.extend(random.choices('01', k=separacion))

                for bit in binary_data:
                    encrypted_data.append('1' if bit == '0' else '0') # add reversed bit
                    encrypted_data.extend(random.choices('01', k=separacion)) # generate random bit/s

                return ''.join(encrypted_data) # join all bits
            
            subprocess.run(["rm "+f"{target}.tar.enc"], shell=True)
            with open(file, "wb") as f:
                encrypted_data = insertar_aleatorios(separacion) # Call the function to invert and fill
                byte_data = bits_to_bytes(encrypted_data) # Call the function to convert bits to bytes
                f.write(byte_data)
                
        # function to convert bits to bytes
        def bits_to_bytes(bit_string):
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting bits to bytes") 
            return bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))

        encriptar(f"{target}.tar.enc", separacion) # AES-256 | invert | fill | bits->bytes

        def generar_secuencia_aleatoria_con_contraseña(contraseña):
            # Generar la primera columna permutada según la contraseña
            primera_columna = list(range(256))
            hash_contraseña = hashlib.sha256(contraseña.encode()).digest()
            random_seed = int.from_bytes(hash_contraseña, 'big')
            random.seed(random_seed)
            random.shuffle(primera_columna)

            # Generar la segunda columna fija
            segunda_columna = [format(i, '08b') for i in range(256)]

            # Combinar las dos columnas en una lista de cadenas
            secuencia_aleatoria = [f"{primera_columna[i]} {segunda_columna[i]}" for i in range(256)]

            return secuencia_aleatoria

        secuencia_aleatoria = generar_secuencia_aleatoria_con_contraseña(password)

        with open("llave.txt", "w", encoding='utf-8') as f:
            for fila in secuencia_aleatoria:
                f.write(f"{fila}\n")

        with open("tempfile", "w") as f:
            subprocess.run(["xxd -b "+f"{target}.tar.enc"+" | cut -d' ' -f2- | cut -d' ' -f1-7"], shell=True, stdout=f)
        
        with open("tempfile", "r") as f:
            binary_data = ''.join(char for char in f.read() if char in ['0', '1'])

        key = {}
        with open("llave.txt", "r") as key_file:
            for line in key_file:
                value, binary = line.strip().split()
                key[binary] = int(value)


        subprocess.run(["rm "+f"{target}.tar.enc"], shell=True)
        with open(f"{target}.tar.enc", "a") as encoded_file:
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting bytes to referenced decimal number") 
            block_size = 8
            for i in range(0, len(binary_data), block_size):
                block = binary_data[i:i+block_size]
                decimal_value = key.get(block)  
                decimal_output = str(decimal_value) + "\n"
                
                encoded_file.write(decimal_output)

        subprocess.run(["rm llave.txt && rm tempfile"], shell=True)
        print(bcolors.WHITE+"[" + bcolors.RED+"@" + bcolors.WHITE+"]" +bcolors.WHITE+ " Compressing...")
        subprocess.run([f"xz -9 {target}.tar.enc"], shell=True)
        print(bcolors.WHITE+"[" + bcolors.GREEN+"=" + bcolors.WHITE+"]" +bcolors.WHITE+ f" Encrypted file with padding {separacion} & saved as '{target}.tar.enc'.")

        print(bcolors.WHITE + "[" + bcolors.GREEN + "#" + bcolors.WHITE + "]" + bcolors.WHITE + " Done ")
        exit()
                
    if choice == "2": # Repeats 1 but process is reversed

        def bits_to_bytes(bit_string):
            return bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))

        def desencriptar(file, separacion):
            with open("tempfile", 'w') as f:
                subprocess.run(["xxd -b "+f"{target}.tar.enc"+" | cut -d' ' -f2- | cut -d' ' -f1-7 | tr -d ' ' | tr -d '\n'"], shell=True, stdout=f)
            
            with open("tempfile", "r") as f:
                binary_data = f.read()
                inverted_data = ''.join('1' if bit == '0' else '0' for bit in binary_data)

            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Removing random bits")    
            original_data = "".join(inverted_data[separacion::(separacion+1)])
            numeroactual = 0
            while numeroactual <= len(original_data):
                numeroactual += 8
            
            if numeroactual == len(original_data):
                decrypted_bytes = bits_to_bytes(original_data)
            else:
                numeroactual -= 8
                decrypted_bytes = bits_to_bytes(original_data[:-(len(original_data)-numeroactual)])


            subprocess.run(["rm "+f"{target}.tar.enc"], shell=True)
            with open(file, "wb") as f:
                f.write(decrypted_bytes)
    
            

        target = input(bcolors.WHITE + "\n[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " Target name (exclude .tar.enc): ")
        password = getpass(bcolors.WHITE+"[" + bcolors.GREEN+"+" + bcolors.WHITE+"]" +bcolors.WHITE+ " Passwd: ")
        separacion = int(input(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Fill *bit value: "))

        if int(separacion) < 1:
            print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be an integer equal to or greater than 1.")
            exit()

        print(bcolors.WHITE+"[" + bcolors.RED+"@" + bcolors.WHITE+"]" +bcolors.WHITE+ " Desompressing...")
        subprocess.run([f"xz -d {target}.tar.enc.xz"], shell=True)

        def generar_secuencia_aleatoria_con_contraseña(contraseña):
            # Generar la primera columna permutada según la contraseña
            primera_columna = list(range(256))
            hash_contraseña = hashlib.sha256(contraseña.encode()).digest()
            random_seed = int.from_bytes(hash_contraseña, 'big')
            random.seed(random_seed)
            random.shuffle(primera_columna)

            # Generar la segunda columna fija
            segunda_columna = [format(i, '08b') for i in range(256)]

            # Combinar las dos columnas en una lista de cadenas
            secuencia_aleatoria = [f"{primera_columna[i]} {segunda_columna[i]}" for i in range(256)]

            return secuencia_aleatoria

        secuencia_aleatoria = generar_secuencia_aleatoria_con_contraseña(password)

        with open("llave.txt", "w", encoding='utf-8') as f:
            for fila in secuencia_aleatoria:
                f.write(f"{fila}\n")

        with open(f"{target}.tar.enc", "r") as encoded_file:
            decimal_values = encoded_file.read().split("\n")

        key = {}
        with open("llave.txt", "r") as key_file:
            for line in key_file:
                value, binary = line.strip().split()
                key[binary] = int(value)

        inverse_key = {value: binary for binary, value in key.items()}
        decimal_values = [value for value in decimal_values if value.strip()]

        subprocess.run(["rm", f"{target}.tar.enc"])

        with open(f"{target}.tar.enc", "ab") as reconstructed_file:
            print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + " Converting decimal number to bytes referenced")
            for decimal_value in decimal_values:
                binary_block = inverse_key.get(int(decimal_value), "Unknown")  
                if binary_block != "Unknown":
                    decimal_value = int(binary_block, 2) 
                    reconstructed_file.write(bytes([decimal_value]))

   
        desencriptar(f"{target}.tar.enc", separacion)
        subprocess.run(["rm llave.txt && rm tempfile"], shell=True)
        
        cmd = f'pv -W {target}.tar.enc | openssl enc -aes-256-cbc -d -md sha512 -pbkdf2 -iter 1000000 -salt -in - -k "{password}" | tar xzvf - && rm {target}.tar.enc'
        
        print(bcolors.WHITE + "[" + bcolors.RED + "@" + bcolors.WHITE + "]" + bcolors.WHITE + ' Executing AES-256')
        try:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(bcolors.RED + "Error:", e.stderr.decode())
            exit()
        
        print(bcolors.WHITE+"[" + bcolors.GREEN+"=" + bcolors.WHITE+"]" +bcolors.WHITE+ f" Decrypted file saved as '{target}'.")

        print(bcolors.WHITE + "[" + bcolors.GREEN + "#" + bcolors.WHITE + "]" + bcolors.WHITE + " Done ")
        exit()
