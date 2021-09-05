#!/usr/bin/env python3
import os
import random


import torch
import numpy as np
from faker import Faker
from loguru import logger
from transformers import GPT2LMHeadModel, GPT2Tokenizer


MODEL_NAME = os.environ.get('MODEL_NAME', 'gpt2')

if MODEL_NAME.lower() == 'gpt2':
    logger.debug('***** Running basic GPT2 pretrained weights *****')
    WEIGHTS_DIR = MODEL_NAME   # Just use the pretrained weights on hugging faces
elif MODEL_NAME.lower() == '4chan':
    # The docker container will automatically download weights to this location
    logger.debug('***** Running GPT2 trained on 3.5 years of 4Chan /pol posts (WARNING: HIGHLY OFFENSIVE OUTPUTS - YOU HAVE BEEN WARNED!!!) *****')
    WEIGHTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../weights'))
else:
    raise ValueError('Only supported models are original gpt2 or 4chan model!')

MAX_LENGTH = int(10000)  # Hardcoded max length to avoid infinite loop


cities = {
    'Arlington': 'Tarrant County',
    'Austin': 'Travis County',
    'Corpus Christi': 'Nueces County',
    'Dallas': 'Collin County',
    'El Paso': 'El Paso County',
    'Fort Worth': 'Denton County',
    'Garland': 'Collin County',
    'Houston': 'Fort Bend County',
    'Irving': 'Dallas County',
    'Laredo': 'Webb County',
    'Lubbock': 'Lubbock County',
    'Plano': 'Collin County',
    'San Antonio': 'Bexar County'
}

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
zip_codes = [
    75001,
    75006,
    75011,
    75014,
    75015,
    75016,
    75017,
    75019,
    75030,
    75038,
    75039,
    75040,
    75041,
    75042,
    75043,
    75044,
    75045,
    75046,
    75047,
    75048,
    75048,
    75049,
    75050,
    75051,
    75052,
    75053,
    75054,
    75060,
    75061,
    75062,
    75063,
    75080,
    75081,
    75082,
    75083,
    75085,
    75088,
    75089,
    75104,
    75106,
    75115,
    75116,
    75123,
    75134,
    75137,
    75138,
    75141,
    75146,
    75149,
    75150,
    75159,
    75159,
    75172,
    75180,
    75180,
    75181,
    75182,
    75182,
    75185,
    75187,
    75201,
    75202,
    75203,
    75204,
    75205,
    75206,
    75207,
    75208,
    75209,
    75210,
    75211,
    75212,
    75214,
    75215,
    75216,
    75217,
    75218,
    75219,
    75220,
    75221,
    75222,
    75223,
    75224,
    75225,
    75226,
    75227,
    75228,
    75229,
    75230,
    75231,
    75232,
    75233,
    75234,
    75234,
    75235,
    75236,
    75237,
    75238,
    75239,
    75240,
    75241,
    75242,
    75243,
    75244,
    75244,
    75245,
    75246,
    75247,
    75248,
    75249,
    75250,
    75251,
    75253,
    75254,
    75258,
    75260,
    75261,
    75262,
    75263,
    75264,
    75265,
    75266,
    75267,
    75270,
    75295,
    75313,
    75315,
    75336,
    75339,
    75342,
    75354,
    75355,
    75356,
    75357,
    75359,
    75360,
    75367,
    75370,
    75371,
    75372,
    75374,
    75376,
    75378,
    75379,
    75380,
    75381,
    75382,
    75398,
]
# TX IPs gathered from here: https://www.xmyip.com/ip-addresses/united--states/texas
ips = [
    "15.180.224.",    # San Antonio
    "15.155.5.",      # San Antonio
    "15.153.133.",    # San Antonio
    "12.56.225.",     # Dallas
    "67.10.46."       # Edinburg
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
    repetition_penalty = 1.0   # Primarily used for CTRL model, so hardcoding this value
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
        text = text[: text.find(stop_token) if stop_token else None]

        # Add the prompt at the beginning of the sequence. Remove the excess text that was used for pre-processing
        total_sequence = (
                prompt_text + text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)):]
        )

        generated_sequences.append(total_sequence)
        # print(total_sequence)

    return generated_sequences


def create_anonymous_form_batch(prompt_text='Dear Gov. Abbott,', batch_size=5):

    # Used for fake name generation
    fake = Faker(['en_US', 'es_MX'])

    text_sequences = generate_text(prompt_text, num_return_sequences=batch_size)

    form_batch = []
    for i in range(batch_size):
        city, county = random.choice(list(cities.items()))
        form_data = {
            'textarea-1': text_sequences[i],
            'text-1': random.choice(info_location),
            'text-6': 'Dr. ' + fake.name(),
            'text-2': city,
            'text-3': 'Texas',
            'text-4': str(random.randint(10000, 99999)),
            'text-5': county,
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
