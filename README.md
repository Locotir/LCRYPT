# LCRYPT
Interesting form of obfuscation in AES-256 post encrypted files

## Requirements
--> Openssl
--> getch==1.0

## Targets accepted
All type of files and folders

## I take NO responsibility
This program is provided for educational and research purposes only. The user assumes all responsibility for the use of the program. The developer is not responsible for any misuse, damage or problems caused by the program. It is strongly recommended to use this software in an ethical and legal manner, respecting local laws and regulations.

# Program operation

## Encrypt whith AES-256
``` 
openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 1000000 -salt -out {target}.tar.enc
```
