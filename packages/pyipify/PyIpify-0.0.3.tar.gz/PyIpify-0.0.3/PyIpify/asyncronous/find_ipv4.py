import aiohttp

async def find_ipv4():
    '''Returns the IPv4 address of the client. 
    This function is asyncronous.
    
    Returns:
        str: The IPv4 address of the client.
        
    Example:
        >>> import asyncio
        >>> from PyIpify.asyncronous import find_ipv4
        >>> asyncio.run(find_ipv4())
        '''
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.ipify.org?format=json') as response:
            return (await response.json())['ip']
        