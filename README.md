# LCRYPT
Interesting form of obfuscation in AES-256 post encrypted files

### Requirements
Openssl & getch==1.0

### Targets accepted
All type of files and folders

### I take NO responsibility
This program is provided for educational and research purposes only. The user assumes all responsibility for the use of the program. The developer is not responsible for any misuse, damage or problems caused by the program. It is strongly recommended to use this software in an ethical and legal manner, respecting local laws and regulations.

# Program operation

### Encrypt whith AES-256
``` 
openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 1000000 -salt -out {target}.tar.enc
```
### Reverse binary chain

### Fill whith n bytes between

### Graphical explanation

![2024-01-12-00:53:50-screenshot](https://github.com/Locotir/LCRYPT/assets/71979632/f0cb2ad5-5a7e-42ed-a32e-090217fb0719)

### Target

![2024-01-12-20:45:28-screenshot](https://github.com/Locotir/LCRYPT/assets/71979632/1de733f2-8155-4b87-9733-befaa434027f)

### After AES-256

![2024-01-12-20:47:04-screenshot](https://github.com/Locotir/LCRYPT/assets/71979632/cd271aa0-5fee-44f4-9a71-ee2c2729c11d)

### After *Byte random bytes refilled [ 2 in this example ]

![2024-01-12-20:51:35-screenshot](https://github.com/Locotir/LCRYPT/assets/71979632/df2a8806-aaa1-4a79-aed8-5b06587c5be2)

### Console preview

![2024-01-12-20:51:45-screenshot](https://github.com/Locotir/LCRYPT/assets/71979632/0e7e3297-6d6a-4aeb-8c51-bb7ba5bdbba7)

### All the process on hex content view

![2024-01-12-20:55:32-screenshot](https://github.com/Locotir/LCRYPT/assets/71979632/ce1396a0-5a0f-4b69-aa78-3a91aa9ec03d)


