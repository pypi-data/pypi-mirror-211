import re

from mask_util.const import KEYWORDS
from replacer import Replacer


def mask_keyword(input: str) -> str:
    """
        按照关键词对文本进行脱敏。
        支持的格式：
            password = "123456"
            map.put("password", "123456")
            {
                "password": "123456"
            }
    :param input: 要脱敏的文本
    :return: 脱敏后的文本
    """
    replacement: str = "***"
    replacer = Replacer(replacement)
    masked_input: str = input
    for keyword in KEYWORDS:
        pattern = r"([\"']?" + keyword + "[\"']?\s*[,:]\s*[\"']?|" + keyword + "\s*=\s*[\"']?)([^\"']*)([\"']?)"
        masked_input = re.sub(pattern, replacer.replacement, masked_input)
    return masked_input
