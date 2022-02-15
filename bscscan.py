from datetime import datetime
import json
import os
import pandas as pd
import requests


# Variables
dt = datetime.now().strftime("%y%m%d-%H%M%S")
endpoint = "https://api.bscscan.com/api"


def main():
    print("Choose an option:")
    print("(1) Balance of one or more addresses")
    print("(2) Normal transactions of an address")
    print("(3) Internal transactions of an address")
    print("(4) BEP-20 transfers of an address")
    print("(5) BEP-721 (NFT) transfers of an address")
    choose = input()

    addresses = list(
        input("Enter the bsc addresses separated by comma: ").strip().split(","))

    if choose == "1":
        get_balance_by_address(addresses)
    elif choose == "2":
        get_normal_transactions_by_address(addresses[0])
    elif choose == "3":
        get_internal_transactions_by_address(addresses[0])
    elif choose == "4":
        get_bep20_token_transfers(addresses[0])
    elif choose == "5":
        get_bep721_token_transfers(addresses[0])
    else:
        print("Choose a valid option.")
        main()

    os.system("pause")


# Get the balance in BNB of a list of addresses and save to a csv file
def get_balance_by_address(addresses):
    api_key = input(
        "Enter your API key (Get one at https://bscscan.com/apis): ")
    params = {"module": "account", "action": "balancemulti",
              "address": addresses, "apikey": api_key}

    response = requests.get(endpoint, params=params).json()
    create_file(response, f"bnb_balance-{dt}.csv")


# Get a list of normal transactions by address and save to a csv file
def get_normal_transactions_by_address(addresses):
    api_key = input(
        "Enter your API key (Get one at https://bscscan.com/apis): ")
    params = {"module": "account", "action": "txlist", "address": addresses,
              "startblock": 0, "endblock": 99999999, "sort": "asc", "apikey": api_key}

    response = requests.get(endpoint, params=params).json()
    create_file(response, f"normal_transactions-{dt}.csv")


# Get a list of internal transactions by address and save to a csv file
def get_internal_transactions_by_address(addresses):
    api_key = input(
        "Enter your API key (Get one at https://bscscan.com/apis): ")
    params = {"module": "account", "action": "txlistinternal", "address": addresses,
              "startblock": 0, "endblock": 99999999, "sort": "asc", "apikey": api_key}

    response = requests.get(endpoint, params=params).json()
    create_file(response, f"internal_transactions-{dt}.csv")


# Get a list of BEP-20 tokens transferred by an address and save to a csv file
def get_bep20_token_transfers(addresses):
    api_key = input(
        "Enter your API key (Get one at https://bscscan.com/apis): ")
    params = {"module": "account", "action": "tokentx", "address": addresses,
              "startblock": 0, "endblock": 99999999, "sort": "asc", "apikey": api_key}

    response = requests.get(endpoint, params=params).json()
    create_file(response, f"bep20_token_transfers-{dt}.csv")


# Get a list of BEP-721 (NFT) tokens transferred by an address and save to a csv file
def get_bep721_token_transfers(addresses):
    api_key = input(
        "Enter your API key (Get one at https://bscscan.com/apis): ")
    params = {"module": "account", "action": "tokennfttx", "address": addresses,
              "startblock": 0, "endblock": 99999999, "sort": "asc", "apikey": api_key}

    response = requests.get(endpoint, params=params).json()
    create_file(response, f"bep721_token_transfers-{dt}.csv")


# Make a dataframe and create the diretory and csv file
def create_file(response, filename):
    data = json.dumps(response['result'])
    df = pd.read_json(data)

    try:
        dir = "bscscan_files"
        path = os.path.join("", dir)
        os.mkdir(path)
    except OSError:
        pass
    finally:
        df.to_csv(f"{dir}/{filename}", index=False)
        print(f"File succesfully created in User folder.")


if __name__ == "__main__":
    main()
