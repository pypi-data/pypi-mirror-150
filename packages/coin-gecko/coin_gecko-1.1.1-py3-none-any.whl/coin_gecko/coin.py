from bot_studio import *
dk=bot_studio.new(apiKey="ldc7Ea6A4AbpiUu4Nfbs3zt7ZPH3")
response1=dk.coingecko(url="https://www.coingecko.com/")

data_list = []

prefix = "https://www.coingecko.com"
def scraper():
    for i in response1["body"]:
        print('i',i["coin_link"])
        data_list.append(i)
        print(i["coin_link"])
        if prefix not in i["coin_link"]:
            response2 = dk.coingeckoisidedetail(url=prefix+i["coin_link"])
        else:
            response2=dk.coingeckoisidedetail(url=i["coin_link"])
        print(response2)
        for j in response2["body"]:
            res = response2.get('body', {}).get(j)
            i[j]=res
    print(data_list)
    return data_list

scraper()

