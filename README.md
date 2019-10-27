# SecureFileUpload
Secure File Upload Client Server using SHA-256

### To Run:
Open Terminal in the Directory SecureFileUpload

```sh
$: cd Server/
$Server/: python3 Server.py
```

The server uses **flask-restplus** which has a swagger gui, it will open at 5000 port on local host and show a swagger documentation which you can test out.
other libraries used:
- **pycryptodome** [Please do not install crypto or pycrypto :these will create an error as they have similar named libraries, if you have then uninstall them before installing pycryptodome]
- **flask**

In a seperate Terminal 

```sh
$: cd Client/
$Client/: python3 Client.py
```

