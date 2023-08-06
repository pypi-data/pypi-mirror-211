import requests

def find_ipv6():
    """Return the public IPv6 address of the system.
    This function is syncronous.
    
    Returns:
        str: The IPv6 address of the client.
        
        Example:
            >>> from PyIpify.syncronous import find_ipv6
            >>> find_ipv6()
    """
    return requests.get('https://api64.ipify.org?format=json').json()['ip']




