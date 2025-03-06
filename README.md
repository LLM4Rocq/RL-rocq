# RL-rocq

Exploring RL methods for writing proofs in Rocq.

## Install

To be able to communicate with the Rocq proof assistant, you need to install a custom version of [coq-lsp](https://github.com/ejgallego/coq-lsp). The custom version is available at https://github.com/LLM4Rocq/coq-lsp/tree/MorePetanqueCommands. Because this is a custom version of coq-lsp, a specific version of [coq](https://github.com/coq/coq) is needed. The complete installation using the [OPAM package manager](https://opam.ocaml.org/) (for Unix-like systems) can be done as follow:

```bash
$ opam switch create custom_coq_lsp 5.1.0   # Optional: create a new switch
$ opam pin add rocq-runtime https://github.com/coq/coq.git#7d4ec9ecfef45f6536d144b3d7919e4129d73274
$ opam pin add rocq-core https://github.com/coq/coq.git#7d4ec9ecfef45f6536d144b3d7919e4129d73274
$ opam pin add rocq-stdlib https://github.com/coq/stdlib.git#155be26dc10a8b6ddb3cfbdd4c144c077c583b5f
$ opam pin add rocq https://github.com/coq/coq.git#7d4ec9ecfef45f6536d144b3d7919e4129d73274
$ opam pin add coq-core https://github.com/coq/coq.git#7d4ec9ecfef45f6536d144b3d7919e4129d73274
$ opam pin add coq-stdlib https://github.com/coq/stdlib.git#155be26dc10a8b6ddb3cfbdd4c144c077c583b5f
$ opam pin add coqide-server https://github.com/coq/coq.git#7d4ec9ecfef45f6536d144b3d7919e4129d73274
$ opam pin add coq https://github.com/coq/coq.git#7d4ec9ecfef45f6536d144b3d7919e4129d73274
$ opam install lwt logs   # Needed for petanque to work
$ opam pin coq-lsp https://github.com/LLM4Rocq/coq-lsp.git#MorePetanqueCommands
```

Additionally, the python package [pytanque](https://github.com/LLM4Rocq/pytanque) is required:

```bash
$ pip install git+https://github.com/LLM4Rocq/pytanque.git@MoreCommands
```

## Getting started

First launch `pet-server` in a terminal

```bash
$ pet-server
```

The default configuration can be found in [conf/config.yaml](conf/config.yaml).
You can override every field (see below).

Then you can run the training using Hugging Face command as follow:

```bash
$ accelerate launch train.py
```

Additionally, you can use vLLM to speed up the training.
When using vLLM, a GPU is required exclusively for generation.
This means you need at least two available GPUs and must ensure that one remains unused by the trainer.
To achieve this, run the training with `--num_processes <NUMBER_OF_GPUs - 1>`.
For example, if you have 4 GPUs, run the training with:

```bash
$ accelerate launch --multi_gpu --num_processes 3 train.py
```

## Configurations

We use [hydra](https://hydra.cc/docs/intro/) to manage the configurations.

```bash
$ python train.py --help
train is powered by Hydra.

You can use your own config file with the option `--config-name my_config.yaml`.
Config files should be in the `conf` directory.

== Config ==
Override anything in the config (foo.bar=value)

Powered by Hydra (https://hydra.cc)
Use --hydra-help to view Hydra specific help
```

You can use your own configuration file by putting it in the folder [conf](./conf) and writing:
