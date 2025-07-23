from dataclasses import dataclass, field

from domain.entities.dialog import Dialog


@dataclass
class Record:
    typecode: int
    name: str
    stringID: str
    data_type_flags: int
    description: str = ''
    trans_name: str = ''
    trans_desc: str = ''
    text: list[Dialog] = field(default_factory=list)
    wordswap_map: list[str] = field(default_factory=list)
    original_name: str = ''
