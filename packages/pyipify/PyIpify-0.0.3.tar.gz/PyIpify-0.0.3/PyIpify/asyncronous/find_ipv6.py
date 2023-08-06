import aiohttp

async def find_ipv6():
    """Return the public IPv6 address of the system.
    This function is asyncronous.
    
    Returns:
        str: The IPv6 address of the client.
        
        Example:
            >>> import asyncio
            >>> from PyIpify.asyncronous import find_ipv6
            >>> asyncio.run(find_ipv6())
            
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api64.ipify.org?format=json') as response:
            return (await response.json())['ip']

