from helpers import model
from helpers.typing import APIMapping, JSONType

from faker import Faker
import random
from helpers.typing import JSONType
from data import load_data

zip_codes = load_data('zip_codes')['TX']
ip_addresses = load_data('ip_addresses')['TX']
doctors = load_data('doctors')['TX']


def anonymous_form() -> JSONType:
  text_sequence = anonymous_form.queue.get()
  anonymous_form.queue.task_done()

  fake = Faker(['en_US', 'es_MX'])
  location = random.choice(list(zip_codes))

  if location['city'] in ip_addresses:
    ip_address = random.choice(ip_addresses[location['city']])
  else:
    ip_address = random.choice(random.choice(list(ip_addresses.values())))
  ip_address += str(random.randint(0, 255))

  doctor = random.choice(doctors)
  doctor = random.choice([f'Dr. {doctor}', f'Dr. {fake.first_name()} {doctor}', doctor, f'Dr. {fake.first_name()[0]}. {doctor}'])

  obtained_evidence_from = random.choice(
    [
      'A friend saw them', 'I work at the clinic', 'I know their secretary', 'They told me at the club', 'The police report',
      'Their spouse told me'
    ]
  )

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


def signup() -> JSONType:
  raise NotImplementedError()


anonymous_form.queue = model.new_text_generator(f'/prolifewhistleblower/anonymous-form', 'Dear Gov. Abbott,')
# signup.queue  = model.new_text_generator('/prolifewhistleblower/signup', 'PROMPT HERE')

api: APIMapping = {
  '/anonymous-form': anonymous_form,
  '/signup': signup,
}
