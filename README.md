[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org) [![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com) [![Arch](https://img.shields.io/badge/Arch%20Linux-1793D1?logo=arch-linux&logoColor=fff&style=for-the-badge)](https://archlinux.org) [![Windows 11](https://img.shields.io/badge/Windows%2011-%230079d5.svg?style=for-the-badge&logo=Windows%2011&logoColor=white)](https://www.microsoft.com/es-es/windows/windows-11?r=1) [![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.me/locotir)

# LCRYPT: Unbreakable Binary-Level Encryption

In the digital age, securing data at its core is crucial. LCRYPT offers a revolutionary encryption solution that protects data at the binary level, ensuring integrity and confidentiality. Unauthorized access is impossible without the decryption keys.

### Description
LCRYPT encrypts files at the binary level, making data indecipherable without the correct keys. This method provides top-tier security, rendering manual decryption futile without the appropriate keys. LCRYPT-encrypted files resist reverse engineering due to their complexity. Each byte is shuffled randomly with a dynamic password and corresponds to a value between 0 and 255, shuffled, and also if the user decides so, it can add a random padding for each original bit, lenght defined by user. Finally an XOR Key string matching the same lenght of the total bits of the result is applied, all this steps results on complicating decryption attempts without the original tool. Even with the LCRYPT tool, brute force decryption is impractical due to the vast number of possible combinations and the required computational resources. The encryption's complexity remains a significant barrier, even against advancements in quantum computing.

**Disclaimer**: This tool does not leave any identifiable signature or trace that could be linked back to the tool or its author. The resulting encryption cannot be analyzed or reverse-engineered to understand the algorithm's nature without access to the program's source code.


### Installation & Run
```
git clone https://github.com/Locotir/LCRYPT
cd LCRYPT
pip3 install -r requirements.txt
python LCRYPT.py
```

### Targets accepted
All type of files and folders (The lighter, the better):                                                                                                                                          
· **Text Files** -> .txt .docx .pdf...                                                                                                                                          
· **Data Files** -> .xls .xlsx .csv...                                                                                                                                          
. **Small Databases** -> .sql .db .mdb...                                                                                                                                          
· **Image Files** -> .png .jpg .gif...                                                                                                                                          
· **Audio Files** -> .mp3 .wav...                                                                                                                                          
· **Video Files** -> .mp4 .mkv .avi...                                                                                                                                          
· **Presentation Files** -> .ppt .pptx...                                                                                                                                          
· **Programming Files** -> .py .c .cpp...                                                                                                                                          
· **Config Files** -> .cfg .ini...                                                                                                                                          
· **Key Files** -> .key .cer                                                                                                                                          
· **Compressed Files** -> .zip .rar...                                                                                                                                          

### I take NO responsibility in misuse
This program is provided for educational and research purposes only. The user assumes all responsibility for the use of the program. The developer is not responsible for any misuse, damage or problems caused by the program. It is strongly recommended to use this software in an ethical and legal manner.


# Program Operation
> [!NOTE]
> **[@]** Binary Shuffle     
> **[@]** Reverse Binary Chain         
> **[@]** Fill with bits between each original bit            
> **[@]** Convert each 8bit string to decimal (0-255):Psswd randomized           
> **[@]** XOR Key applied as long as entire file bit string            

# Graphical Explanation

![explained drawio (1)](https://github.com/Locotir/LCRYPT/assets/71979632/addd9770-aeef-4d20-956e-31665ffb31f8)


# Target

![2024-06-06-200547_702x294_scrot](https://github.com/Locotir/LCRYPT/assets/71979632/79ed003a-82a9-4565-832e-0f6e29695ff8)


### After compresion, shuffling, reverse, padding, bytes to decimal number saved in binary format and XOR Key finally applied:


![2024-06-06-200703_710x304_scrot](https://github.com/Locotir/LCRYPT/assets/71979632/a67c8673-8df6-4c86-ac63-3d1e54f4f47b)


# Console Preview

![2024-06-06-200619_954x608_scrot](https://github.com/Locotir/LCRYPT/assets/71979632/f71bee13-13fb-40a9-983b-f794fd4295cb)

# Breakthrough Attempt
## Scenario
For a simpler visualization, in this case we are not using TAR as it leads to a bigger file for the small files.

Target: Text file, contains 'a'
- Content in binary: 01100001 00001010
- Content in HEX: 610a

Encrypted with padding = 1:
- Content in binary: 10011110 11111100 00110010 10111101
- Content in HEX: 9efc 32bd

## Process
- 1. Original bits: 01100001 00001010
- 2. Byte random sequence: [1, 2, 5, 3, 0, 6, 4, 7] & [7, 2, 6, 5, 3, 1, 4, 0] : Randomized with the passwd for each byte
- 3. Result reversed: 00111110 11011101
- 4. Adding Padding: 00000111 01011110 11010011 11010011 : Each bit generated is also random
- 5. Byte to decimal (Each list is randomized with passwd+(padding value)):
- 00000111 : 142 | 01011110 : 167 | 11010011 : 151 | 11010011 : 151
- 6. Decimal to byte:
- 142 : 10001110 | 167: 10100111 | 151 : 10010111 | 151 : 10010111
- 7. **Result:**       10001110 10100111 10010111 10010111
- 8. **XOR Key:**      00010000 01011011 10100101 00101010
- 9. **Final Result:** 10011110 11111100 00110010 10111101

## Break Attempt
The result file is never gonna have metadata about the original file.
Also the lack of a file type patterns also disapears with XOR Key.
From here, any atempt for decrypting the file is impossible.

Let's imagine, the atacker knows the encryption method and the original file size:
  - As in this case, the file is double the size, so padding is 1.
  - If he attempts to remove the padding, the result will be: 01101110 01000111
  - ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤthe original looks: 01100001 00001010 (not even close obviously)
  - In just 2 bytes of 8bits exists 65.536 possible combinations.
  - The correct way to decrypt the file is by having the decimal to byte reference list which is generated with passwd+(padding value)
  
  - Only if the attacker knows exactly the start or end of a byte in the file:
      He would need to create the original XOR Key which is the same lenght as the file, and after replicate each unique list 1-256 of 256 lenght and then remove padding and verify if the original byte is there.
      This sounds possible, but it really dosen't make sense as the possible unique lists is: ```857817775342842654119082271681232625157781520279485619859655650377269452553147589377440291360451408450375885342336584306157196834693696475322289288497426025679637332563368786442675207626794560187968867971521143307702077526646451464709187326100832876325702818980773671781454170250523018608495319068138257481070252817559459476987034665712738139286205234756808218860701203611083152093501947437109101726968262861606263662435022840944191408424615936000000000000000000000000000000000000000000000000000000000000000```
      So, here also there is no way to decrypt the file.

- The last option and only possible one is by bruteforcing the decryption process from the program.
  For the smallests files, the execution time is aprox 0.05s.
  If the attacker uses a 14M passwords dictionary: ~8 days would take.
  But using a password long enough and not listed in any dictionary, it would take for ever.
  
        



