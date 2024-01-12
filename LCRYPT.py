from getch import getch
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
    sys.exit("Exiting...")

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
        target = input(bcolors.WHITE + "\n[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " target name: ")

        # Set the AES-256 & remove original target
        cmd = f'tar -czvf - {target} | pv -W | openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 1000000 -salt -out {target}.tar.enc && rm -r {target}'
        print(bcolors.WHITE + "[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.RED + ' Executing command...')

        # Execute
        subprocess.run(cmd, shell=True)

        # Define the n of random bytes between original-encrypted ones
        separacion = int(input(bcolors.WHITE + "[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " fill *byte value: "))

        if int(separacion) < 1:
            print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be an integer equal to or greater than 1.")
            exit()

        def encriptar(file, separacion):
            with open(file, 'rb') as content:
                data = bytearray(content.read())

            # Target content in binary
            datos_encriptados = bytearray()

            for _ in range(separacion):
                datos_encriptados.extend(generar_bloque_aleatorio())

            for i in range(0, len(data), 1):
                bloque = data[i:i + 1]
                # Reverse the block
                bloque_invertido = bytearray([~b & 0xff for b in bloque])
                datos_encriptados.extend(bloque_invertido)

                # If not the last byte, adds additional random blocks
                if i + 1 < len(data):
                    for _ in range(separacion):
                        datos_encriptados.extend(generar_bloque_aleatorio())
    
            # Add random blocks to the end of the encrypted file
            for _ in range(separacion):
                datos_encriptados.extend(generar_bloque_aleatorio())

            # write changes
            with open(file, 'wb') as encrypted_file:
                encrypted_file.write(datos_encriptados)

            print(f"    --> Encrypted file with padding {separacion} & saved as '{file}'.")

        def generar_bloque_aleatorio():
            return bytearray([random.randint(0, 255)])

        encriptar(f"{target}.tar.enc", separacion)

        print(bcolors.WHITE + "[" + bcolors.GREEN + "#" + bcolors.WHITE + "]" + bcolors.WHITE + " Done ")
                
    if choice == "2":

        # Reverse the steps
        separacion = int(input(bcolors.WHITE + "\n[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " fill *byte value: "))

        if int(separacion) < 1:
            print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be an integer equal to or greater than 1.")
            exit()

        def desencriptar(file, separacion):
            with open(file, 'rb') as content:
                data = bytearray(content.read())

            # Target content in binary
            datos_desencriptados = bytearray()
            # Reverse the block
            datos_encriptados_invertidos = bytearray([~b & 0xff for b in data])
          
            # Iterate over the reversed data to reconstruct the encripted-AES-256 content
            for i in range(separacion, len(datos_encriptados_invertidos) - separacion, 1):
                if i % (separacion + 1) == separacion:
                    bloque = datos_encriptados_invertidos[i:i + 1]
                    bloque_invertido = bytearray([~b & 0xff for b in bloque])
                    datos_desencriptados.extend(bloque_invertido)

            datos_desencriptados_invertidos = bytearray([~b & 0xff for b in datos_desencriptados])

            with open(file, 'wb') as decrypted_file:
                decrypted_file.write(datos_desencriptados_invertidos)

            print(f"    --> Decrypted file saved as '{file}'.")

        target = input(bcolors.WHITE + "[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " target name (exclude .tar.enc): ")

        # Start removing filler bytes and invert the blocks
        desencriptar(f"{target}.tar.enc", separacion)

        # Finally, decrypt the AES-256 encrypted target
        cmd = f'pv -W {target}.tar.enc | openssl enc -aes-256-cbc -d -md sha512 -pbkdf2 -iter 1000000 -salt -in - | tar xzvf - && rm {target}.tar.enc'
        
        print(bcolors.WHITE + "[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.RED + 'Executing command...')
        subprocess.run(cmd, shell=True)

        print(bcolors.WHITE + "[" + bcolors.GREEN + "#" + bcolors.WHITE + "]" + bcolors.WHITE + " Done ")
        exit()
    
    else:
        exit()
