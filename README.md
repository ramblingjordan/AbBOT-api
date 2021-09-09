# Overview

This implements a dockerized version of GPT2 optimized for "impolite" text generation and an API for easy use.

To help prevent abuse, the code here is for inference only using pretrained weights (weights automatically download
when building container).

## Quickstart

First, build the docker image.

```bash
docker image build -t dev-abbot-model .
```

Then, to startup the inference engine:

```bash
docker container run -e MODEL_NAME="gpt2" -p 5000:5000 --rm dev-abbot-model

# Note: This will take a long time to run the first time as it downloads the pretrained weights from hugging faces
at request time. TODO: The dockerfile needs to be updated to do this during the image build.
```

If you're interested in the nuclear option, you can run the engine using weights that were fine-tuned on 3.5 years of
4Chan /pol posts (NSFW! In fact, not really safe for anyone...)

After the container starts up, you can test the endpoint using by using curl or visiting in your browser:

```bash
curl http://localhost:5000/getFormBatch
```

You should get an output response like below that contains a list of the forms (each call creates a batch of forms):

```json
[{
    "data": {
        "textarea-1": [
            "Dear House Member Dennis Paul, what do you think about Donald Trump? Is it wise to let him run the show and not the media? I have a question for you. What would you do if Hillary was elected? Would you join the NRA? No, I would not. What would you do if Trump were to lose? NRA..."
        ],
        "text-1": "The police report",
        "text-6": "Dr. Gary Roberts",
        "text-2": "San Antonio",
        "text-3": "Texas",
        "text-4": "78201",
        "text-5": "Bexar County",
        "hidden-1": "15.155.5.114",
        "checkbox-1[]": "no"
    },
    "msg": "Successfully created anonymous form!",
    "status": 200
}]
```

## Attribution

### TX Zip Codes

Original csv file with zip code data obtained from [simplemaps](https://simplemaps.com/data/us-zips), under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/). Data for all TX zip codes was pulled from the csv file and formatted to JSON in the txzips.json file.
