
from web3 import *
import asyncio
from address_v2_abi import *
import telegram,time


INFURA_HTTPS = 'https://mainnet.infura.io/v3/YOUR_API_KEY'
connection = Web3(Web3.HTTPProvider(INFURA_HTTPS))
print(f'connectioned via HTTP: {connection.is_connected()}')

async def alert(token,eth_amount,token_amount,begin):
    token_contract = connection.eth.contract(address=token,abi=BASIC_TOKEN_ABI)
    token_name = token_contract.functions.symbol().call()
    eth_amount = eth_amount/10**18
    token_amount = token_amount/10**token_contract.functions.decimals().call()

    end = time.perf_counter()
    laps = end-begin
    bot_token2 = 'YOUR TELEGRAAM_TOKEN'
    async def main():
        bot=telegram.Bot(bot_token2)
        async with bot:
            await bot.send_message(text=f'New token is been added \nName: {token_name}\nETH_ADDED:{eth_amount}\n{token_name} AMOUNT: {token_amount}\n{token_name} Contract:{token}\nTook:{laps}',
            chat_id=963648721)
    await main()



async def process(input,begin):
    router = connection.eth.contract(address=ROUTER_V2_ADDRESS,abi=ROUTER_V2_ABI)
    decode = router.decode_function_input(input)[1]
    token = decode['token']
    token_amount = decode['amountTokenDesired']
    eth_amount = decode['amountETHMin']
    pool = await factory_pool(token)

    if pool != '0x0000000000000000000000000000000000000000':
        await alert(token,eth_amount,token_amount,begin)



async def factory_pool(token):
    factory = connection.eth.contract(address=FACTORY_ADDRESS,abi=FACTORY_ABI)
    return factory.functions.getPair(connection.to_checksum_address(token), connection.to_checksum_address('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')).call()#CHECKING POOL WITH WETH
