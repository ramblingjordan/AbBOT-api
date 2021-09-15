#!/usr/bin/env python3
from os import environ, path

from queue import Queue
from threading import Thread
from typing import Callable, List, NoReturn, Optional, Union, cast

import torch
import numpy as np
from loguru import logger
from transformers import GPT2LMHeadModel, GPT2Tokenizer

import random
from nltk import sent_tokenize
import locationtagger

MODEL_NAME: str = environ.get('MODEL_NAME', 'gpt2')
try:
  WEIGHTS_DIR: str = {'gpt2': 'gpt2', '4chan': path.abspath(path.join(path.dirname(path.curdir), '../weights'))}[MODEL_NAME]
  logger.debug(f"Using '{MODEL_NAME}' model.")
except KeyError:
  raise ValueError("Environment variable MODEL_NAME must be either 'gpt2' or '4chan'")

MAX_LENGTH = 10000  # Hardcoded max length to avoid infinite loop


def set_random_seed(seed, n_gpu):
  np.random.seed(seed)
  torch.manual_seed(seed)
  if n_gpu > 0:
    torch.cuda.manual_seed_all(seed)


def adjust_seq_length_to_model(length: int, max_sequence_length: int):
  if length < 0 and max_sequence_length > 0:
    return max_sequence_length
  elif 0 < max_sequence_length < length:
    return max_sequence_length  # No generation bigger than model size
  elif length < 0:
    return MAX_LENGTH  # avoid infinite loop
  else:
    return length


def generate_text(
  prompt_text: str,
  k: int = 50,
  p: float = 0.9,
  seq_length: int = 150,
  seed: Optional[int] = None,
  temperature: float = 1.0,
  num_return_sequences: int = 5
):
  """ Create a synthetic text sequence using a pretrained model. """
  device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  n_gpu = 0 if device == 'cpu' else torch.cuda.device_count()
  repetition_penalty: float = 1.0  # Primarily used for CTRL model, so hardcoding this value
  stop_token: str = "<|endoftext|>"

  set_random_seed(seed or np.random.randint(0, 1000000), n_gpu)

  # Initialize the model and tokenizer
  model_class, tokenizer_class = (GPT2LMHeadModel, GPT2Tokenizer)
  tokenizer: GPT2Tokenizer = tokenizer_class.from_pretrained(WEIGHTS_DIR)
  model = model_class.from_pretrained(WEIGHTS_DIR)
  model.to(device)

  encoded_prompt = tokenizer.encode(prompt_text, add_special_tokens=True, return_tensors="pt")
  encoded_prompt = encoded_prompt.to(device)
  if encoded_prompt.size()[-1] == 0:
    input_ids = None
  else:
    input_ids = encoded_prompt

  max_length = adjust_seq_length_to_model(seq_length, max_sequence_length=model.config.max_position_embeddings)
  output_sequences = model.generate(
    input_ids=input_ids,
    max_length=max_length + len(encoded_prompt[0]),
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
  for _, generated_sequence in enumerate(output_sequences):
    generated_sequence = generated_sequence.tolist()
    text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

    # Remove all text after the stop token
    text = text[:text.find(stop_token) if stop_token else None]

    # Add the prompt at the beginning of the sequence. Remove the excess text that was used for pre-processing
    total_sequence = (prompt_text + text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)):])
    generated_sequences.append(total_sequence)
  return generated_sequences


def new_text_generator(name: str, prompt_text: Union[str, Callable[[], str]], **kwargs) -> Queue:
  BATCH_SIZE: int = int(environ.get('API_BATCH_SIZE', 5))
  queue: Queue = Queue(maxsize=int(BATCH_SIZE))

  def generate_to_queue() -> NoReturn:
    while True:
      kwargs['num_return_sequences'] = BATCH_SIZE
      prompt: str = prompt_text() if callable(prompt_text) else prompt_text

      logger.debug(f'Generating {BATCH_SIZE} more sequences for {name}')
      batch: str = generate_text(prompt, **kwargs)
      logger.debug(f'Done generating sequences for {name}')
      for item in batch:
        queue.put(item)

  logger.debug(f'Starting generation thread for {name}')
  generate_thread: Thread = Thread(target=generate_to_queue)
  generate_thread.start()
  return queue


TEXT_REPLACEMENTS = {
  '\nAdvertisement\n': '',
  '[pullquote]': '',
  '\n': ' ',
  '"': '',
}


def clean_text(text: str, city: Union[str, List[str]], state: Union[str, List[str]], country: Union[str, List[str]]) -> str:
  for k, v in TEXT_REPLACEMENTS.items():
    text = text.replace(k, v)

  text = ' '.join(sent_tokenize(text)[:-1])  # TODO: Not sure why this is here, it just removes the last sentence.
  text = text.encode('ascii', 'ignore').decode()  # Removes leftover unicode characters

  def random_choice_or_str(values: Union[str, List[str]]) -> str:
    if type(values) == list:
      return random.choice(values)
    else:
      return cast(str, values)

  # Replace references to locations to match the correct city/state/country.
  place = locationtagger.find_locations(text=text)
  for replacements, found in ((city, place.cities), (state, place.regions), (country, place.countries)):
    for item in found:
      if not (item in replacements or item == replacements):
        logger.debug(f'Replacing {item} with {replacements} because item != replacement')
        text = text.replace(item, random_choice_or_str(replacements))
  return text
