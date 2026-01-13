import requests

SUBDOMAIN = "infoeasypaymentsonline"  # без .amocrm.ru
URL = f"https://{SUBDOMAIN}.amocrm.ru/oauth2/access_token"

DATA = {
    "client_id": "51103657-c003-4a82-b56a-314b6f399d8e",
    "client_secret": "oKpH6uAB9LWOOlvuliST9cxTvWK67YVEtvPbmVeOpQiOqHvepp4lXIg1VihaNMJM",
    "grant_type": "authorization_code",
    "code": "def502003f02e78a46fb025dc125258997b763af37b39899aebcf849354bea55c4bf6fc2cf7baa5396d4f9c6900509d2478cc003fd1cf881a5625be5c86084fd19daaea1bf10f71fc07616c7c27746f0660cdd2db4927f32fdd63ed0e078305377ee14086131ac59606e18064fd50d3685922c81420132436c62948b72785b995342b1c1362948e5c7bc24820e0257568973b795cc8d89b026eb137cfe34e77440acd2741f6791ebf9cb05f10892d124ef15c1ccb552a69e74ea3fdf5658ff41f24d372b65132145bcf001d08425a3cd9dece552293d56673b3f961831e5d857740af55f1a66219b878c0e89d0c37fa0e53aa8cd0c3ccf98ae919834b6de8ba9c39353105be6d4d22ed3ce814cdad36b079a708b8b67568432605d21f7bb26f11c1f7f2ad55d4df862a2368c16926f42e6b98a5843808d31f54f1caa5a6bde99b5ffa8f18223614ab1e7a5e9274acc0c952a0cf87367ed02c0943ac1de17ed387840f11e9d2a61dbf397fea32ed051274d54d59a74ea01dfc6bbb8d929042f420061fe001613d7ce5c4ac3256fc13ea079e02b44bd97b92ad786fd867e69356cc519747e44e11b5bd1f0b3cec77ff69a7599e0ee55d183b9873262207ecf1ceb21fde81a47140b61294e7ee1d35e74d9cd7d37307e86",
    "redirect_uri": "https://easypayments.online/",
}

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "amoCRM-oAuth-client/1.0",
}

response = requests.post(URL, json=DATA, headers=HEADERS, timeout=15)

print("HTTP:", response.status_code)
print("RAW:", response.text)

if response.status_code not in (200, 201, 202, 204):
    raise RuntimeError(f"OAuth error: {response.status_code} {response.text}")

payload = response.json()

access_token = payload["access_token"]
refresh_token = payload["refresh_token"]
token_type = payload["token_type"]
expires_in = payload["expires_in"]

print("ACCESS:", access_token)
print("REFRESH:", refresh_token)
print("TYPE:", token_type)
print("EXPIRES IN:", expires_in)
