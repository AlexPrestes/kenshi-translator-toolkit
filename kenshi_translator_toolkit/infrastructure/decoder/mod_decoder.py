from dataclasses import dataclass

from domain.entities.data import Data
from infrastructure.decoder.decoder_helpers import parse_mod


@dataclass
class Decoder:
    @staticmethod
    def decoder_mod(filename: str) -> Data:
        with open(filename, 'rb') as file_obj:
            parsed_mod = parse_mod(file_obj.read())
            parsed_mod.source_mod_name = file_obj.name
            return parsed_mod
