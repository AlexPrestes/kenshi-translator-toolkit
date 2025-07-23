import io
import logging

from domain.entities.data import Data
from domain.entities.record import Record
from domain.entities.typecode import TypeCode
from infrastructure.encoder.encoder_utils import write_int, write_string

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constantes
WORDSWAP_CHARS = ['∩∩∩', '∪∪∪', '⊂⊂⊂', '⊃⊃⊃', '⊆⊆⊆', '⊇⊇⊇', '∈∈∈', '∋∋∋']
MOD_VERSION = 1
UNKNOWN_HEADER_VALUE = 0x004C67A6


def encode_mod(data: Data, is_word_swap_active: bool = True) -> bytes:
    """
    Converte o objeto Data de volta para o formato binário .mod do Kenshi

    Args:
        data: Objeto Data contendo os registros a serem serializados
        is_word_swap_active: Se True, aplica a reversão do WordSwap

    Returns:
        Bytes do arquivo .mod codificado
    """
    buffer = io.BytesIO()

    try:
        # Escrever cabeçalho (tipo 16 - formato simples)
        _write_header(buffer, data)

        # Escrever cada registro
        for record in data.data:
            _write_record(buffer, record, is_word_swap_active)

        return buffer.getvalue()

    except Exception as e:
        logger.error('Erro na codificação do MOD: %s', e)
        raise
    finally:
        buffer.close()


def _write_header(buffer: io.BytesIO, data: Data) -> None:
    """Escreve o cabeçalho do arquivo MOD"""
    # Tipo de arquivo (16 = formato simples)
    write_int(buffer, TypeCode.SIMPLE_HEADER)

    # Versão do MOD
    write_int(buffer, MOD_VERSION)

    # Autor (vazio para traduções)
    write_string(buffer, '')

    # Descrição do MOD
    mod_description = f'Tradução para {data.source_mod_name}'
    write_string(buffer, mod_description)

    # Dependências
    dependencies_str = ','.join(data.source_mod_dependencies)
    dependencies_str += f',{data.source_mod_name}'
    write_string(buffer, dependencies_str)

    # Referências (vazio)
    write_string(buffer, '')

    # Valor desconhecido (padrão)
    write_int(buffer, UNKNOWN_HEADER_VALUE)

    # Contagem de registros
    write_int(buffer, len(data.data))


def _write_record(
    buffer: io.BytesIO, record: Record, is_word_swap_active: bool
) -> None:

    """Escreve um único registro no arquivo MOD"""
    # Contagem de instâncias (sempre 0)
    write_int(buffer, 0)

    # Tipo do registro
    write_int(buffer, record.typecode)

    # ID (sempre 0)
    write_int(buffer, 0)

    # Nome (usa tradução se disponível)
    name_to_write = record.trans_name or record.original_name
    write_string(buffer, name_to_write)

    # String ID
    write_string(buffer, record.stringID)

    # Flags de dados
    write_int(buffer, _determine_flags(record))

    # Blocos vazios (bool, float, int)
    for _ in range(3):
        write_int(buffer, 0)  # Contagem de elementos

    # Blocos vetoriais vazios (vec3f, vec4f)
    for _ in range(2):
        write_int(buffer, 0)  # Contagem de elementos

    # Escrever strings (diálogos ou descrição)
    if record.typecode == TypeCode.DIALOG:
        _write_dialogs(buffer, record, is_word_swap_active)
    elif TypeCode.is_editable(record.typecode):
        _write_description(buffer, record, is_word_swap_active)
    else:
        write_int(buffer, 0)  # Contagem de strings = 0

    # Bloco de nomes de arquivo (vazio)
    write_int(buffer, 0)

    # Bloco de referências (vazio)
    write_int(buffer, 0)  # Contagem de listas de referência

    # Bloco de instâncias (vazio)
    write_int(buffer, 0)  # Contagem de instâncias


def _determine_flags(record: Record) -> int:
    """Determina as flags baseado no que foi modificado"""
    # Item novo (não presente no original)
    if record.data_type_flags == -2147483647:
        return -2147483647

    # Nome modificado
    if record.trans_name and record.trans_name != record.original_name:
        return -2147483645  # 0x80000003

    # Outros dados modificados
    return -2147483646  # 0x80000002


def _write_dialogs(
    buffer: io.BytesIO, record: Record, is_word_swap_active: bool
) -> None:
    """Escreve diálogos para registros do tipo 19"""
    # Contagem de diálogos
    write_int(buffer, len(record.text))

    for dialog in record.text:
        # Usar texto traduzido se disponível
        text_to_write = dialog.trans_text or dialog.text

        # Reverter WordSwap se necessário
        if is_word_swap_active and record.wordswap_map:
            text_to_write = _reverse_wordswap(
                text_to_write, record.wordswap_map
            )

        write_string(buffer, dialog.textID)
        write_string(buffer, text_to_write)


def _write_description(
    buffer: io.BytesIO, record: Record, is_word_swap_active: bool
) -> None:
    """Escreve descrição para itens editáveis"""
    if not record.trans_desc and not record.description:
        write_int(buffer, 0)  # Sem descrição
        return

    # Usar descrição traduzida se disponível
    description_to_write = record.trans_desc or record.description

    # Reverter WordSwap se necessário
    if is_word_swap_active and record.wordswap_map:
        description_to_write = _reverse_wordswap(
            description_to_write, record.wordswap_map
        )

    # Escrever string única
    write_int(buffer, 1)
    write_string(buffer, 'description')
    write_string(buffer, description_to_write)


def _reverse_wordswap(text: str, wordswap_map: list[str]) -> str:
    """Reverte o WordSwap substituindo símbolos pelos padrões originais"""
    for i, symbol in enumerate(WORDSWAP_CHARS):
        if i < len(wordswap_map):
            text = text.replace(symbol, wordswap_map[i])
    return text
