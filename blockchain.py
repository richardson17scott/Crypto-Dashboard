import os
import requests

def scan_all_wallet_tokens(wallet_address):
    """
    Queries Ankr's multi-chain indexer to get EVERY token asset 
    inside a wallet across major networks, down to microscopic decimal sizes.
    """
    # Using Ankr's public multi-chain advanced indexed gateway
    url = "https://rpc.ankr.com/multichain/a705755171672a3af93f91b8d7e6bcba3cf38ac8e76531a72307259e2bd935f3"
    
    # Target major EVM chains to scan simultaneously
    target_chains = ["eth", "polygon", "bsc", "arbitrum", "base", "avalanche"]
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "ankr_getAccountBalance", # Pre-indexed balance query
            "params": {
                "walletAddress": wallet_address.strip(),
                "blockchain": target_chains
            },
            "id": 1
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        
        token_list = []
        
        if response.status_code == 200:
            result_data = response.json().get("result", {})
            assets = result_data.get("assets", [])
            
            for asset in assets:
                # Extract properties
                symbol = asset.get("tokenSymbol", "UNKNOWN")
                raw_balance = asset.get("balance", "0")
                
                try:
                    # Convert raw text string balance directly to a high-precision float
                    balance_float = float(raw_balance)
                except ValueError:
                    balance_float = 0.0
                    
                # CRITICAL FEATURE: Keep assets greater than absolute 0 (captures 0.00001)
                if balance_float > 0.0:
                    token_list.append({
                        "Symbol": symbol,
                        "Amount": balance_float,
                    })
                    
            return (token_list)
            
        print(f"Indexer returned status error: {response.status_code}")
        return []
        
    except Exception as e:
        print(f"Error scanning wallet inventory: {e}")
        return []
    
if __name__=="__main__": 
    print(scan_all_wallet_tokens("0xfA89F86fBC3e0D1f8E7E4a4C3Da05548d35D4446"))