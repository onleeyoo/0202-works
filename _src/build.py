import json,os,base64,sys,datetime
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
pw=sys.argv[1].encode(); it=200000
salt=os.urandom(16); iv=os.urandom(12)
key=PBKDF2HMAC(hashes.SHA256(),32,salt,it).derive(pw)
ct=AESGCM(key).encrypt(iv,open('items.json','rb').read(),None)
enc={"salt":base64.b64encode(salt).decode(),"iv":base64.b64encode(iv).decode(),"ct":base64.b64encode(ct).decode(),"iter":it}
t=open('template.html').read().replace('__ENC__',json.dumps(enc)).replace('__UPDATED__',datetime.date.today().strftime('%m.%d'))
os.makedirs('out',exist_ok=True); open('out/index.html','w').write(t)
