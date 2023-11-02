"""
Lab 2
BPE and machine translation evaluation
"""


def prepare_word(
    raw_word: str, start_of_word: str | None, end_of_word: str | None
) -> tuple[str, ...] | None:
    """
    Tokenizes word into unigrams and appends end-of-word token
    :param raw_word: original word
    :param start_of_word: a token that signifies the start of word
    :param end_of_word: a token that signifies the end of word
    :return: preprocessed word
    """
    if not isinstance(raw_word, str):
        return None
    if not isinstance(start_of_word, str) and start_of_word is not None:
        return None
    if not isinstance(end_of_word, str) and end_of_word is not None:
        return None

    tokens = []
    if start_of_word is not None:
        tokens.append(start_of_word)
    tokens.extend(list(raw_word))
    if end_of_word is not None:
        tokens.append(end_of_word)
    return tuple(tokens)

def collect_frequencies(
    text: str, start_of_word: str | None, end_of_word: str
) -> dict[tuple[str, ...], int] | None:
    """
    Counts number of occurrences of each word
    :param text: original text with no preprocessing
    :param start_of_word: a token that signifies the start of word
    :param end_of_word: a token that signifies the end of word
    :return: dictionary in the form of <preprocessed word: number of occurrences>
    """
    if (not isinstance(text, str) or
            not (isinstance(start_of_word, str) or start_of_word is None) or
            not isinstance(end_of_word, str)):
        return None

    dict_of_freq = {}
    words = text.split()
    prepr_words = [prepare_word(word, start_of_word, end_of_word) for word in words]
    for word in set(prepr_words):
        if word is None:
            return None
        dict_of_freq[word] = prepr_words.count(word)

    return dict_of_freq


def count_tokens_pairs(
    word_frequencies: dict[tuple[str, ...], int]
) -> dict[tuple[str, str], int] | None:
    """
    Counts number of occurrences of each pair of subsequent tokens
    :param word_frequencies: dictionary in the form of <preprocessed word: number of occurrences>
    :return: dictionary in the form of <token pair: number of occurrences>
    """
    if not isinstance(word_frequencies, dict):
        return None

    result_dic = {}
    for word in word_frequencies:
        for i in range(len(word) - 1):
            pair = word[i:i + 2]
            if not result_dic.get(pair):
                result_dic[pair] = 0
            result_dic[pair] += word_frequencies[word]

    return result_dic



def merge_tokens(
    word_frequencies: dict[tuple[str, ...], int], pair: tuple[str, str]
) -> dict[tuple[str, ...], int] | None:
    """
    Updates word frequency dictionary by replacing a pair of token with a merged one
    :param word_frequencies: dictionary in the form of <preprocessed word: number of occurrences>
    :param pair: a pair of tokens to be merged
    :return: dictionary in the form of <preprocessed word: number of occurrences>
    """
    if (not isinstance(word_frequencies, dict) or
            not isinstance(pair, tuple)):
        return None

    new_word_freq = {}
    for word in word_frequencies:
        new_word = list(word)
        if pair[0] in word and pair[1] in word:
            for i in range(len(word) - 1):
                current_pair = tuple([word[i], word[i+1]])
                if current_pair == pair:
                    new_word.pop(i+1)
                    new_word[i] = pair[0] + pair[1]

        new_word_freq[tuple(new_word)] = word_frequencies[word]

    return new_word_freq


def train(
    word_frequencies: dict[tuple[str, ...], int] | None, num_merges: int
) -> dict[tuple[str, ...], int] | None:
    """
    Creates required number of new tokens by merging existing ones
    :param word_frequencies: dictionary of a kind <preprocessed word: number of occurrences>
    :param num_merges: required number of new tokens
    :return: dictionary in the form of <preprocessed word: number of occurrences>
    """
    if (not isinstance(word_frequencies, dict) or
            not isinstance(num_merges, int)):
        return None

    dict_pairs = count_tokens_pairs(word_frequencies)
    if dict_pairs is None:
        return None
    num_merges = min(num_merges, len(dict_pairs))

    for iteration in range(num_merges):
        if dict_pairs != {}:
            max_value = max(dict_pairs.values())
            value_list = [key for key, value in dict_pairs.items() if value == max_value]

            max_len = max(len(''.join(pair)) for pair in value_list)
            len_list = [pair for pair in value_list if len(''.join(pair)) == max_len]

            word_frequencies = merge_tokens(word_frequencies, sorted(len_list)[0])
            if word_frequencies is None:
                return None

            dict_pairs = count_tokens_pairs(word_frequencies)
            if dict_pairs is None:
                return None

    return word_frequencies


def get_vocabulary(
    word_frequencies: dict[tuple[str, ...], int], unknown_token: str
) -> dict[str, int] | None:
    """
    Establishes correspondence between tokens and its integer identifier
    :param word_frequencies: dictionary in the form of <preprocessed word: number of occurrences>
    :param unknown_token: a token to signify an unknown token
    :return: dictionary in the form of <token: identifier>
    """


def decode(
    encoded_text: list[int] | None, vocabulary: dict[str, int] | None, end_of_word_token: str | None
) -> str | None:
    """
    Translates encoded sequence into decoded one
    :param encoded_text: a sequence of token identifiers
    :param vocabulary: dictionary in the form of <token: identifier>
    :param end_of_word_token: an end-of-word token
    :return: decoded sequence
    """


def tokenize_word(
    word: tuple[str, ...], vocabulary: dict[str, int], end_of_word: str | None, unknown_token: str
) -> list[int] | None:
    """
    Splits word into tokens
    :param word: preprocessed word
    :param vocabulary: dictionary in the form of <token: identifier>
    :param end_of_word: an end-of-word token
    :param unknown_token: token that signifies unknown sequence
    :return: list of token identifiers
    """


def load_vocabulary(vocab_path: str) -> dict[str, int] | None:
    """
    Reads and retrieves dictionary of type <token: identifier>
    :param vocab_path: path to the saved vocabulary
    :return: dictionary in the form of <token: identifier>
    """


def encode(
    original_text: str,
    vocabulary: dict[str, int] | None,
    start_of_word_token: str | None,
    end_of_word_token: str | None,
    unknown_token: str,
) -> list[int] | None:
    """
    Translates decoded sequence into encoded one
    :param original_text: original text
    :param vocabulary: dictionary in the form of <token: identifier>
    :param start_of_word_token: a start-of-word token
    :param end_of_word_token: an end-of-word token
    :param unknown_token: token that signifies unknown sequence
    :return: list of token identifiers
    """


def collect_ngrams(text: str, order: int) -> list[tuple[str, ...]] | None:
    """
    Extracts n-grams from the given sequence
    :param text: original text
    :param order: required number of elements in a single n-gram
    :return: sequence of n-grams
    """


def calculate_precision(
    actual: list[tuple[str, ...]], reference: list[tuple[str, ...]]
) -> float | None:
    """
    Compares two sequences by virtue of Precision metric
    :param actual: predicted sequence of n-grams
    :param reference: expected sequence of n-grams
    :return: value of Precision metric
    """


def geo_mean(precisions: list[float], max_order: int) -> float | None:
    """
    Computes geometric mean of sequence of values
    :param precisions: sequence of Precision values
    :param max_order: maximum length of n-gram considered
    :return: value of geometric mean of Precision metric
    """


def calculate_bleu(actual: str | None, reference: str, max_order: int = 3) -> float | None:
    """
    Compares two sequences by virtue of BLEU metric
    :param actual: predicted sequence
    :param reference: expected sequence
    :param max_order: max length of n-gram to consider for comparison
    :return: value of BLEU metric
    """
