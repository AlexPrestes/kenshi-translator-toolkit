# Kenshi Translator Toolkit (Beta)

[![PyPI version](https://img.shields.io/pypi/v/kenshi-translator-toolkit.svg)](https://pypi.org/project/kenshi-translator-toolkit/)
[![GitHub license](https://img.shields.io/github/license/AlexPrestes/kenshi-translator-toolkit)](https://github.com/AlexPrestes/kenshi-translator-toolkit/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/AlexPrestes/kenshi-translator-toolkit)](https://github.com/AlexPrestes/kenshi-translator-toolkit/issues)

⚠️ **Versão beta inicial** - Ferramenta em desenvolvimento ativo ⚠️

## Links Importantes
- **Repositório GitHub**: https://github.com/AlexPrestes/kenshi-translator-toolkit
- **Documentação**: https://github.com/AlexPrestes/kenshi-translator-toolkit/blob/main/README.md
- **Reportar Bugs**: https://github.com/AlexPrestes/kenshi-translator-toolkit/issues

## Instalação
```bash
pip install kenshi-translator-toolkit
```

## Uso básico
```python
from kenshi_translator_toolkit import Decoder, Encoder

# Inicializa os componentes
decoder = Decoder()
encoder = Encoder()

# Lê o arquivo original (binário) e decodifica os dados
with open("/path/to/original.mod", "rb") as f:
    content = f.read()
    data = decoder.decode_mod(content)

# Modifica os campos de tradução (exemplo)
for record in data.data:

    if record.name:
        record.trans_name = record.name

    if record.description:
        record.trans_desc = record.description

    for dialog in record.text:
        dialog.trans_text = dialog.text

# Codifica os dados novamente para um buffer binário
buffer = encoder.encode_mod(data)

# Salva o resultado em um novo arquivo
with open("/path/to/translated.mod", "wb") as f:
    f.write(buffer)
```
=======
# kenshi-translator-toolkit
Ferramenta para extração e reinserção de textos em arquivos .mod do Kenshi
