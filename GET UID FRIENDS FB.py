import requests

access_token = 'EAABwzLixnjYB...'
r = requests.request('GET',f'https://graph.facebook.com/v17.0/me/friends?access_token={access_token}&pretty=1&limit=5000')
result = r.json()
for data in result['data']:
    with open('full.user.txt','a+',encoding='utf-8') as f:
        f.write(f'{data["id"]}|{data["name"]}\n')
    with open('uid.user.txt','a+',encoding='utf-8') as f:
        f.write(f'{data["id"]}\n')
