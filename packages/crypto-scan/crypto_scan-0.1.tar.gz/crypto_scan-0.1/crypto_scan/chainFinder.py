import re
from configs import ETH_CHAIN, SOLNANA_CHAIN
ETH_REG = r'(0x[a-fA-F0-9]{40})[^a-z^A-Z^0-9]?'
SOL_REG = r'([1-9A-HJ-NP-Za-km-z]{32,44})'


def find_chain(addr):
    matches = []
    if re.match(ETH_REG, addr):
        matches.append(ETH_CHAIN)
    if re.match(SOL_REG, addr):
        matches.append(SOLNANA_CHAIN)
    return matches
