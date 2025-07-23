import io
import logging
import os
import re
import traceback

from domain.entities.data import Data
from domain.entities.dialog import Dialog
from domain.entities.record import Record
from domain.entities.typecode import TypeCode
from infrastructure.decoder.decoder_utils import (
    read_bool,
    read_char,
    read_float,
    read_int,
    read_string,
    skip_block,
    skip_vector_block,
)

# Configuração do logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constantes para WordSwap (opcional)
WORDSWAP_CHARS = ["∩∩∩", "∪∪∪", "⊂⊂⊂", "⊃⊃⊃", "⊆⊆⊆", "⊇⊇⊇", "∈∈∈", "∋∋∋"]
is_word_swap_active = True  # Configurável conforme necessidade


def parse_mod(file_content: bytes) -> Data:
    f = io.BytesIO(file_content)
    data = Data()

    try:
        # Leitura do tipo de arquivo
        file_type = read_int(f)
        logger.debug("Tipo de arquivo detectado: %s", file_type)

        # Processamento do cabeçalho
        record_count, dependencies_str = parse_header(f, file_type)
        data.source_mod_dependencies = extract_dependencies(dependencies_str)
        logger.debug("Dependências encontradas: %s", data.source_mod_dependencies)

        # Processamento de registros
        for rec_idx in range(record_count):
            try:
                record = parse_record(f)
                if should_include_record(record):
                    data.data.append(record)
            except Exception as e:
                logger.error("Erro no registro %s: %s", rec_idx, e)
                logger.debug(traceback.format_exc())

    except Exception as e:
        logger.error("Erro fatal no parsing: %s", e)
        logger.debug(traceback.format_exc())

    return data


def should_include_record(record: Record) -> bool:
    """Determina se o registro deve ser incluído nos resultados"""
    if not record:
        return False

    # Diálogos (type 19) sempre são incluídos
    if record.typecode == TypeCode.DIALOG:
        return bool(record.text)

    # Itens editáveis: incluir apenas se a flag não estiver ativa
    if TypeCode.is_editable(record.typecode):
        if record.data_type_flags & 0b1:
            return False
        return bool(record.name or record.description or record.text)

    return False


def parse_header(f: io.BytesIO, file_type: int) -> tuple[int, str]:
    """Processa o cabeçalho do arquivo MOD"""
    record_count = 0
    dependencies_str = ''

    if file_type == TypeCode.SIMPLE_HEADER:  # Type 16
        _ = read_int(f)  # version
        _ = read_string(f)  # author
        _ = read_string(f)  # description
        dependencies_str = read_string(f)
        _ = read_string(f)  # references
        _ = read_int(f)  # unknown
        record_count = read_int(f)

    elif file_type == TypeCode.EXTENDED_HEADER:  # Type 17
        header_len = read_int(f)
        _ = read_int(f)  # version
        _ = read_string(f)  # author
        _ = read_string(f)  # description
        dependencies_str = read_string(f)  # dependencies
        _ = read_string(f)  # references
        _ = read_int(f)
        _ = read_int(f)  # unknown1
        _ = read_char(f)  # unknown2

        # Pular para o final do cabeçalho estendido
        if header_len > 0:
            current_pos = f.tell()
            target_pos = header_len + 8
            if current_pos < target_pos:
                f.seek(target_pos, os.SEEK_SET)

        _ = read_int(f)  # unknown3
        record_count = read_int(f)

    else:
        logger.error("Tipo de cabeçalho desconhecido: %s", file_type)

    return record_count, dependencies_str


def extract_dependencies(dependencies_str: str) -> list[str]:
    """Extrai as dependências da string do cabeçalho"""
    if not dependencies_str:
        return []
    return [
        d.strip()
        for d in dependencies_str.split(',')
        if d.strip().lower().endswith('.mod')
    ]


def parse_record(f: io.BytesIO) -> Record:
    """Analisa um único registro do arquivo MOD"""
    # Metadados básicos
    _ = read_int(f)  # instance_count
    typecode = read_int(f)
    _ = read_int(f)  # id
    name = read_string(f)
    string_id = read_string(f)
    data_type_flags = read_int(f)

    # Blocos de dados a serem ignorados
    skip_block(f, read_bool)
    skip_block(f, read_float)
    skip_block(f, read_int)
    skip_vector_block(f, 3)  # Vec3f
    skip_vector_block(f, 4)  # Vec4f

    # Criar registro
    record = Record(
        typecode=typecode,
        name=name,
        stringID=string_id,
        data_type_flags=data_type_flags,
        original_name=name
    )

    # Processar strings (diálogos e descrições)
    str_count = read_int(f)
    for _ in range(str_count):
        key = read_string(f)
        value = read_string(f)

        # Descrição para itens editáveis
        if key == "description" and TypeCode.is_editable(typecode):
            record.description = apply_wordswap(value)

        # Diálogos
        elif typecode == TypeCode.DIALOG and key.startswith("text"):
            record.text.append(Dialog(
                textID=key,
                text=apply_wordswap(value),
                trans_text=''
            ))

    # Blocos adicionais
    skip_block(f, read_string)  # Filename map

    # Referências
    ref_list_count = read_int(f)
    for _ in range(ref_list_count):
        _ = read_string(f)
        sub_ref_count = read_int(f)
        for _ in range(sub_ref_count):
            _ = read_string(f)
            _ = read_int(f)
            _ = read_int(f)
            _ = read_int(f)

    # Instâncias
    instance_list_count = read_int(f)
    for _ in range(instance_list_count):
        _ = read_string(f)  # instance name
        _ = read_string(f)  # instance file
        for _ in range(6):  # position and rotation
            _ = read_float(f)
        attachment_count = read_int(f)
        for _ in range(attachment_count):
            _ = read_string(f)  # attachment name

    return record


def apply_wordswap(text: str) -> str:
    """Aplica a substituição de WordSwap se ativado"""
    if not is_word_swap_active:
        return text

    # Substitui padrões /.../ por caracteres especiais
    processed = text
    swaps = re.findall(r'/.+?/', text)
    unique_swaps = list(dict.fromkeys(swaps))  # Mantém ordem sem duplicatas

    for i, pattern in enumerate(unique_swaps):
        if i < len(WORDSWAP_CHARS):
            processed = processed.replace(pattern, WORDSWAP_CHARS[i])

    return processed
