from dataclasses import dataclass

from kenshi_translator_toolkit.domain.entities.data import Data
from kenshi_translator_toolkit.infrastructure.decoder.decoder_helpers import parse_mod


@dataclass
class Decoder:

    @staticmethod
    def decoder_mod(file_content: bytes) -> Data:
        parsed_mod = parse_mod(file_content)
        return parsed_mod
