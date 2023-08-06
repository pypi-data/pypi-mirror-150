
from __future__ import annotations

import time
import threading

from .utilities import IBDataReciver
from .utilities import IBEvents
from .utilities import Events
from .utilities import IBApi

from ibapi.client import BarData, TagValueList, TickerId, Contract
from ibapi.scanner import ScanData, ScannerSubscription
from ibapi.tag_value import TagValue


class IBSyncEvent():
    def __init__(self) -> None:
        self.global_state = IBDataReciver()

        self.ib_handlers = IBEvents()

        self.events_thread = {
            Events.MAIN: threading.Event(),
            Events.SECONDARY: threading.Event()
        }

        self.ibapi = IBApi(self.events_thread,
                           self.global_state, self.ib_handlers)

        self.connection_thread = threading.Thread(
            target=self.ibapi.run, daemon=True)

    def connect(self, host: str, port: int, conId: int) -> None:
        self.ibapi.connect(host, port, conId)
        self.connection_thread.start()
        time.sleep(1)

    def request_historical_bars(self, reqId: TickerId, contract: Contract, endDateTime: str, durationStr: str, barSizeSetting: str, whatToShow: str, useRTH: int, formatDate: int, keepUpToDate: bool, chartOptions: TagValueList) -> list[BarData] or None:
        self.events_thread[Events.MAIN].clear()
        self.ibapi.reqHistoricalData(reqId, contract, endDateTime, durationStr,
                                     barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions)
        self.events_thread[Events.MAIN].wait()

        if not self.ib_handlers.historical_bars_event:
            results = self.global_state.get_historical_bars()
            self.global_state.clear_historical_bars()
            return results

    def request_scanner_results(self, reqId: TickerId, subscription: ScannerSubscription, scannerSubscriptionOptions: list[TagValue], scannerSubscriptionFilterOptions: list[TagValue]) -> list[ScanData] or None:
        self.events_thread[Events.MAIN].clear()
        self.ibapi.reqScannerSubscription(
            reqId, subscription, scannerSubscriptionOptions, scannerSubscriptionFilterOptions)
        self.events_thread[Events.MAIN].wait()

        self.events_thread[Events.SECONDARY].clear()
        self.ibapi.cancelScannerSubscription(reqId)
        self.events_thread[Events.SECONDARY].wait()

        results = self.global_state.get_scanner_results()
        self.global_state.clear_scanner_results()
        return results

    def request_account_summary(self, reqId: TickerId, groupName: str, tags: str) -> TagValue or None:
        self.events_thread[Events.MAIN].clear()
        self.ibapi.reqAccountSummary(reqId, groupName, tags)
        self.events_thread[Events.MAIN].wait()

        self.events_thread[Events.SECONDARY].clear()
        self.ibapi.cancelAccountSummary(reqId)
        self.events_thread[Events.SECONDARY].wait()

        results = self.global_state.get_account_summary_tag()
        self.global_state.clear_account_summary_tag()
        return results
