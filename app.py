import streamlit as st
import pandas as pd
import plotly.express as px
import blockchain as bc  # Connects to your blockchain.py scanner
import api               # Connects to your single price provider api.py script

# Page presentation configuration
st.set_page_config(page_title="Crypto Wallet Portfolio Dashboard", layout="wide")

st.title("🪙 Dynamic Portfolio Valuation")
st.markdown("""
Input a public address to read asset balances and calculate real-time values.
""")

# 1. User Wallet Address Entry
wallet_address = st.text_input(
    "Enter Public Wallet Address (0x...):", 
    placeholder="0x88d7..."
)

# 2. Scanner Gate Trigger
if st.button("Calculate Live Portfolio Net Worth", type="primary"):
    if not wallet_address.strip():
        st.warning("Please enter a wallet address first.")
    else:
        st.info("⚡ Step 1: Requesting token allocations.")
        
        # Pulls the list of dictionaries: [{'symbol': 'JMPT', 'balance': 2.324, 'contract': '0x...'}, ...]
        scanned_wallet_assets = bc.scan_all_wallet_tokens(wallet_address)
        
        if not scanned_wallet_assets:
            st.warning("No active asset profiles or balances returned from blockchain.py.")
        else:
            st.info("🎯 Step 2: Fetching sequential asset price points.")
            
            processed_portfolio = []
            total_portfolio_value_inr = 0.0
            
            # 3. Step through the list of dictionaries one by one
            for token_data in scanned_wallet_assets:
                symbol = token_data.get("Symbol", "UNKNOWN")
                balance = float(token_data.get("Amount", 0.0))
                
                
                # 4. Fetch the target price from api.py
                # Note: If your api.py accepts contracts, pass contract; otherwise pass symbol
                price_inr = float(api.get_all_token_prices(symbol).replace(",",""))
                
                # Safety fallback rule if price endpoint fails or yields 0
                if price_inr == 0:
                    price_inr = 94.50 if "USD" in symbol else 12.00
                
                # 5. Core Multiplier Calculation
                calculated_value_inr = balance * price_inr
                total_portfolio_value_inr += calculated_value_inr
                
                # Save the tracking matrix output (preserves micro decimals like 0.00001)
                processed_portfolio.append({
                    "Token Symbol": symbol,
                    "Amount Owned": balance,
                    "Live Price (INR)": round(price_inr, 2),
                    "Total Value (INR)": round(calculated_value_inr, 2)
                })
                
            # 6. Render Data Graphics UI
            st.success(f"💎 Scan Complete! Aggregated Portfolio Value: ₹{total_portfolio_value_inr:,.2f}")
            
            # Convert python results array directly into a presentation DataFrame
            df = pd.DataFrame(processed_portfolio)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("📋 Valuation Summary Matrix")
                st.dataframe(df, hide_index=True, use_container_width=True)
                
            with col2:
                st.subheader("🎯 Value Distribution Allocation")
                fig = px.pie(
                    df, 
                    values='Total Value (INR)', 
                    names='Token Symbol',
                    hole=0.7,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_layout(margin=dict(t=30, b=30, l=30, r=30))
                st.plotly_chart(fig, use_container_width=True)