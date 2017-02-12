import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt (key,filename):
	chuncksize=64*1024
	outputFile=filename+".enc"
	filesize=str(os.path.getsize(filename)).zfill(16)
	IV=Random.new().read(16)
	encryptor=AES.new(key,AES.MODE_CBC,IV)
	with open(filename,'rb')as infile:
		with open(outputFile,'wb')as outfile:
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)
			while True:
				chunck=infile.read(chuncksize)
				if len(chunck)==0:
					break
				elif len(chunck)%16!=0:
					chunck+=b' ' * (16 -(len(chunck)%16))
				outfile.write(encryptor.encrypt(chunck))



def decrypt(key,filename):
	chuncksize=64*1024
	outputFile=filename[:-4]
	with open (filename,'rb') as infile:
		filesize=infile.read(16)
		IV=infile.read(16)
	        decryptor=AES.new(key,AES.MODE_CBC,IV)
		with open(outputFile,'wb') as outfile:
			while True:
				chunck=infile.read(chuncksize)
				if len(chunck)==0:
					break

				outfile.write(decryptor.decrypt(chunck))
			outfile.truncate(int(filesize))





def getKey(password):
	hasher=SHA256.new(password.encode('utf-8'))
	return hasher.digest()

def main():
	choice=raw_input("Enter choice E or D:")
	if choice =='E':
		filename=raw_input("File to Encrypt:")
		password=raw_input("password")
		encrypt(getKey(password),filename)
		print "Done"
	elif choice== 'D':
		filename=raw_input("File to Decrypt:")
		password=raw_input("Password")
		decrypt(getKey(password),filename)
		print "Done"

	else:
		print "No Option Selected:"


main()

