import re
import silabeador
from dataclasses import dataclass, replace


@dataclass
class Values:
    words: list
    syllables: list


class Transcription:
    def __init__(self, sentence, mono=False, epenthesis=False, aspiration=False,
                 sampastr='"'):
        self.sentence = self.__letters(sentence, epenthesis)
        self.phonology = self.transcription_fnl(self.sentence, mono, aspiration)
        self.phonetics = self.transcription_fnt(self.phonology)
        self.sampa = self.ipa2sampa(self.phonetics, sampastr)

    @staticmethod
    def __clean(sentence, epenthesis):
        symbols = ['(', ')', '¿', '?', '¡', '!', '«', '»', '“', '”', '‘', '’',
                   '[', ']',
                   '—', '…', ',', ';', ':', "'", '.', '–', '"', '-']
        letters = {'õ': 'o', 'æ': 'e',
                   ' à ': ' a ', ' ò ': 'o',
                   'à': 'á', 'è': 'é', 'ì': 'í', 'ò': 'ó', 'ù': 'ú',
                   'ö': '_o', 'ä': '_a', 'ë': '_e', 'ï': '_i',
                   'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
                   'ç': 's'}
        for x in symbols:
            if x in sentence:
                sentence = sentence.replace(x, ' ')
        for x in letters:
            if x in sentence:
                sentence = sentence.replace(x, letters[x])
        if epenthesis:
            sentence = re.sub(r'\bs((?![aeiouáéíóúäëïöü]))', r'es\1', sentence)
        return sentence

    def __letters(self, sentence, epenthesis):
        sentence = self.__clean(sentence.lower(), epenthesis)
        letters = {'b': 'be', 'c': 'ce', 'd': 'de', 'f': 'efe', 'g': 'ge',
                   'h': 'hache', 'j': 'jota', 'k': 'ka', 'l': 'ele',
                   'm': 'eme', 'n': 'ene', 'p': 'pe', 'q': 'ku',
                   'r': 'erre', 's': 'ese', 't': 'te', 'v': 'ube',
                   'w': 'ubedoble', 'x': 'ekis', 'z': 'ceta', 'ph': 'peache'}
        for letter in letters:
            sentence = re.sub(rf'\b{letter}\b', 'letters[letter]', sentence)
        return sentence

    def transcription_fnl(self, sentence, mono, aspiration):
        diacritics = {'á': 'a', 'à': 'a', 'ä': 'a',
                      'é': 'e', 'è': 'e', 'ë': 'e',
                      'í': 'i', 'ì': 'i', 'ï': 'i',
                      'ó': 'o', 'ò': 'o', 'ö': 'o',
                      'ú': 'u', 'ù': 'u', 'ü': 'u',
                      '_': ''}

        consonants = {'w': 'b', 'v': 'b', 'z': 'θ', 'x': 'ks', 'j': 'x',
                      'ñ': 'ɲ', 'qu': 'k', 'll': 'ʎ', 'ch': 'ʧ',
                      'r': 'ɾ', 'R': 'r',
                      'ce': 'θe', 'cé': 'θé', 'cë': 'θë',
                      'ci': 'θi', 'cí': 'θí', 'cï': 'θï', 'cj': 'θj',
                      'c': 'k', 'ph': 'f'}
        sentence = re.sub(r'(?:([nls])r|rr|\br)', r'\1R', sentence)
        sentence = sentence.replace('r', 'ɾ')
        sentence = re.sub(r'\bh', 'ʰ', sentence)
        for consonant in consonants:
            if consonant in sentence:
                sentence = sentence.replace(consonant, consonants[consonant])
        if aspiration:
            sentence = re.sub(r'\bh', 'ʰ', sentence)
        sentence = sentence.replace('h', '')
        if 'y' in sentence:
            sentence = re.sub(r'\by\b', 'i', sentence)
            sentence = re.sub(r'y\b', 'j', sentence)
            sentence = sentence.replace('y', 'ʝ')
            for key, value in diacritics.items():
                if key in 'áéíóú':
                    sentence = re.sub(rf'{value}ʝ\b', f'{key}i', sentence)
            # sentence = re.sub(r'y', 'ʝ', sentence)
            # sentence = re.sub(r'ʝ\b', 'i', sentence)
            sentence = re.sub(r'ʝ((?![aeiouáéíóú]))', r'i\1', sentence)
        if 'g' in sentence:
            for reg in [
                [r'g([eiéíiëï])', rf'x\1'],
                    [r'g[u]([eiéíëï])', rf'g\1']]:
                sentence = re.sub(reg[0], reg[1], sentence)
            sentence = re.sub(r'gü([ei])', r'gw\1', sentence)
            sentence = re.sub(r'gu([ao])', r'gw\1', sentence)
        transcription = self.__split_variables(sentence, mono)
        words = transcription['words']
        syllables = transcription['syllables']
        for letter in diacritics:
            words = [word.replace(letter, diacritics[letter])
                     for word in words]
            syllables = [syllable.replace(letter, diacritics[letter]) for
                         syllable in syllables]
        return Values(words, syllables)

    @staticmethod
    def ipa2sampa(ipa, sampastr):
        ipa = Values(ipa.words.copy(), ipa.syllables.copy())
        transliteration = {'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u',
                           'j': 'j', 'w': 'w',
                           'b': 'b', 'β': 'B', 'd': 'd', 'ð': 'D',
                           'g': 'g', 'ɣ': 'G',
                           'p': 'p', 't': 't', 'k': 'k',
                           'l': 'l', 'ʎ': 'L', 'r': 'rr', 'ɾ': 'r',
                           'm': 'm', 'ɱ': 'M', 'n': 'n', 'ŋ': 'N', 'ɲ': 'J',
                           'ʧ': 'tS', 'ʝ': 'y', 'x': 'x', 'χ': '4',
                           'f': 'f', 's': 's', 'z': 'z', 'θ': 'T',
                           'ˈ': sampastr, 'ˌ': '%'}

        for symbol in transliteration:
            for idx, word in enumerate(ipa.words):
                ipa.words[idx] = word.replace(symbol, transliteration[symbol])
            for idx, syllable in enumerate(ipa.syllables):
                ipa.syllables[idx] = syllable.replace(symbol,
                                                      transliteration[symbol])
        return ipa

    def __split_variables(self, sentence, mono):
        syllabic = []
        words = []
        for word in sentence.split():
            if len(word) > 5 and word.endswith('mente'):
                syllabification = silabeador.syllabification(
                    word[:-5], True, True)
                syllables = syllabification.syllables
                if len(syllables) > 1:
                    syllables = syllables + ['ˌmen', 'te']
                    stress = syllabification.stress - 2
                    word = word.replace('mente', 'ˌmente')
                else:
                    syllables = syllables + ["ˈmen", 'te']
                    stress = -2
            else:
                syllabification = silabeador.syllabification(word, True, True)
                syllables = syllabification.syllables
                stress = syllabification.stress
            conta = 0
            diph = self.__diphthongs(word, syllables)
            word = diph['word']
            syllables = diph['syllables']
            syllables[stress] = f"ˈ{syllables[stress]}"
            for idx, slb in enumerate(syllables):
                for char in slb:
                    if char == "ˈ":
                        word = word[:conta] + "ˈ" + word[conta:]
                    else:
                        conta += 1
            for idx, syllable in enumerate(syllables):
                if not mono and len(syllables) == 1:
                    syllable = syllable.strip("ˈ")
                syllabic += [syllable]
            if len(syllables) == 1 and not mono:
                word = word.replace('ˈ', '')
            words += [word]
        return {'words': words, 'syllables': syllabic}

    @staticmethod
    def __fsubstitute(words):
        words = words.replace('b', 'β').replace('d', 'ð').replace('g', 'ɣ')
        words = re.sub(r'([mnɲ ^])(\-*)β', r'\1\2b', words)
        words = re.sub(r'([mnɲlʎ ^])(\-*)ð', r'\1\2d', words)
        words = re.sub(r'([mnɲ ^])(\-*)ɣ', r'\1\2g', words)
        words = re.sub(r'θ(\-*)([bdgβðɣmnɲlʎrɾ])', r'ð\1\2', words)
        words = re.sub(r's(\-*)([bdgβðɣmnɲlʎrɾ])', r'z\1\2', words)
        words = re.sub(r'f(\-*)([bdgβðɣmnɲʎ])', r'v\1\2', words)
        allophones = {'nb': 'mb', 'nˈb': 'mˈb',
                      'nf': 'ɱf', 'nˈf': 'ɱˈf',
                      'nk': 'ŋk', 'nˈk': 'ŋˈk',
                      'ng': 'ŋg', 'nˈg': 'ŋˈg',
                      'nx': 'ŋx', 'nˈx': 'ŋˈx',
                      'xu': 'χu', 'xo': 'χo', 'xw': 'χw',
                      'n-b': 'm-b', 'n-ˈb': 'm-ˈb',
                      'n-f': 'ɱ-f', 'n-ˈf': 'ɱ-ˈf',
                      'n-k': 'ŋ-k', 'n-ˈk': 'ŋ-ˈk',
                      'n-g': 'ŋ-g', 'n-ˈg': 'ŋ-ˈg',
                      'n-x': 'ŋ-x', 'n-ˈx': 'ŋ-ˈx'
                      }
        if any(allophone in words for allophone in allophones):
            for allophone in allophones:
                words = words.replace(allophone, allophones[allophone])
        return words.replace('-', ' ')

    def transcription_fnt(self, phonology):
        words = ' '.join(phonology.words)
        syllables = '-'.join(phonology.syllables)
        words = self.__fsubstitute(words)
        syllables = self.__fsubstitute(syllables)
        return Values(self.__fsubstitute(words).split(),
                      self.__fsubstitute(syllables).split())

    @staticmethod
    def __replace_ocurrence(string, origin, to, num):
        strange_char = '$&$@$$&'
        if string.count(origin) < 0:
            return string
        elif string.count(origin) > 1:
            return string.replace(origin, strange_char, num).replace(
                strange_char, origin, num-1).replace(to, strange_char, 1)
        else:
            return string.replace(origin, to)

    def __diphthongs(self, word, syllables):
        i = 0
        j = 0
        for idx, syllable in enumerate(syllables):
            if re.search(r'[aeiouáéíóú]{2,}', syllable):
                i += 1
                syllable = re.sub(r'([aeoáééóú])i', r'\1j', syllable)
                syllable = re.sub(r'([aeoáééóú])u', r'\1w', syllable)
                word = self.__replace_ocurrence(word,
                                                syllables[idx],
                                                syllable, i)
            if re.search(r'[ui][aeiouáééiíóú]', syllable):
                j += 1
                syllable = re.sub(r'i([aeouáééiíóú])', r'j\1', syllable)
                syllable = re.sub(r'u([aeioáééiíóú])', r'w\1', syllable)
                word = self.__replace_ocurrence(word,
                                                syllables[idx],
                                                syllable, j)
            syllables[idx] = syllable
        return {'word': word, 'syllables': syllables}
