import re

from mask_util.const import KEYWORDS
from mask_util.replacer import Replacer


def mask_keyword(input: str) -> str:
    """
        Desensitize text by keywords。
        supported formats：
            password = "123456"
            map.put("password", "123456")
            {
                "password": "123456"
            }
    :param input: need to desensitize text
    :return: Desensitized text
    """
    replacement: str = "***"
    replacer = Replacer(replacement)
    masked_input: str = input
    keyword_reg = '|'.join(r'\b' + keyword + r'\b' for keyword in KEYWORDS)
    pattern = r"(([\"']?)(" + keyword_reg + r")(\2?)\s*[,:]\s*|(" + keyword_reg + r")\s*=\s*)([\"']?)(\w+)(\4?)"
    masked_input = re.sub(pattern, replacer.replacement, masked_input)
    return masked_input
