import base64
from time import sleep

backupmethod = ''
try:
    etoken = open('enctoken.key','r')
except FileNotFoundError:
    backupmethod = input('enctoken not found. Paste your bot token here: ')
    if backupmethod == '':
        print('You do not have the enctoken.key file.\nThis file is for the storage of your bot token.\nEither just put the bot token you get from the developer portal in token.txt, or paste it in above.')
        print('enctoken.key is used to store the encoded base64 bot token, if you paste the raw key in it, it won\'t work.\nIn that case, paste the bot token after you\'ve removed the existing enctoken.key and re-run the script.')
        exit(1)
    with open('token.txt','w+') as tokenfile:
        tokenfile.write(backupmethod)
        print('Saved token.')
        exit(0)

print('enctoken.key found, decoding...')
print('Decrypting... [0/3]',end='\r')
decrypt = etoken.read()
sleep(1)
print('Decrypting... [1/3]',end='\r')
decrypt = decrypt.encode('utf+8')
sleep(1)
print('Decrypting... [2/3]',end='\r')
decrypt = base64.b64decode(decrypt)
sleep(1)
print('Decrypting... [3/3]',end='\r')
decrypt = decrypt.decode()
sleep(1)

with open('token.txt','w+') as tokenfile:
    tokenfile.write(decrypt)

out = ''
count = 0
for i in [a for a in decrypt]:
    if count <= 10:
        out += i
    else:
        out += '*'
    count += 1
    print(out,end='\r')
    sleep(0.00003)
print(f'Decode success, result:{out}            ')