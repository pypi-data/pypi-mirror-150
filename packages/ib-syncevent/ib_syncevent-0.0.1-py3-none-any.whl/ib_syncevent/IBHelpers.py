
from ibapi.client import Contract
from ibapi.scanner import ScannerSubscription

class IBHelpers():#
    def create_contract(symbol: str, sec_type: str, exchange: str, primaryExchange: str, currency: str):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type
        contract.exchange = exchange  # Give us the best price
        contract.primaryExchange = primaryExchange  # avoid 162 ambiguity error
        contract.currency = currency
        return contract

    def create_scanner_subscription(scan_code: str, instrument: str, locationCode: str, numberOfRows: int, abovePrice: int, aboveVolume: int):
        scanner = ScannerSubscription()
        scanner.scanCode = scan_code
        scanner.instrument = instrument
        scanner.locationCode = locationCode
        scanner.numberOfRows = numberOfRows
        # HIGH_OPEN_GAP - for buy positions /// LOW_OPEN_GAP - for sell positions
        scanner.abovePrice = abovePrice
        scanner.aboveVolume = aboveVolume
        return scanner