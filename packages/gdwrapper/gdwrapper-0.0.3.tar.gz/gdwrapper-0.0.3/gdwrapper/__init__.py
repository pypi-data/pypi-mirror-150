# __init__.py
__version__ = "0.0.3"

import hashlib
import requests
from itertools import cycle
import base64

head = {
    'Accept-Encoding': None,
    'User-Agent': "",
    'Accept': '*/*',
    'Accept-Language': None,
    'Content-Length': '82',
    'Content-Type': 'application/x-www-form-urlencoded'
}


def get_userinfo(username, proxy=None):
    url = "http://www.boomlings.com/database/getGJUsers20.php"
    try:
        r = f"gameVersion=21&binaryVersion=35&gdw=0&str={username}&total=0&page=0&secret=Wmfd2893gb7".encode()
        if proxy == None:      
            data = requests.post(url=url, data=r, headers=head).content.decode()
        else:
            data = requests.post(url=url, data=r, headers=head, proxies=proxy).content.decode()
        data = data.split(":")
        print(f"""Account-ID: {data[21]}
User-ID: {data[3]}
Stars: {data[23]}
Diamonds: {data[17]}
Secret-Coins: {data[5]}
User-Coins: {data[7]}
Demons: {data[27].split("#")[0]}
Creator-Points: {data[25]}""")
    except:
        print("Type in a valid Username.")


# def get_levelpassword(levelid, proxy=None):
#     try:
#         url = "http://c8o.altervista.org/password.php"
#         r = f"LevelID={str(levelid)}"
#         print(r)
#         if proxy == None:
#             data = requests.post(url=url, data=r, headers=head).content.decode()
#             print("e")
#         else:
#             data = requests.post(url=url, data=r, headers=head, proxies=proxy).content.decode()
#             print("e2")
#         if data == "":
#             print("The Level doesn't have a Password.")
#         print(data)
#     except:
#         print("Type in a valid Level-ID.")


def comment(username, password, levelid, comment, proxy=None):
    levelid = str(levelid)
    try:
        url = "http://www.boomlings.com/database/getGJUsers20.php"
        r = f"gameVersion=21&binaryVersion=35&gdw=0&str={username}&total=0&page=0&secret=Wmfd2893gb7".encode()
        data = requests.post(url=url, data=r, headers=head).content.decode()
        data = data.split(":")
        accountid = data[21]
    except:
        print("Type in a valid Username.")

    def xor(data, key):
        xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
        return base64.b64encode(xored.encode())

    def unxor(xored, key):
        data = base64.b64decode(xored.encode()).decode()
        unxored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
        return unxored
    
    gjp = xor(password, "37526").decode()
    
    comment = base64.b64encode(comment.encode()).decode()
    m = hashlib.sha1(f"{username}{comment}{levelid}00xPT6iUrtws0J".encode()).hexdigest()
    chk = xor(m, "29481").decode()
    url = "http://www.boomlings.com/database/uploadGJComment21.php"
    r = f"gameVersion=21&binaryVersion=35&gdw=0&accountID={accountid}&gjp={gjp}&userName={username}&comment={comment}&secret=Wmfd2893gb7&levelID={levelid}&chk={chk}".encode()
    if proxy == None:
        data = requests.post(url=url, data=r, headers=head).content.decode()
    else:
        data = requests.post(url=url, data=r, headers=head, proxies=proxy).content.decode()
    if data == "-1":
        print("Couldn't send the comment. Please check if the Usernames matches the Password or the comment isn't to long and try it again.")
    elif data == "1":
        print("Successfully sent a Comment.")
    else:
        print(data)


def send_message(username, password, ToUsername, title, message, proxy=None):
    try:
        url = "http://www.boomlings.com/database/getGJUsers20.php"
        r = f"gameVersion=21&binaryVersion=35&gdw=0&str={username}&total=0&page=0&secret=Wmfd2893gb7".encode()
        r2 = f"gameVersion=21&binaryVersion=35&gdw=0&str={ToUsername}&total=0&page=0&secret=Wmfd2893gb7".encode()
        data = requests.post(url=url, data=r, headers=head).content.decode()
        data2 = requests.post(url=url, data=r2, headers=head).content.decode()
        data = data.split(":")
        data2 = data2.split(":")
        accountid = data[21]
        accountid2 = data2[21]
    except Exception as e:
        print(e)
        print("Type in a valid Username.")

    def xor(data, key):
        xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
        return base64.b64encode(xored.encode())

    def unxor(xored, key):
        data = base64.b64decode(xored.encode()).decode()
        unxored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
        return unxored
    
    gjp = xor(password, "37526").decode()
    subject = base64.b64encode(title.encode()).decode()
    body = xor(message, "14251").decode()
    url = "http://www.boomlings.com/database/uploadGJMessage20.php"
    r = f"gameVersion=21&binaryVersion=35&gdw=0&accountID={accountid}&gjp={gjp}&toAccountID={accountid2}&subject={subject}&body={body}&secret=Wmfd2893gb7".encode()
    if proxy == None:
        data = requests.post(url=url, data=r, headers=head).content.decode()
    else:
        data = requests.post(url=url, data=r, headers=head, proxies=proxy).content.decode()
    if data == "-1":
        print("Couldn't send the Message. Please check if the Usernames matches the Password or the Message isn't to long and try it again.")
    elif data == "1":
        print("Successfully sent a Message.")
    else:
        print(data)


def login(username, password, proxy=None):
    url = "http://www.boomlings.com/database/accounts/loginGJAccount.php"
    r = f"udid=S15212864471883312752224026790081311001&userName={username}&password={password}&sID=76561200095338154&secret=Wmfv3899gc9".encode()
    if proxy == None:
        data = requests.post(url=url, data=r, headers=head).content.decode()
    else:
        data = requests.post(url=url, data=r, headers=head, proxies=proxy).content.decode()
    if data == "-1":
        print("Couldn't login.")
    else:
        print("Logged in.")


def like_level(username, password, levelid, like, proxy=None):
    levelid = str(levelid)
    try:
        url = "http://www.boomlings.com/database/getGJUsers20.php"
        r = f"gameVersion=21&binaryVersion=35&gdw=0&str={username}&total=0&page=0&secret=Wmfd2893gb7".encode()
        data = requests.post(url=url, data=r, headers=head).content.decode()
        data = data.split(":")
        userid = data[3]
        accountid = data[21]
    except Exception as e:
        print(e)
        print("Type in a valid Username or Level-ID.")

    def xor(data, key):
        xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
        return base64.b64encode(xored.encode())

    def unxor(xored, key):
        data = base64.b64decode(xored.encode()).decode()
        unxored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
        return unxored
    
    gjp = xor(password, "37526").decode()

    if like == 0:
        like_ = 0
    elif like == 1:
        like_ = 1
    else:
       print("Type in a valid Like-Syntax.")

    m = hashlib.sha1(f"0{levelid}{like_}1A587gjOPKL{accountid}ffffffff-bde6-58df-ffff-ffffe5b9c0d7{userid}ysg6pUrtjn0J".encode()).hexdigest()
    chk = xor(m, "58281").decode()
    r = f"gameVersion=20&binaryVersion=34&gdw=0&accountID=" +str(accountid)+ "&gjp=" +str(gjp)+ "&udid=ffffffff-bde6-58df-ffff-ffffe5b9c0d7&uuid=" +str(userid)+ "&itemID=" +str(levelid)+ "&like=" +str(like)+ "&type=1&secret=Wmfd2893gb7&special=0&rs=A587gjOPKL&chk=" +str(chk)
    r = r.encode()
    if proxy == None:
        data = requests.post(url="http://www.boomlings.com/database/likeGJItem211.php", data=r, headers=head).content.decode()
    else:
        data = requests.post(url="http://www.boomlings.com/database/likeGJItem211.php", data=r, headers=head, proxies=proxy).content.decode()
    if data == "-1":
        print("Couldn't send a Like.")
    elif data == "1":
        print("Successfully sent a Like.")
    else:
        print(data)
