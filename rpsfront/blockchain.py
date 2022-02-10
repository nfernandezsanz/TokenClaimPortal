import requests
import time

def CantTokens(wallet):

    headers = {
        'accept': 'application/json',
        'X-API-Key': '#ApiKey',
    }
    retry = 3
    suc   = 0
    while(suc != 1 and retry > 0):
        retry    -= 1
        response = requests.get('https://deep-index.moralis.io/api/v2/' + wallet + '/erc20?chain=bsc&token_addresses=0x267022751e06d97b9ee4e5f26cc1023670bdb349', headers=headers)
        try:
            return float(response.json()[0]['balance']) / float(10**(int(response.json()[0]['decimals'])))    
        except:
            if(response.ok == True):
                return 0
            else:
                time.sleep(0.5)
    return -1

def get_NFTS_V2(wallet):
        headers = {
            'accept': 'application/json',
            'X-API-Key': '#ApiKey',
        }
        link = 'https://deep-index.moralis.io/api/v2/' + wallet + '/nft/' + "0xa3599134b1af6672d3788e561c61c5dca62f8244" + '?chain=bsc&format=decimal'
        suc = 0
        retry = 3
        while(suc != 1 and retry > 0):
            retry    -= 1
            response = requests.get(link, headers=headers)
            try:
                resp = response.json()['result']
                return resp
            except:
                time.sleep(0.1)
                pass
        return -1 

def get_NFTS_V1(wallet):
        headers = {
            'accept': 'application/json',
            'X-API-Key': '#ApiKey',
        }
        link = 'https://deep-index.moralis.io/api/v2/' + wallet + '/nft/' + "0xFeCcBc6dFfEf9E456E501F936FeFAB5B96a8BF9E" + '?chain=bsc&format=decimal'
        suc = 0
        retry = 3
        while(suc != 1 and retry > 0):
            retry    -= 1
            response = requests.get(link, headers=headers)
            try:
                resp = response.json()['result']
                return resp
            except:
                time.sleep(0.1)
                pass
        return -1
        
def CantNFTs(wallet):
    try:
        nfts_v1 = get_NFTS_V1(wallet)
        nfts_v2 = get_NFTS_V2(wallet)
        sum = len(nfts_v1) + len (nfts_v2)
        if(sum > 0):
            return sum
        else:
            return 0
    except:
        return 0
