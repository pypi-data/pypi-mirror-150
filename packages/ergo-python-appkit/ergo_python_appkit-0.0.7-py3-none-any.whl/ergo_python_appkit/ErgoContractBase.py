from typing import Dict, List
from ergo_python_appkit.appkit import ErgoAppKit, ErgoValueT
from org.ergoplatform.appkit import ErgoValue, OutBox
from sigmastate.Values import ErgoTree

from paideia_contracts.contracts.ErgoBox import ErgoBox

class ErgoContractBase:
    def __init__(self, appKit: ErgoAppKit, script: str = None, mapping: Dict[str,ErgoValue] = {}, ergoTree: ErgoTree = None) -> None:
        self._appKit = appKit
        if script is not None:
            with open(script) as f:
                self._ergoScript = f.read()
            self._ergoTree = self._appKit.compileErgoScript(self._ergoScript, mapping)
        if ergoTree is not None:
            self._ergoTree = ergoTree
        self._contract = self._appKit.contractFromTree(self._ergoTree)

    def buildBox(self, value: int, tokens: Dict[str, int] = None, registers: List[ErgoValue] = None) -> ErgoBox:
        outBox = self._appKit.buildOutBox(
            value=value,
            tokens=tokens,
            registers=registers,
            contract=self._contract
        )
        return ErgoBox(outBox)

