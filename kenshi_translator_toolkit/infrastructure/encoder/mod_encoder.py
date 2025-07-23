from dataclasses import dataclass

from domain.entities.data import Data
from infrastructure.encoder.encoder_helpers import encode_mod


@dataclass
class Encoder:

    @staticmethod
    def encoder_mod(data: Data, filename: str) -> None:
        data_bytes = encode_mod(data)
        with open(filename, 'wb') as file_obj:
            file_obj.write(data_bytes)
