from bot_studio import *
dk=bot_studio.new(apiKey="ldc7Ea6A4AbpiUu4Nfbs3zt7ZPH3")
response1=dk.coingecko(url="https://www.coingecko.com/")

data_list = []

def scraper():
    for i in response1["body"]:
        data_list.append(i)
        response2=dk.coingeckoisidedetail(url=i["coin_link"])
        for j in response2["body"]:
            res = response2.get('body', {}).get(j)
            i[j]=res
    print(data_list)
    return data_list
scraper()

