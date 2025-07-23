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
from kenshi_translator_toolkit import decode_mod, encode_mod
from kenshi_translator_toolkit.domain.entities import Data, Record, Dialog

# Extrair dados para tradução
data = decode_mod("original.mod")

# Modificar campos de tradução (exemplo)
for record in data.data:
    if record.typecode == 19:  # Diálogos
        for dialog in record.text:
            dialog.trans_text = dialog.text.upper()  # Exemplo simplificado

    # Outros campos traduzíveis
    record.trans_name = record.name.upper()
    record.trans_desc = record.description.upper()

# Gerar novo arquivo traduzido
encode_mod(data, "traduzido.mod")
```
=======
# kenshi-translator-toolkit
Ferramenta para extração e reinserção de textos em arquivos .mod do Kenshi
