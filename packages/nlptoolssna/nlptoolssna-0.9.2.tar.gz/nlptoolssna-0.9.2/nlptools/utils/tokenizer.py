# -*- coding: utf-8 -*-
# Imported from camel
import re

from nlptools.morphology.charsets import UNICODE_PUNCT_SYMBOL_CHARSET
from nlptools.morphology.charsets import UNICODE_LETTER_MARK_NUMBER_CHARSET


_ALL_PUNCT = u''.join(UNICODE_PUNCT_SYMBOL_CHARSET)
_ALL_LETTER_MARK_NUMBER = u''.join(UNICODE_LETTER_MARK_NUMBER_CHARSET)
_TOKENIZE_RE = re.compile(r'[' + re.escape(_ALL_PUNCT) + r']|[' +
                          re.escape(_ALL_LETTER_MARK_NUMBER) + r']+')


def simple_word_tokenize(sentence):
    """Tokenizes a sentence by splitting on whitespace and seperating
    punctuation. The resulting tokens are either alpha-numeric words or single
    punctuation/symbol characters. This function is language agnostic and
    splits all characters marked as punctuation or symbols in the Unicode
    specification. For example, tokenizing :code:`'Hello,    world!!!'`
    would yield :code:`['Hello', ',', 'world', '!', '!', '!']`.
    Args:
        sentence (:obj:`str`): Sentence to tokenize.
    Returns:
        :obj:`list` of :obj:`str`: The list of tokens.
    """

    return _TOKENIZE_RE.findall(sentence)



 #print(simple_word_tokenize("Hello, world!!!"))
