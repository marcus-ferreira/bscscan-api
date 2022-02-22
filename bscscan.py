import json
import os
import pandas as pd
import requests


# Variables
api_key = input(
    f"Enter your API key (Get one at https://bscscan.com/apis): ")
endpoint = "https://api.bscscan.com/api"


def main():
    choose = input(
        f"Choose an option:\n"
        "(1) Balance of one or more addresses\n"
        "(2) Normal transactions of an address\n"
        "(3) Internal transactions of an address\n"
        "(4) BEP-20 transfers of an address\n"
        "(5) BEP-721 (NFT) transfers of an address\n")

    addresses = list(
        input(f"Enter the bsc address(es) separated by comma: ").strip().split(","))

    match choose:
        case "1":
            get_balance_by_address(addresses)
        case "2":
            get_transactions_by_address("normal", addresses[0])
        case "3":
            get_transactions_by_address("internal", addresses[0])
        case "4":
            get_transactions_by_address("BEP-20", addresses[0])
        case "5":
            get_transactions_by_address("BEP-721", addresses[0])
        case _:
            main()


# Get the balance in BNB of a list of addresses and save to a csv file
def get_balance_by_address(addresses):
    params = {"module": "account", "action": "balancemulti",
              "address": addresses, "apikey": api_key}

    response = requests.get(endpoint, params=params).json()
    create_file(response, f"bnb_balance.csv")
    main()


# Get a list of transactions by address and save to a csv file
def get_transactions_by_address(type, addresses):
    params = {"module": "account", "address": addresses, "startblock": 0,
              "endblock": 99999999, "sort": "asc", "apikey": api_key}

    if type == "normal":
        params['action'] = "txlist"
    elif type == "internal":
        params['action'] = "txlistinternal"
    elif type == "BEP-20":
        params['action'] = "tokentx"
    elif type == "BEP-721":
        params['action'] = "tokennfttx"

    response = requests.get(endpoint, params=params).json()
    create_file(response, f"{type}_transactions.csv")
    main()


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
        print(f"File succesfully created.")


if __name__ == "__main__":
    main()
