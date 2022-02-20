


from cryptography.fernet import Fernet
import subprocess
import base64
global fernetKey
keyGen = bytes(subprocess.getoutput('cat /etc/machine-id'),'UTF-8')
fernetKey = Fernet(base64.urlsafe_b64encode(keyGen))
print('cat /etc/machine-id')
print(keyGen)
print(fernetKey)
