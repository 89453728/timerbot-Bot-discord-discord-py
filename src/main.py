# base url: 
# https://discord.com/api


import requests
# https://discord.com/api/v8/channels/827625180745564180/messages

payload = {
    'content': "hello world"
}
headers = {
    'authorization': "ODI3NjEwODQ2MTg0MjEwNDUy.YGdiqQ.nnm2-WgfEMxgSfpJPz-0FUSuAAE"
}
channel_id = 827617020437987368

r = requests.post("https://discord.com/api/v8/channels/{}/messages".format(channel_id), data=payload, headers=headers)
print(r.status_code)
