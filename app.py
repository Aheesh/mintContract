import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/artwork_abi.json')) as f:
         artwork_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
    address=contract_address,
    abi=artwork_abi
)


    return contract


contract = load_contract()


################################################################################
# Register New Artwork
################################################################################
st.title("Anon Communicator")

accounts = w3.eth.accounts

# Use a streamlit component to get the address of the artwork owner from the user
# @TODO: YOUR CODE HERE!
address = st.selectbox("Authenticated Wallet address (Place holder this will be populated via web3 wallet login)", options=accounts)


# Use a streamlit component to get the artwork's URI
# HINT: You can just enter this as text for now.
# @TODO: YOUR CODE HERE!
artwork_uri = st.text_input("URI of the stored message (PLACEHOLDER - to be replaced by the URI we get from IPFS Pinata)")

if st.button("Send the Message"):

    # Use the contract to send a transaction to the registerArtwork function
    tx_hash = contract.functions.registerArtwork(address, artwork_uri).transact({
        "from": address,
        "gas": 1000000
    })

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")

################################################################################
# Logged in user : Inbox
################################################################################
st.markdown("## Message Inbox")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address has {tokens} messages in the Inbox")

token_id = st.selectbox("Messages Inbox", list(range(tokens)))

# List all tokens and date of message sent.
#token_ids=contract.functions.tokenOfOwnerByIndex(selected_address,token_id).call()
#st.write(f"List of Tokens {token_ids} ")

if st.button("Display Message"):

    # Use the contract's `ownerOf` function to get the art token owner
    owner =  contract.functions.ownerOf(token_id).call()

    st.write(f"The message is for {owner}")

    # Use the contract's `tokenURI` function to get the art token's URI
    token_uri =  contract.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI of the message is {token_uri}")
    st.image(token_uri)

