from web3 import Web3
from abi import contract_abi
import random
import time


#--CONFIG--#
#Insert Private keys in keys.txt; One key per line | Приватные ключи в созданный файл keys.txt. По 1 в строку, не должны начинаться с 0x
from_sec = 10     #|Wait from N seconds between transactions | Минимальное значение "ждать от N sec между транзакиями". Для рандомного выбора 
to_sec = 20	    #|Wait to N seconds between transactions | Максиимальное значение "спать до N sec между транзакциями". Для рандомного выбора 
eth_min = 0.00001 #|Min ETH quantity for deposit | Значение ETH минимального депозита. Для рандомного выбора
eth_max = 0.0001   #|Max ETH quantity for deposit | Значение ETH максимального депозита. Для рандомного выбора
contract_address = "0x831698FB4A583b82E25D753a172633bE185637a1" #|Contract address. DO NOT CHANGE if own contract is not deployed | Адрес контракта. НЕ МЕНЯТЬ если не свой не деплоили
RPC = "https://rpc.ankr.com/zksync_era" #|RPC for web3 provider. DO NOT CHANGE if you dont have own RPC | RPC web3 провайдера. НЕ МЕНЯТЬ если нет своей
#----------#


23
eth_min = float(eth_min)
eth_max = float(eth_max)
private_keys = []
failed_keys = []
web3 = Web3(Web3.HTTPProvider(RPC))
contract_address = web3.to_checksum_address(contract_address)
contract = web3.eth.contract(contract_address, abi=contract_abi)

def random_sleep():
    sleep_duration = random.randint(from_sec, to_sec)
    print(f"Sleeping for {sleep_duration} seconds")
    time.sleep(sleep_duration)


def deposit(min_val, max_val, pvt_key):
	address = web3.eth.account.from_key(pvt_key).address
	value_eth = "{:.8f}".format(random.uniform(min_val, max_val))
	value_wei = web3.to_wei(value_eth, 'ether')
	transaction = contract.functions.deposit().build_transaction({
		'from': web3.to_checksum_address(address),
		'value': value_wei,
		'gasPrice': web3.to_wei(0.25, 'gwei'),
		'nonce': web3.eth.get_transaction_count(web3.to_checksum_address(address))
	})

	transaction['gas'] = int(web3.eth.estimate_gas(transaction))

	signed_txn = web3.eth.account.sign_transaction(transaction, pvt_key)
	transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
	print(f"Deposited {value_eth} ETH | Hash: {transaction_hash}")
	random_sleep()


def withdraw(pvt_key):
	address = web3.eth.account.from_key(pvt_key).address
	balance = contract.functions.getBalance().call({'from': address})
	transaction = contract.functions.withdraw(
		balance
	).build_transaction({
		'from': web3.to_checksum_address(address),
		'value': 0,
		'gasPrice': web3.to_wei(0.25, 'gwei'),
		'nonce': web3.eth.get_transaction_count(web3.to_checksum_address(address))
	})
	transaction['gas'] = int(web3.eth.estimate_gas(transaction))
	signed_txn = web3.eth.account.sign_transaction(transaction, pvt_key)
	transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
	print(f"Withdrawing {web3.from_wei(balance, 'ether')} ETH for {address}\nHash: {transaction_hash}\nPrivate key: {pvt_key}")
	random_sleep()

def check_balance(pvt_key):
	address = web3.eth.account.from_key(pvt_key).address
	balance = contract.functions.getBalance().call({'from': address})
	print(f"Address: {address}\nPrivate key: {pvt_key}\nBalance: {web3.from_wei(balance, 'ether')} ETH\n")

with open('.secret', 'r') as f:
    for line in f:
        line = line.strip()
        private_keys.append(line)

choice = int(input("\n----------------------\n1: deposit\n2: withdraw\n3: check balance\nChoice: "))
rounds = int(input("Enter number of rounds: "))  # Specify the number of rounds of operations

for _ in range(rounds):
    # Perform 2 deposits
    for _ in range(2):
        for key in private_keys:
            try:
                deposit(eth_min, eth_max, key)
            except Exception as e:
                print(f"Deposit failed for private key: {key} | Error: {e}")
                failed_keys.append(key)
        random_sleep()

    # Perform 1 withdrawal
    for key in private_keys:
        try:
            withdraw(key)
        except Exception as e:
            print(f"Withdrawal failed for private key: {key} | Error: {e}")
            failed_keys.append(key)
        random_sleep()

    # Display failed keys, if any
    if failed_keys:
        print("\n\nFailed keys: ")
        for failed in failed_keys:
            print(failed)

# End of the script
