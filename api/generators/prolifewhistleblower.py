from .. import model
from loguru import logger
from helpers.typing import APIMapping, JSONType
from faker import Faker
import random
from helpers.typing import JSONType
from data import load_data

zip_codes = load_data('zip_codes')['TX']
ip_addresses = load_data('ip_addresses')['TX']


def anonymous_form() -> JSONType:
  text_sequence = anonymous_form.queue.get()
  anonymous_form.queue.task_done()

  fake = Faker(['en_US', 'es_MX'])
  zip_code, location = random.choice(list(zip_codes.items()))
  if location['city'] in ip_addresses:
    ip_address = random.choice(ip_addresses[location['city']])
  else:
    ip_address = random.choice(random.choice(list(ip_addresses.values())))
  ip_address += str(random.randint(0, 255))

  return {
    'violation': text_sequence,
    'obtained_evidence_from': random.choice(model.info_location),
    'clinic_or_doctor': 'Dr. ' + fake.name(),
    'city': location['city'],
    'state': random.choice(['tx', 'TX', 'Texas', 'TEXAS']),
    'zip_code': zip_code,
    'county': location['countyname'],
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
