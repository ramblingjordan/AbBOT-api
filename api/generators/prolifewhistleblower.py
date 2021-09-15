from queue import Queue
from typing import Mapping, List, cast
from helpers import model
from helpers.typos import add_typos
from helpers.typing import APIMapping, JSONType, ZIPCode
from helpers.random import WeightedLists, WeightedTuples, weighted_choice

from faker import Faker
import random
from helpers.typing import JSONType
from data import load_data

suspect_words = [
  [1.0, "suspect"], [1.0, "know"], [1.0, "discovered"], [1.0, "uncovered"], [1.0, "suspect"], [1.0, "learned"], [0.8, "figured out"],
  [1.0, "found out"], [0.3, "have reason to suspect"], [1.0, "believe"], [0.3, "have reason to believe"], [1.0, "think"],
  [0.5, "have found evidence"], [0.5, "have written evidence"], [0.5, "have audio evidence"], [0.5, "have video evidence"],
  [0.5, "have obtained evidence"], [0.5, "have evidence"], [0.2, "have strong evidence"], [1.0, "am convinced"], [1.0, "am certain"],
  [1.0, "have proof"], [1.0, "am positive"], [1.0, "am suspicious"], [1.0, "am sure"], [1.0, "can prove"], [0.8, "can legally show"],
  [0.8, "can legally prove"], [1.0, "can verify"], [0.3, "can attest"], [0.5, "can testify"], [0.5, "will testify"], [1.0, "have verified"],
  [1.0, "have verification"], [0.8, "happened upon proof"], [0.8, "happened upon evidence"], [0.8, "stumbled upon proof"],
  [0.8, "stumbled upon evidence"], [0.8, "came upon proof"], [0.8, "came upon evidence"], [0.8, "came across evidence"],
  [0.8, "came across proof"], [1.0, "uncovered proof"], [1.0, "uncovered evidence"], [1.0, "recovered proof"], [1.0, "recovered evidence"],
  [0.5, "just received proof"], [0.5, "just received evidence"], [1.0, "got evidence"], [1.0, "just got evidence"], [1.0, "just got proof"],
  [1.0, "got proof"], [1.0, "received proof"], [1.0, "received evidence"], [0.5, "got hold of proof"], [0.5, "got hold of evidence"],
  [0.5, "saved proof"], [0.5, "saved evidence"], [0.5, "have saved proof"], [0.5, "have saved evidence"], [0.5, "happen to have proof"],
  [0.5, "happen to have evidence"], [0.8, "hold the proof"], [0.8, "hold the evidence"],
  [0.8, "have the evidence"], [1.0, "have the proof"], [0.5, "will prove"], [0.5, "will legally prove"], [0.5, "will provide proof"],
  [0.5, "will show legal proof"], [0.3, "have it on video"], [0.3, "have it on film"], [0.3, "have it on a recording"],
  [1.0, "have video proof"], [1.0, "have audio proof"], [0.5, "saved screenshots as proof"], [0.5, "saved screenshots as evidence"],
  [0.5, "saved texts as proof"], [0.5, "saved texts as evidence"], [0.5, "saved messages as proof"], [0.5, "saved messages as evidence"],
  [0.8, "took screenshots as proof"], [0.8, "took screenshots as evidence"], [0.8, "saved video as proof"], [0.8, "took video as evidence"],
  [1.0, "have confirmed"], [1.0, "have confirmation"], [1.0, "know and can prove"]
]

subjects = [
  "science", "math", "history", "social studies", "chemistry", "algebra", "Spanish", "calculus", "art", "music", "gym", "English",
  "language arts", "composition", "geometry", "statistics", "physics", "earth science", "economics", "geography", "government", "French",
  "business", "political science", "engineering", "psychology"
]

my_nonfamily_words = [
  [2.0, "neighbor"], [0.6, "next-door neighbor"], [1.5, "boss"], [0.7, "landlord"], [1.5, "doctor"], [0.7, "employee"], [0.5, "roommate"],
  [1.0, "friend"], [1.0, "girlfriend"], [1.0, "boyfriend"], [0.3, "maid"], [0.2, "live-in maid"], [0.1, "live in maid"],
  [0.2, "housekeeper"], [0.1, "cleaning lady"], [2.0, "ex"], [0.3, "therapist"], [0.5, "supervisor"], [1.0, "employer"], [0.2, "lawyer"],
  [0.4, "dentist"], [0.2, "plumber"], [1.5, "pastor"], [0.5, "deacon"], [0.8, "priest"], [0.2, "accountant"], [0.5, "co-worker"],
  [0.5, "coworker"], [0.2, "colleague"], [0.2, "dry-cleaner"], [0.2, "bartender"]
]
my_family_possessive_adj: WeightedTuples = [(cast(float, k[0]), cast(str, k[1]) + "'s ") for k in my_nonfamily_words]
my_family_possessive_adj.append((20.0, ''))

my_family_words: WeightedLists = [
  [0.5, "father"], [0.5, "mother"], [1.0, "brother"], [1.0, "sister"], [0.2, "older brother"], [0.2, "older sister"],
  [0.5, "younger brother"], [0.5, "younger sister"], [1.0, "cousin"], [2.0, "aunt"], [0.5, "uncle"], [0.6, "daughter"], [0.6, "son"],
  [0.2, "step-son"], [0.1, "step son"], [0.2, "step-daughter"], [0.1, "step daughter"], [0.7, "nephew"], [0.7, "niece"],
  [0.5, "grandmother"], [0.2, "grandma"], [0.5, "grandfather"], [0.2, "grandpa"], [0.5, "granddad"], [1.0, "grandson"],
  [1.0, "granddaughter"], [1.0, "son-in-law"], [1.0, "daughter-in-law"], [1.0, "mother-in-law"], [1.0, "father-in-law"],
  [0.1, "half-brother"], [0.1, "half-sister"]
]
my_nonfamily_possessive_adj = [(k[0], cast(str, k[1]) + "'s ") for k in my_family_words]
my_nonfamily_possessive_adj.append((20.0, ''))

my_teacher_words = [
  (1.0, 'teacher'),
  *[(0.2, k + ' teacher') for k in subjects],
  (0.5, 'tutor'),
  *[(0.1, k + ' tutor') for k in subjects],
  (1.0, 'babysitter'),
  (1.0, 'instructor'),
  *[(0.2, k + ' instructor') for k in subjects],
  (0.5, 'professor'),
  *[(0.1, k + ' professor') for k in subjects],
]
my_teacher_possessive_adj = [
  [0.2, "younger brother's "], [0.1, "older brother's "], [0.2, "younger sister's "], [0.1, "older sister's "], [0.8, "brother's "],
  [0.4, "step-brother's "], [0.8, "sister's "], [0.4, "step-sister's "], [1.0, "cousin's "], [2.0, "daughter's "], [2.0, "son's "],
  [0.4, "step-son's "], [0.2, "step son's "], [0.4, "step-daughter's "], [0.2, "step daughter's "], [0.7, "nephew's "], [0.7, "niece's "]
]

violated_words = [
  [4.0, "assisted someone in violating"], [4.0, "assisted someone in breaking"], [4.0, "assisted someone in disobeying"],
  [3.0, "helped someone violate"], [3.0, "helped someone disobey"], [3.0, "helped someone break"], [3.0, "helped violate"],
  [3.0, "helped break"], [3.0, "helped disobey"], [0.4, "helped someone have an abortion, violating"],
  [0.4, "helped someone have an abortion, breaking"], [0.4, "helped someone have an abortion in violation of"],
  [0.4, "helped someone get an abortion, violating"], [0.4, "helped someone get an abortion, breaking"],
  [0.4, "helped someone get an abortion in violation of"], [0.4, "helped someone to get an abortion, violating"],
  [0.4, "helped someone to get an abortion, breaking"], [0.4, "helped someone to get an abortion in violation of"],
  [0.1, "helped someone kill her child and violate"], [0.1, "helped someone kill her baby and violate"],
  [0.1, "helped someone kill a child and violate"], [0.1, "helped someone kill a baby and violate"],
  [0.1, "helped someone kill a child and disobey"], [0.1, "helped someone kill a baby and disobey"],
  [0.1, "helped someone kill her child and disobey"], [0.1, "helped someone kill her baby and disobey"],
  [0.4, "helped someone abort her child and violate"], [0.4, "helped someone abort her baby and violate"],
  [0.4, "helped someone abort her child and disobey"], [0.4, "helped someone abort her baby and disobey"],
  [0.1, "helped someone murder her child and violate"], [0.1, "helped someone murder her baby and violate"],
  [0.1, "helped someone murder a child and disobey"], [0.1, "helped someone murder a baby and disobey"],
  [0.1, "helped someone murder her child and disobey"], [0.1, "helped someone murder her baby and disobey"],
  [0.1, "helped someone murder her child in violation of"], [0.1, "helped someone murder her baby in violation of"],
  [0.1, "helped someone murder a child in violation of"], [0.1, "helped someone murder a baby in violation of"],
  [0.1, "helped someone kill her child in violation of"], [0.1, "helped someone kill her baby in violation of"],
  [0.1, "helped someone kill a child in violation of"], [0.1, "helped someone kill a baby in violation of"],
  [0.1, "helped someone kill her child, violating"], [0.1, "helped someone kill her baby, violating"],
  [0.1, "helped someone kill a child, violating"], [0.1, "helped someone kill a baby, violating"],
  [0.1, "helped someone murder a child, violating"], [0.1, "helped someone murder a baby, violating"],
  [0.1, "helped someone murder her child, violating"], [0.1, "helped someone murder her baby, violating"],
  [0.1, "aided in the killing of a child, violating"], [0.1, "aided in the killing of a baby, violating"],
  [0.1, "aided in the killing of her child, violating"], [0.1, "aided in the killing of her baby, violating"],
  [0.1, "aided her in killing her baby, violating"], [0.1, "aided her in killing her child, violating"],
  [0.1, "aided in the killing of a child, disobeying"], [0.1, "aided in the killing of a baby, disobeying"],
  [0.1, "aided her in killing her baby, disobeying"], [0.1, "aided her in killing her child, disobeying"],
  [0.1, "aided in the killing of a child, breaking"], [0.1, "aided in the killing of a baby, breaking"],
  [0.1, "aided in the killing of her child, breaking"], [0.1, "aided in the killing of her baby, breaking"],
  [0.1, "aided in the killing of a child, breaking"], [0.1, "aided in the killing of a baby, breaking"],
  [0.1, "aided her in killing her baby, breaking"], [0.1, "aided her in killing her child, breaking"],
  [0.1, "aided her in killing her baby, breaking"], [0.1, "aided her in killing her child, breaking"],
  [0.1, "aided in the killing of a child, in violation of"], [0.1, "aided in the killing of a baby, in violation of"],
  [0.1, "aided in the killing of her child, in violation of"], [0.1, "aided in the killing of her baby, in violation of"],
  [0.1, "aided in the killing of a child, in violation of"], [0.1, "aided in the killing of a baby, in violation of"],
  [0.1, "aided her in killing her baby, in violation of"], [0.1, "aided her in killing her child, in violation of"],
  [0.1, "aided her in killing her baby, in violation of"], [0.1, "aided her in killing her child, in violation of"],
  [0.1, "aided in the killing of a child and violated"], [0.1, "aided in the killing of a baby and violated"],
  [0.1, "aided in the killing of her child and violated"], [0.1, "aided in the killing of her baby and violated"],
  [0.1, "aided her in killing her baby and violated"], [0.1, "aided her in killing her child and violated"], [5.0, "violated"],
  [2.5, "intentionally violated"], [2.5, "knowingly violated"], [2.5, "purposefully violated"], [5.0, "disregarded"],
  [2.5, "intentionally disregarded"], [2.5, "knowingly disregarded"], [2.5, "purposefully disregarded"], [5.0, "disobeyed"],
  [2.5, "intentionally disobeyed"], [2.5, "knowingly disobeyed"], [2.5, "purposefully disobeyed"], [5.0, "broke"],
  [2.5, "intentionally broke"], [2.5, "knowingly broke"], [2.5, "purposefully broke"], [5.0, "ignored"], [2.5, "intentionally ignored"],
  [2.5, "knowingly ignored"], [2.5, "purposefully ignored"], [2.0, "helped violate"], [2.0, "aided in breaking"], [2.0, "helped disobey"],
  [2.0, "aided someone in breaking"], [2.0, "assisted someone in disobeying"], [2.0, "helped a friend break"],
  [2.0, "conspired to violate"], [2.0, "colluded to break"], [2.0, "colluded in breaking"], [2.0, "colluded to violate"],
  [2.0, "conspired in violating"]
]

days_of_the_week = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
]
past_time_frames = [
  "last week", "last month", "this week", "this month", "yesterday", "a week ago", "two weeks ago", "two days ago", "on the weekend",
  "this weekend", "last weekend", "over the weekend", "this last weekend"
]
past_time_frames.extend(['last ' + k for k in days_of_the_week])
past_time_frames.extend(['on ' + k for k in days_of_the_week])
past_time_frames.extend(['last ' + k for k in days_of_the_week])
past_time_frames.extend(['on ' + k for k in days_of_the_week])
future_time_frames = [
  "next week", "this week", "tomorrow", "two days from now", "two days from today", "a week from now", "after she leaves work",
  "after work", "on the weekend", "this weekend", "next weekend", "the weekend after next", "three days from now", "three days from today",
  "right after work", "just after work", "tomorrow morning", "tomorrow evening", "next monday", "next tuesday", "next wednesday",
  "next thursday", "next friday", "this afternoon"
]
future_time_frames.extend(['next ' + k for k in days_of_the_week])
future_time_frames.extend(['on ' + k for k in days_of_the_week])

got_words = [
  "got", "secretly got", "had", "secretly had", "helped someone get", "assisted somebody in getting", "aided someone in getting",
  "drove someone to get", "conspired to get", "colluded with somebody to get", "planned to get", "consorted with a person to get",
  "worked with someone else to get", "succeeded in getting", "successfully got", "managed to get", "illegally got", "illegally had",
  "unlawfully got", "unlawfully had"
]
will_get_words = [
  "is getting", "will get", "plans on having", "is trying to get", "is trying to have", "will try to get", "is helping someone get",
  "is scheduled to get"
  "is planning to get", "is planning on getting", "plans to get", "is secretly getting", "is conspiring to get", "is colluding to get",
  "is planning to have", "is determined to get", "is adamant on getting", "will definitely get", "will surely get", "will knowingly have",
  "is having"
]

abortion_ban_words = [
  "abortion ban", "ban on abortion", "law on abortion", "recent abortion law", "abortion restrictions", "restrictions on abortion", "ban",
  "law", "legislation", "abortion law", "abortion ban", "abortion restriction", "anti-abortion law", "anti-abortion legislation",
  "abortion prohibition", "ban on abortion"
]
abortion_ban_words = [*["recently passed " + k for k in abortion_ban_words], *[k for k in abortion_ban_words]]
abortion_ban_words = [*["Texas's " + k for k in abortion_ban_words], *["the " + k for k in abortion_ban_words]]
abortion_ban_words.extend(
  [
    "Texas law", "the new law", "Texas law on abortion", "the Texas law on abortion", "the Texas abortion law",
    "the new Texas abortion law", "the recently passed Texas abortion law", "new abortion law", "Texas legislation", "the new legislation",
    "the new rule", "the new regulation", "Texas regulation", "legal code"
  ]
)
abortion_modifiers = [[0.5, ""], [0.1, " illegal"], [0.1, " unlawful"], [0.1, " illicit"], [0.05, " aspiration"]]

zip_codes: List[ZIPCode] = load_data('zip_codes')['TX']
ip_addresses: Mapping[str, List[str]] = load_data('ip_addresses')['TX']
doctors = load_data('doctors')['TX']


def anonymous_form() -> JSONType:
  text_sequence: str = queues['/anonymous-form'].get()
  queues['/anonymous-form'].task_done()

  fake: Faker = Faker(['en_US', 'es_MX'])
  location: ZIPCode = random.choice(list(zip_codes))

  ip_address: str
  if location['city'] in ip_addresses:
    ip_address = random.choice(ip_addresses[location['city']])
  else:
    ip_address = random.choice(random.choice(list(ip_addresses.values())))
  ip_address += str(random.randint(0, 255))

  doctor: str = random.choice(doctors)
  doctor = random.choice([f'Dr. {doctor}', f'Dr. {fake.first_name()} {doctor}', doctor, f'Dr. {fake.first_name()[0]}. {doctor}'])

  obtained_evidence_from = random.choice(
    [
      'A friend saw them', 'I work at the clinic', 'I know their secretary', 'They told me at the club', 'The police report',
      'Their spouse told me'
    ]
  )

  text_sequence = model.clean_text(
    text_sequence, location['city'], ['tx', 'TX', 'Texas', 'TEXAS'], ['US', 'USA', 'United States', 'America']
  )
  text_sequence = add_typos(text_sequence)
  return {
    'violation': text_sequence,
    'obtained_evidence_from': obtained_evidence_from,
    'clinic_or_doctor': doctor,
    'city': location['city'],
    'state': random.choice(['tx', 'TX', 'Texas', 'TEXAS']),
    'zip_code': location['zip'],
    'county': location['county'],
    'ip_address': ip_address,
    'elected_to_public_office': 'no',
  }


def anonymous_form_prompt() -> str:
  accused: str
  accused_type: str = weighted_choice([[1.0, 'FAMILY'], [1.5, 'NON-FAMILY'], [0.5, 'TEACHER']])
  if accused_type == 'FAMILY':
    accused = weighted_choice(my_family_possessive_adj) + weighted_choice(my_family_words)
  elif accused_type == 'NON-FAMILY':
    accused = weighted_choice(my_nonfamily_possessive_adj) + weighted_choice(my_nonfamily_words)
  elif accused_type == 'TEACHER':
    accused = weighted_choice(my_teacher_possessive_adj) + weighted_choice(my_teacher_words)

  prompt: str
  relation = random.choice(['I', 'My'])
  if relation == 'I':
    prompt = f"I {weighted_choice(suspect_words)}{weighted_choice([(0.75, ' that'), (0.25, '')])} my {accused}{random.choice([' has', ''])} {weighted_choice(violated_words)} {random.choice(abortion_ban_words)}."
  if relation == 'My':
    tense = random.choice(['past', 'future'])
    include_timeframe = random.choice([True, False])
    prompt = f"My {accused} {random.choice(got_words) if tense == 'past' else random.choice(will_get_words)} an{weighted_choice(abortion_modifiers)} abortion{' ' + (random.choice(past_time_frames) if tense == 'past' else random.choice(future_time_frames)) if include_timeframe else ''}."

  return prompt


def signup() -> JSONType:
  raise NotImplementedError()


queues: Mapping[str, Queue] = {
  '/anonymous-form': model.new_text_generator(f'/prolifewhistleblower/anonymous-form', anonymous_form_prompt),
  # '/form': model.new_text_generator('/prolifewhistleblower/signup', 'PROMPT HERE'),
}

api: APIMapping = {
  '/anonymous-form': anonymous_form,
  # '/signup': signup,
}
