from ergo_python_appkit.appkit import ErgoAppKit, ErgoValueT
from org.ergoplatform.appkit import ErgoValue, OutBox

class ErgoBox:
    def __init__(self, box: OutBox) -> None:
        self._box = box