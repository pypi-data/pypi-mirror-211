import re

from mask_util.const import KEYWORDS
from replacer import Replacer


def mask_keyword(input: str) -> str:
    """
        ���չؼ��ʶ��ı�����������
        ֧�ֵĸ�ʽ��
            password = "123456"
            map.put("password", "123456")
            {
                "password": "123456"
            }
    :param input: Ҫ�������ı�
    :return: ��������ı�
    """
    replacement: str = "***"
    replacer = Replacer(replacement)
    masked_input: str = input
    for keyword in KEYWORDS:
        pattern = r"([\"']?" + keyword + "[\"']?\s*[,:]\s*[\"']?|" + keyword + "\s*=\s*[\"']?)([^\"']*)([\"']?)"
        masked_input = re.sub(pattern, replacer.replacement, masked_input)
    return masked_input
