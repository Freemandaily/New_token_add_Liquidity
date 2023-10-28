import asyncio
from brownie import *
import time
from class_sniper import sniper

network.connect('goerli')

priv1 = '0x9e5839ef55eb53e6a6b4e497e8045e899fb5a5e8c3ed9eb0077c369f7ccf7ae2'
priv2 = '0x3f022b7cc0898a2f15a7e69880a89c6558e910b4018244ab18cb2697a2db1a72'

account1 = accounts.add(priv1)
account2 = accounts.add(priv2)

token_contract = input('Token contract address\n')

ROUTER_ADDRESS = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
FACTORY_ADDRESS = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
WETH = '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6'

swap = sniper(account1)
#swap2 = sniper(account2)

input = 0.001
profit_percent = 1 
swap_back_percent = 0.01
token_id = str(round(time.time()))
not_trading =  True
async def main():
    while not_trading :
        print('spying the the pool')
        new_token = swap.contract_load(token_contract,'token'+token_id)
        router = swap.contract_load(ROUTER_ADDRESS,'router')
        factory = swap.contract_load(FACTORY_ADDRESS,'factory')
        try:
            allowance = swap.allowance(new_token,router)
            if allowance == 0:
               print('approving token')
               swap.token_approve(new_token,router,amount=input*10**18)
        except Exception as e:
            print(f'The problem is {e}')


        
        pool_address = factory.getPair(web3.toChecksumAddress(new_token.address),web3.toChecksumAddress(WETH))
        
        if pool_address != '0x0000000000000000000000000000000000000000':
            #not_trading = False
            print('ready to make a trade')
            price = swap.trade(router,new_token,amount=input*10**18)
            
            if price:
                while True:
                    print('checking for profitable price')
                    pool = swap.contract_load(pool_address,'pool'+token_id)
                    token_address = pool.token1()
                    token_A_balance,token_B_balance = pool.getReserves()[:2]
                    
                    if token_address == web3.toChecksumAddress(new_token.address):
                        print('hello')
                        updated_price = token_A_balance/token_B_balance
                        print(f'First price:{price}\nUpdated price:{updated_price}')
                    else:
                        print('hi')
                        updated_price = token_B_balance/token_A_balance
                        print(f'First price:{price}\nUpdated price:{updated_price}')
                    if updated_price <= profit_percent*price:
                        user_balance =  new_token.balanceOf(account1)
                        amount = user_balance*swap_back_percent
                        trade_success = swap.trade_back(router,new_token,amount)

                        break
                break

                    

zeta = '0xCc7bb2D219A0FC08033E130629C2B854b7bA9195'  
dai = '0x11fE4B6AE13d2a6055C8D9cF65c55bac32B5d844'      
           
asyncio.run(main())