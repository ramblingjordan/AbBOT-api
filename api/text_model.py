#!/usr/bin/env python3
import os
import random
import json

import torch
import numpy as np
from faker import Faker
from loguru import logger
from transformers import GPT2LMHeadModel, GPT2Tokenizer

with open(os.path.join(os.path.dirname(__file__), './txzips.json')) as zips_file:
  zips = json.load(zips_file)

MODEL_NAME = os.environ.get('MODEL_NAME', 'gpt2')

if MODEL_NAME.lower() == 'gpt2':
  logger.debug('***** Running basic GPT2 pretrained weights *****')
  WEIGHTS_DIR = MODEL_NAME  # Just use the pretrained weights on hugging faces
elif MODEL_NAME.lower() == '4chan':
  # The docker container will automatically download weights to this location
  logger.debug(
    '***** Running GPT2 trained on 3.5 years of 4Chan /pol posts (WARNING: HIGHLY OFFENSIVE OUTPUTS - YOU HAVE BEEN WARNED!!!) *****'
  )
  WEIGHTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../weights'))
else:
  raise ValueError('Only supported models are original gpt2 or 4chan model!')

MAX_LENGTH = int(10000)  # Hardcoded max length to avoid infinite loop

gop_members = [
  'Gary VanDeaver', 'Bryan Slaton', 'Cecil Bell Jr.', 'Keith Bell', 'Cole Hefner', 'Matt Schaefer', 'Jay Dean', 'Cody Harris',
  'Chris Paddie', 'Travis Clardy', 'Kyle Kacal', 'Ben Leman', 'John N. Raney', 'Steve Toth', 'Will Metcalf', 'John Cyrier', 'Ernest Bailes',
  'James White', 'Terry Wilson', 'Dade Phelan', 'Mayes Middleton', 'Greg Bonnen', 'Cody Vasut', 'Brooks Landgraf', 'Tom Craddick',
  'Dustin Burrows', 'John Frullo', 'Phil Stephenson', 'John T. Smithee', 'Four Price', 'Ken King', 'Candy Noble', 'Stephanie Klick',
  'Jeff Cason', 'Matt Krause', 'Tony Tinderholt', 'David Cook', 'Craig Goldman', 'Giovanni Capriglione', 'Charlie Geren', 'Sam Harless',
  'Dan Huberty', 'Briscoe Cain', 'Dennis Paul', 'Tom Oliverson', 'Mike Schofield'
]
firstNames = ['Hannah', 'Olivia', 'Marcia', 'Sarah', 'Tara', 'Brooke', 'Wanda', 'Andrea', 'Julie']
lastNames = ['Morgan', 'Walker', 'Lewis', 'Butler', 'Jones', 'Barnes', 'Martin', 'Wright', 'Foster']

info_location = [
  'A friend saw them', 'I work at the clinic', 'I know his secretary', 'He told me at the club', 'The police report', 'His wife told me'
]

# TX IPs gathered from here: https://www.xmyip.com/ip-addresses/united--states/texas
ips = [
  "15.180.224.",  # San Antonio
  "15.155.5.",  # San Antonio
  "15.153.133.",  # San Antonio
  "12.56.225.",  # Dallas
  "67.10.46."  # Edinburg
]
# random element from each list


def sign_up_page():
  raise NotImplementedError()


def set_random_seed(seed, n_gpu):
  np.random.seed(seed)
  torch.manual_seed(seed)
  if n_gpu > 0:
    torch.cuda.manual_seed_all(seed)


def adjust_seq_length_to_model(length, max_sequence_length):
  if length < 0 and max_sequence_length > 0:
    length = max_sequence_length
  elif 0 < max_sequence_length < length:
    length = max_sequence_length  # No generation bigger than model size
  elif length < 0:
    length = MAX_LENGTH  # avoid infinite loop
  return length


def generate_text(prompt_text: str, k=50, p=0.9, seq_length=150, seed=None, temperature=1.0, num_return_sequences=1):
  """ Create a synthetic text sequence using a pretrained model. """
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  n_gpu = 0 if device == 'cpu' else torch.cuda.device_count()
  repetition_penalty = 1.0  # Primarily used for CTRL model, so hardcoding this value
  stop_token = "<EOS>"

  seed = seed if seed is not None else np.random.randint(0, 1000000)
  set_random_seed(seed, n_gpu)

  # Initialize the model and tokenizer
  model_class, tokenizer_class = (GPT2LMHeadModel, GPT2Tokenizer)

  tokenizer = tokenizer_class.from_pretrained(WEIGHTS_DIR)
  model = model_class.from_pretrained(WEIGHTS_DIR)
  model.to(device)

  seq_length = adjust_seq_length_to_model(seq_length, max_sequence_length=model.config.max_position_embeddings)

  encoded_prompt = tokenizer.encode(prompt_text, add_special_tokens=True, return_tensors="pt")
  encoded_prompt = encoded_prompt.to(device)

  if encoded_prompt.size()[-1] == 0:
    input_ids = None
  else:
    input_ids = encoded_prompt

  output_sequences = model.generate(
    input_ids=input_ids,
    max_length=seq_length + len(encoded_prompt[0]),
    temperature=temperature,
    top_k=k,
    top_p=p,
    repetition_penalty=repetition_penalty,
    do_sample=True,
    num_return_sequences=num_return_sequences,
  )

  # Remove the batch dimension when returning multiple sequences
  if len(output_sequences.shape) > 2:
    output_sequences.squeeze_()

  generated_sequences = []

  for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
    # print("=== GENERATED SEQUENCE {} ===".format(generated_sequence_idx + 1))
    generated_sequence = generated_sequence.tolist()

    # Decode text
    text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

    # Remove all text after the stop token
    text = text[:text.find(stop_token) if stop_token else None]

    # Add the prompt at the beginning of the sequence. Remove the excess text that was used for pre-processing
    total_sequence = (prompt_text + text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)):])

    generated_sequences.append(total_sequence)
    # print(total_sequence)

  return generated_sequences


def create_anonymous_form_batch(prompt_text='Dear Gov. Abbott,', batch_size=5):

  # Used for fake name generation
  fake = Faker(['en_US', 'es_MX'])

  text_sequences = generate_text(prompt_text, num_return_sequences=batch_size)

  form_batch = []

  for i in range(batch_size):
    zipKey = random.choice(list(zips["texaszips"]))
    zipObj = zips["texaszips"][zipKey]

    userLocation = {
      'userCity': zipObj["city"],
      'userCounty': zipObj["countyname"],
      'userState': zipObj["statename"] if random.choice([True, False]) else zipObj["stateid"],
      'userZip': zipKey,
    }
    form_data = {
      'textarea-1': text_sequences[i],
      'text-1': random.choice(info_location),
      'text-6': 'Dr. ' + fake.name(),
      'text-2': userLocation['userCity'],
      'text-3': userLocation['userState'],
      'text-4': userLocation['userZip'],
      'text-5': userLocation['userCounty'],
      'hidden-1': random.choice(ips) + str(random.randint(0, 255)),
      'checkbox-1[]': 'no',
    }
    form_batch.append(form_data)
  return form_batch


def _test_form_generator():
  prompt_text = f'Dear {random.choice(gop_members)},'
  form_batch = create_anonymous_form_batch(prompt_text, batch_size=3)
  logger.info(form_batch)


if __name__ == "__main__":
  _test_form_generator()
