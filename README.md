![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Arch](https://img.shields.io/badge/Arch%20Linux-1793D1?logo=arch-linux&logoColor=fff&style=for-the-badge) ![Windows 11](https://img.shields.io/badge/Windows%2011-%230079d5.svg?style=for-the-badge&logo=Windows%2011&logoColor=white) ![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)

# LCRYPT: Unbreakable Binary-Level Encryption

In the digital age, securing data at its core is crucial. LCRYPT offers a revolutionary encryption solution that protects data at the binary level, ensuring integrity and confidentiality. Unauthorized access is impossible without the decryption keys.

### Description
LCRYPT encrypts files at the binary level, making data indecipherable without the correct keys. This method provides top-tier security, rendering manual decryption futile without the appropriate keys. LCRYPT-encrypted files resist reverse engineering due to their complexity. Each byte is shuffled randomly with a dynamic password and corresponds to a value between 0 and 255, complicating decryption attempts without the original tool. Even with the LCRYPT tool, brute force decryption is impractical due to the vast number of possible combinations and the required computational resources. The encryption's complexity remains a significant barrier, even against advancements in quantum computing.


### Installation & Run
```
git clone https://github.com/Locotir/LCRYPT
cd LCRYPT
pip3 install -r requirements.txt
python LCRYPT.py
```

### Targets accepted
All type of files and folders

### I take NO responsibility in misuse
This program is provided for educational and research purposes only. The user assumes all responsibility for the use of the program. The developer is not responsible for any misuse, damage or problems caused by the program. It is strongly recommended to use this software in an ethical and legal manner.


# Program Operation
> [!NOTE]
> [@] Binary Shuffle     
> [@] Reverse Binary Chain         
> [@] Fill with bits between each original bit            
> [@] Convert each 8bit string to decimal (0-255):Psswd randomized            

# Graphical Explanation

![diagram drawio](https://github.com/Locotir/LCRYPT/assets/71979632/5b7fac5b-3bf6-40b9-a3ef-24c0a0087db9)


# Target

![2024-05-18-192236_696x295_scrot](https://github.com/Locotir/LCRYPT/assets/71979632/18fc078e-3852-4f36-a096-ceb9904af482)

### After compresion, shuffling, reverse, padding and bytes to decimal number saved in binary format:


![2024-05-18-192525_712x292_scrot](https://github.com/Locotir/LCRYPT/assets/71979632/f84e40bb-97ce-4809-88d7-7b84750840ee)


# Console Preview

![2024-05-18-192505_888x609_scrot](https://github.com/Locotir/LCRYPT/assets/71979632/92ab5415-f93b-47c2-99bb-0b71b5433283)

# Breakthrough Attempt
## Scenario
For a simpler visualization, in this case we are not using TAR as it leads to a bigger file for the small files.

Target: Text file, contains 'a'
        Content in binary: 01100001 00001010
        Content in HEX: 610a

Encrypted with padding = 1:
        Content in binary: 01011000 00001011 00010111 01110110
        Content in HEX: 580b 1776

## Process
- 1. Original bits: 01100001 00001010
- 2. Byte random sequence: [2, 1, 6, 0, 3, 5, 7, 4] : Randomized with the passwd
- 3. Result reversed: 00111101 11011110
- 4. Adding Padding: 00100101 11010001 01110001 11011110 : Each bit generated is also random
- 5. Byte to decimal: 00100101 : 88   Each list is randomized with passwd+(padding value)
                    11010001 : 11
                    01110001 : 23
                    11011110 : 118
- 6. Decimal to byte:  88 : 01011000
                     11 : 00001011
                     23 : 00010111
                    118 : 01110110
- 7. Result: 01011000 00001011 00010111 01110110

## Break Attempt
The result file is never gonna have metadata about the original file.
Also the lack of a file type patterns also disapears adding !=0 padding.
From here, any atempt for decrypting the file is impossible.

Let's imagine, the atacker knows the encryption method and the original file size:
  - As in this case, the file is double the size, so padding is 1.
  - If he attempts to remove the padding, the result will be: 11000001 01111110
                                        - the original looks: 01100001 00001010 (not even close obviously)
  - In just 2 bytes of 8bits exists 65.536 possible combinations.
  - The correct way to decrypt the file is by having the decimal to byte reference list which is generated with passwd+(padding value)
  
  - Only if the attacker knows exactly the start or end of a byte in the file:
      He would need to create each unique list 1-256 of 256 lenght and then remove padding and verify if the original byte is there.
      This sounds possible, but it really dosen't make sense as the possible unique lists is: ```857817775342842654119082271681232625157781520279485619859655650377269452553147589377440291360451408450375885342336584306157196834693696475322289288497426025679637332563368786442675207626794560187968867971521143307702077526646451464709187326100832876325702818980773671781454170250523018608495319068138257481070252817559459476987034665712738139286205234756808218860701203611083152093501947437109101726968262861606263662435022840944191408424615936000000000000000000000000000000000000000000000000000000000000000```
      So, here also there is no way to decrypt the file.

- The last option and only possible one is by bruteforcing the decryption process from the program.
  For the smallests files, the execution time is aprox 0.05s.
  If the attacker uses a 14M passwords dictionary: ~8 days would take.
  But using a password long enough and not listed in any dictionary, it would take for ever.
  
        



