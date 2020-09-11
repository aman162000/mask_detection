import random
import string
import requests
import firebase_admin
from firebase_admin import credentials,db

#credentials for connection to firebase database
cred = credentials.Certificate('E:\Aman\Python Project\Fine Collection\payment\secretkey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://mask-detection-e7ec2.firebaseio.com/'})

#generate unique ID
unique_key = "".join(random.choices(string.ascii_lowercase+string.digits,k=6))
temp = None
ref = db.reference('Tables/')
url = "https://www.fast2sms.com/dev/bulk"
val=[]
pending=[]
names =ref.child('Names').get()
payment = db.reference('Tables/Payment')
pend = db.reference('Tables/Pending/Names')

#function to send messages
def msg(name):

    no = names[name]
    data = {unique_key: {name: no}}

    for i, j in payment.get().items():
        if type(j) is dict:
            for a, b in j.items():
                if not b in val:
                    val.append(b)
    if not no in val:
        print('pay fine')

        global temp
        temp = unique_key
        ref.child('Payment').update(data)

        payload = "sender_id=FSTSMS&language=english&route=qt&numbers=" + str(
            no) + "&message=34609&variables={#BB#}|{#EE#}&variables_values=" + unique_key + "|bit.ly/payfine"
        headers = {
            'authorization': "Gh5HYLqbR3Tt2SCjPQ9KWeIMxidXzky1VAuUJsr8EDamcwNF0p9Sho7Ok5lGiABqfsWxdnIJT1NgvVZy",
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)


    else:
        for i, j in pend.get().items():
            if type(j) is dict:
                for a, b in j.items():
                    if not b in pending:
                        pending.append(b)
                        print(pending)

        if not no in pending:
            # Send message about "Pay previous fine"

            payload = "sender_id=FSTSMS&language=english&route=qt&numbers=" + str(no) + "&message=34611"
            headers = {
                'authorization': "Gh5HYLqbR3Tt2SCjPQ9KWeIMxidXzky1VAuUJsr8EDamcwNF0p9Sho7Ok5lGiABqfsWxdnIJT1NgvVZy",
                'cache-control': "no-cache",
                'content-type': "application/x-www-form-urlencoded"
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)

            print('Pay your previous fine')

            if temp is None:
                for i, j in payment.get().items():
                    t = i
                    if type(j) is dict:
                        for a, b in j.items():
                            if a == name:
                                ref.child('Pending/Names').update({t: {name: no}})
                            else:
                                t = None
            else:
                ref.child('Pending/Names').update({temp: {name: no}})
        else:
            print('Nothing will Happen')

