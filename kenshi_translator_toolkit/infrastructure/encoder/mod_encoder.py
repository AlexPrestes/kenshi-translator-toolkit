from dataclasses import dataclass

from kenshi_translator_toolkit.domain.entities.data import Data
from kenshi_translator_toolkit.infrastructure.encoder.encoder_helpers import encode_mod


@dataclass
class Encoder:

    @staticmethod
    def encoder_mod(data: Data) -> bytes:
        buffer = encode_mod(data)
        return buffer
