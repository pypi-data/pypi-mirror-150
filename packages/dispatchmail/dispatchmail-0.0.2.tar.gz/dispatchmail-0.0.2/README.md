# mailing
Light, simple, mailing api written in Python

# Disclaimer

Not all smtp mail server will allow for Python to make a connection 

As of May 30, 2022, Google will no longer support the use of third-party apps or devices
and the smtp.gmail.com server will be broken. Recommend using local smtp mail server,
default SendMail mailing settings are `Mailing=('localhost', 587)` but this can be changed.

# Usage
```python
from dispatchmail import EmailConst as Mail

# NOTE: this is unsecure, consider hashing and storing your password!
login = ("example@gmail.com", "password")

mail = Mail("Some Example Mail", "other@gmail.com", "example@gmail.com", "Hello, World!")
mail.SendMail(login, Mailing=("smtp.gmail.com", 587))
```

dispatchmail also supports the ability to send to multiple users, just specify `To` as a list

```python
mail = Mail("Some Example Mail", ["other@gmail.com", "user@gmail.com"], "example@gmail.com", "Hello, World!")
```

# TODO

- [ ] Add use of configuration file, JSON / .ini
- [ ] Host a small development smtp server for debugging
