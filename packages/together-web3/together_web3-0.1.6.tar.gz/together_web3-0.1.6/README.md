# @togethercomputer/together-web3.py [![build](https://github.com/togethercomputer/together-web3.py/actions/workflows/build.yml/badge.svg)](https://github.com/togethercomputer/together-web3.py/actions/workflows/build.yml)

```python
from together_web3.computer import LanguageModelInferenceRequest
from together_web3.together import TogetherWeb3

together_web3 = TogetherWeb3()
result = await together_web3.language_model_inference(
    from_dict(
        data_class=LanguageModelInferenceRequest,
        data={
            "model": "gpt2",
            "prompt": "Alan Turing was",
        }
    ),
)
print("result", result)
```

See [examples/example.py](examples/example.py)

### Generate an image

```console
python examples/example.py "Rainbow unicorn" "StableDiffusion" \
  | grep image_base64 | cut -d\" -f4 | base64 -d > x.jpg && open x.jpg
```

## Publish to PyPi

GitHub repo > Releases > Draft a new Release > Choose a tag > Create new tag on publish >

Name the tag using the current version from pyproject.toml with a "v" e.g. `v1.0.9`.

> Publish Release

In the repo toolbar select > Actions

- Verify the publish workflow is running and completes successfully

