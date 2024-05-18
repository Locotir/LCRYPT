# LCRYPT: Unbreakable Encryption at the Binary Level
In the digital age, securing information at its most fundamental level is paramount. Recognizing that all data ultimately translates to binary code, LCRYPT presents a groundbreaking encryption solution designed to safeguard data integrity and confidentiality. Even with full knowledge of the encryption process, unauthorized access remains an insurmountable challenge without the corresponding decryption keys.

### Description
LCRYPT offers a robust mechanism to secure files by encrypting them at the binary level. This ensures that sensitive information remains protected against unauthorized access attempts, aligning with the highest standards of data security. The encryption process renders the content indecipherable without the appropriate keys, making it akin to deciphering a dictionary submerged in an alphabet soup.

The primary objective of LCRYPT is to provide an impenetrable barrier, effectively "wiping" the contents of a file, and enabling recovery solely through authorized decryption. This approach guarantees that even with extensive knowledge of the encryption procedure, attempting manual decryption without the requisite keys is as futile as reconstructing a vast dictionary from a jumbled mass of letters.

### Rreverse Engineering Considerations
Any attempt at reverse engineering LCRYPT-encrypted files faces significant hurdles. Without leaving identifiable marks or traces of the encryption method employed, discerning the encryption algorithm proves exceptionally challenging. Each byte within the encrypted file corresponds to a decimal number within the range of 0 to 255, representing all possible 8-bit combinations. The complexity of the encryption process goes beyond simply manipulating the position of each bit, rendering manual decryption unfeasible without the original encryption tool.

### Brute Forcing Analysis
For adversaries equipped with the LCRYPT tool, decrypting files through brute force entails exhaustive attempts with varying padding settings. However, the sheer magnitude of possible combinations, combined with the computational resources required, presents formidable obstacles. Even assuming a generous timeframe for each decryption attempt, the endeavor becomes a test of endurance.

In scenarios involving quantum computing, theoretical speed enhancements pose additional challenges. Despite speculative advancements in computational power, the exponential complexity of LCRYPT encryption remains a formidable barrier. Hypothetical comparisons underscore the monumental effort required, emphasizing the impregnability of LCRYPT's encryption methodology.



### Installation & Run
```
git clone https://github.com/Locotir/LCRYPT
cd LCRYPT
pip3 install -r requirements.txt
python LCRYPT.py
```

### Targets accepted
All type of files and folders

### I take NO responsibility
This program is provided for educational and research purposes only. The user assumes all responsibility for the use of the program. The developer is not responsible for any misuse, damage or problems caused by the program. It is strongly recommended to use this software in an ethical and legal manner. 

# Program Operation

### | Binary Shuffle

### | Reverse Binary Chain

### | Fill whith bits between each original bit

### | Convert each 8bit string to decimal (0-255):Psswd randomized

# Graphical Explanation

![diagram drawio](https://github.com/Locotir/LCRYPT/assets/71979632/5b7fac5b-3bf6-40b9-a3ef-24c0a0087db9)


# Target

![2024-05-18-192236_696x295_scrot](https://github.com/Locotir/LCRYPT/assets/71979632/18fc078e-3852-4f36-a096-ceb9904af482)

### After compressing the target, shuffling, applying bit padding, converting bytes to decimal reference numbers, and saving in binary format.

![2024-05-18-192525_712x292_scrot](https://github.com/Locotir/LCRYPT/assets/71979632/f84e40bb-97ce-4809-88d7-7b84750840ee)


# Console Preview

![2024-05-18-192505_888x609_scrot](https://github.com/Locotir/LCRYPT/assets/71979632/92ab5415-f93b-47c2-99bb-0b71b5433283)



