from typing import Dict, List, Optional, TypedDict
from .random import weighted_choice
import random
import re


def generate_odds():
  return 1.0 - (random.betavariate(0.5, 0.15) * 0.3 + 0.699995)


class Odds(TypedDict):
  letters: float
  letter_casing: float
  whitespace: float
  punctuation: float


def add_typos(text: str, odds: Optional[Odds] = None):
  if odds is None:
    letters = weighted_choice([(0.9, generate_odds()), (0.1, 0.0)])
    odds = {
      'letters': letters,
      'letter_casing': random.random(),
      'whitespace': generate_odds() / 2.0,
      'punctuation': (generate_odds() + letters**0.5) / 2.0
    }

  # Convert multi-letter substitutions into specific unicode characters for easier processing
  QU = '\u2600'
  EI = '\u2601'
  IES = '\u2602'
  IE = '\u2603'
  ES = '\u2604'
  IE_SPACE = '\u2605'
  APOSTROPHE_S = '\u2606'

  text = text.replace('qu', QU)
  text = text.replace('ei', EI)
  text = text.replace('ies', IES)
  text = text.replace('ie', IE)
  text = text.replace('es', ES)
  text = text.replace('ie ', IE_SPACE)
  text = text.replace('\'s', APOSTROPHE_S)

  subtitutions = {
    'a': [
      # First element is always 1 - odds['letters'] and it's always the correct
      # letter. The rest of the elements are incorrect substitutions.
      # They can also be multiple letters or zero letters.
      (1 - odds['letters'], 'a'),
      (0.2 * odds['letters'], 'e'),
      (0.1 * odds['letters'], 'i')
    ],
    'b': [
      (1 - odds['letters'], 'b'),
      (0.2 * odds['letters'], 'p'),
      (0.1 * odds['letters'], 'h'),
      (0.1 * odds['letters'], 'n'),
    ],
    'c': [
      (1 - odds['letters'], 'c'),
      (0.1 * odds['letters'], 'ts'),
      (0.3 * odds['letters'], 's'),
      (0.3 * odds['letters'], 'k'),
    ],
    'd': [
      (1 - odds['letters'], 'd'),
      (0.5 * odds['letters'], 't'),
    ],
    'e': [
      (1 - odds['letters'], 'e'),
      (0.1 * odds['letters'], 'a'),
      (0.5 * odds['letters'], 'i'),
    ],
    'f': [
      (1 - odds['letters'], 'f'),
      (0.5 * odds['letters'], 'v'),
    ],
    'g': [
      (1 - odds['letters'], 'g'),
      (0.1 * odds['letters'], 'k'),
    ],
    'h': [
      (1 - odds['letters'], 'h'),
      (0.2 * odds['letters'], ''),
    ],
    'i': [
      (1 - odds['letters'], 'i'),
      (0.3 * odds['letters'], 'e'),
      (0.1 * odds['letters'], 'a'),
      (0.01 * odds['letters'], 'k'),
    ],
    'j': [
      (1 - odds['letters'], 'j'),
      (0.01 * odds['letters'], 'ch'),
    ],
    'k': [(1 - odds['letters'], 'k'), (0.1 * odds['letters'], 'g'), (0.4 * odds['letters'], 'c')],
    'l': [
      (1 - odds['letters'], 'l'),
      (0.03 * odds['letters'], 'r'),
      (0.03 * odds['letters'], 'w'),
    ],
    'm': [
      (1 - odds['letters'], 'm'),
      (0.5 * odds['letters'], 'n'),
    ],
    'n': [(1 - odds['letters'], 'n'), (0.5 * odds['letters'], 'n'), (0.2 * odds['letters'], 'b')],
    'o': [(1 - odds['letters'], 'o'), (0.2 * odds['letters'], 'u'), (0.1 * odds['letters'], 'p')],
    'p': [
      (1 - odds['letters'], 'p'),
      (0.5 * odds['letters'], 'b'),
      (0.2 * odds['letters'], 'o'),
    ],
    QU: [
      (1 - odds['letters'], 'qu'),
      (0.9 * odds['letters'], 'kw'),
      (0.1 * odds['letters'], 'q'),
    ],
    'r': [(1 - odds['letters'], 'r'), (0.3 * odds['letters'], 'l'), (0.1 * odds['letters'], 't')],
    's': [(1 - odds['letters'], 's'), (0.2 * odds['letters'], 'z')],
    't': [(1 - odds['letters'], 't'), (0.5 * odds['letters'], 'd'), (0.3 * odds['letters'], 'th'), (0.1 * odds['letters'], 'r')],
    'u': [
      (1 - odds['letters'], 'u'),
      (0.01 * odds['letters'], 'yu'),
      (0.2 * odds['letters'], 'o'),
      (0.1 * odds['letters'], ''),
    ],
    'v': [(1 - odds['letters'], 'v'), (odds['letters'], 'f')],
    'w': [
      (1 - odds['letters'], 'w'),
      (0.5 * odds['letters'], ''),
    ],
    'x': [
      (1 - odds['letters'], 'x'),
      (0.6 * odds['letters'], 'ks'),
      (0.1 * odds['letters'], 'z'),
    ],
    'y': [(1 - odds['letters'], 'y'), (0.5 * odds['letters'], 'u'), (0.2 * odds['letters'], 'h'), (0.1 * odds['letters'], 'j')],
    'z': [(1 - odds['letters'], 'z'), (0.9 * odds['letters'], 's'), (0.05 * odds['letters'], 'x')],
    EI: [(1 - odds['letters'], 'ei'), (1.0 * odds['letters'], 'ie')],
    IE: [(1 - odds['letters'], 'ie'), (1.0 * odds['letters'], 'ei')],
    ES: [(1 - odds['letters'], 'es'), (1.0 * odds['letters'], 's')],
    IES: [(1 - odds['letters'], 'ies'), (1.0 * odds['letters'], 'ys')],
    IE_SPACE: [(1 - odds['letters'], 'ie'), (1.0 * odds['letters'], 'y')],
    ',': [
      (1 - odds['punctuation'], ','),
      (0.9 * odds['punctuation'], ''),
      (0.1 * odds['punctuation'], '.'),
    ],
    '.': [
      (1 - odds['punctuation'], '.'),
      (0.3 * odds['punctuation'], ''),
      (0.1 * odds['punctuation'], ' .'),
      (0.01 * odds['punctuation'], '>'),
      (0.3 * odds['punctuation'], ','),
    ],
    APOSTROPHE_S: [
      (1 - odds['punctuation'], "'s"), (0.7 * odds['punctuation'], "s"), (0.1 * odds['punctuation'], "s'"),
      (0.2 * odds['punctuation'], "'")
    ],
    "'": [(1 - odds['punctuation'], "'"), (1.0 * odds['punctuation'], "")]
  }

  whitespace_substitutions = [
    (1 - odds['whitespace'], ' '),
    (0.9 * odds['whitespace'], ''),
    (0.1 * odds['whitespace'], '  '),
  ]

  words = text.split()
  final_words: List[str] = []
  misspelled_words: Dict[str, str] = {}
  for word in words:
    previous_character_input = ''
    previous_character_output = ''
    word_output = ''

    # Use the same misspelled words about half of the time.
    if word in misspelled_words and random.choice([True, False]):
      final_words.append(misspelled_words[word])
      continue

    for character in word:
      if character in subtitutions:
        # Increase the odds that repeated characters (like 'oo' in 'cool') are not substituted.
        if character == previous_character_input and random.random() > odds['letters']:
          word_output += character
        else:
          # Emulate a potential typo based on weights defined above.
          previous_character_output = weighted_choice(subtitutions[character])
          word_output += previous_character_output
      else:
        word_output += character
      previous_character_input = character

    if word_output != word:
      misspelled_words[word] = word_output
    final_words.append(word_output)

  output = ' '.join(final_words)

  if odds['letter_casing'] < 0.1:
    output = weighted_choice([(0.8, output.lower()), (0.2, output.upper())])

  output = re.sub(r' ', lambda _: weighted_choice(whitespace_substitutions), output)
  return output
