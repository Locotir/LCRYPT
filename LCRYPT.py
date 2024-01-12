from getch import getch, pause
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

choice = ""
while choice != "3":
    print(bcolors.YELLOW+"\n Options:")
    print(bcolors.GREEN+"1. Encrypter")
    print(bcolors.BLUE+"2. Decrypter")
    print(bcolors.RED+"3. Quit")

    choice = getch()


    if choice == "1":
        foldername = input(bcolors.WHITE + "\n[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " target name: ")
        cmd = f'tar -czvf - {foldername} | pv -W | openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 1000000 -salt -out {foldername}.tar.enc && rm -r {foldername}'
        print(bcolors.WHITE + "[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.RED + ' Executing command...')
        subprocess.run(cmd, shell=True)
        separacion = int(input(bcolors.WHITE + "[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " separation *bits value: "))
        
        if int(separacion) < 1:
            print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be an integer equal to or greater than 1.")
            exit()

        def encriptar(file, separacion):
            with open(file, 'rb') as content:
                data = bytearray(content.read())



            datos_encriptados = bytearray()

            for _ in range(separacion):
                datos_encriptados.extend(generar_bloque_aleatorio())

            for i in range(0, len(data), 1):
                bloque = data[i:i + 1]
                bloque_invertido = bytearray([~b & 0xff for b in bloque])
                datos_encriptados.extend(bloque_invertido)

                if i + 1 < len(data):
                    for _ in range(separacion):
                        datos_encriptados.extend(generar_bloque_aleatorio())

            for _ in range(separacion):
                datos_encriptados.extend(generar_bloque_aleatorio())

            with open(file, 'wb') as encrypted_file:
                encrypted_file.write(datos_encriptados)

            print(f"    --> Encrypted file with padding {separacion} & saved as '{file}'.")

        def generar_bloque_aleatorio():
            return bytearray([random.randint(0, 255)])

        encriptar(f"{foldername}.tar.enc", separacion)


        print(bcolors.WHITE + "[" + bcolors.GREEN + "#" + bcolors.WHITE + "]" + bcolors.WHITE + " Done ")
                
    if choice == "2":
        separacion = int(input(bcolors.WHITE + "\n[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " separation *bits value: "))
        if int(separacion) < 1:
            print(bcolors.WHITE + "[" + bcolors.RED + "!" + bcolors.WHITE + "]" + bcolors.WHITE + " The fill value must be an integer equal to or greater than 1.")
            exit()

        def desencriptar(file, separacion):
            with open(file, 'rb') as content:
                data = bytearray(content.read())

            datos_desencriptados = bytearray()

            datos_encriptados_invertidos = bytearray([~b & 0xff for b in data])

            for i in range(separacion, len(datos_encriptados_invertidos) - separacion, 1):
                if i % (separacion + 1) == separacion:
                    bloque = datos_encriptados_invertidos[i:i + 1]
                    bloque_invertido = bytearray([~b & 0xff for b in bloque])
                    datos_desencriptados.extend(bloque_invertido)

            datos_desencriptados_invertidos = bytearray([~b & 0xff for b in datos_desencriptados])

            with open(file, 'wb') as decrypted_file:
                decrypted_file.write(datos_desencriptados_invertidos)

            print(f"    --> Decrypted file saved as '{file}'.")

        foldername = input(bcolors.WHITE + "[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.WHITE + " target name (exclude .tar.enc): ")
        desencriptar(f"{foldername}.tar.enc", separacion)
        cmd = f'pv -W {foldername}.tar.enc | openssl enc -aes-256-cbc -d -md sha512 -pbkdf2 -iter 1000000 -salt -in - | tar xzvf - && rm {foldername}.tar.enc'  
        print(bcolors.WHITE + "[" + bcolors.GREEN + "+" + bcolors.WHITE + "]" + bcolors.RED + 'Executing command...')
        subprocess.run(cmd, shell=True)

        print(bcolors.WHITE + "[" + bcolors.GREEN + "#" + bcolors.WHITE + "]" + bcolors.WHITE + " Done ")
        exit()
    
    else:
        exit()
