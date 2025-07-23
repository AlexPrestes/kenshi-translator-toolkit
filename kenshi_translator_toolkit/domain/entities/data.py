from dataclasses import dataclass, field

from kenshi_translator_toolkit.domain.entities.record import Record


@dataclass
class Data:
    source_mod_name: str = ''
    source_mod_dependencies: list[str] = field(default_factory=list)
    data: list[Record] = field(default_factory=list)
