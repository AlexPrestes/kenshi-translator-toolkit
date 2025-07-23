from dataclasses import dataclass


@dataclass
class Dialog:
    textID: str
    text: str
    trans_text: str = ''
