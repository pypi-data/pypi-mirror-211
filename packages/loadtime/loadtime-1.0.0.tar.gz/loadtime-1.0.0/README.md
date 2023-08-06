# LoadTime

[English](https://github.com/riversun/LoadTime/blob/main/README.md) | [&#26085;&#26412;&#35486;](https://github.com/riversun/LoadTime/blob/main/README_ja.md)


**LoadTime** is a Python package designed specifically 
to tackle the challenge of long waiting times associated 
with loading large-scale pretrained language models,
such as HuggingFace models, into GPU or CPU memory. 

<img src="https://riversun.github.io/loadtime/loadtime_std.gif">


With **LoadTime**, instead of waiting in uncertainty, 
you can visualize the progress of your loading process.


Of course, it can also be used for other long-term operations.

## Installation

You can install LoadTime via pip:

```bash
pip install loadtime
```


## Key Features

- **Real-time tracking**: LoadTime provides real-time tracking of the loading process. No more staring at a static screen!


- **Progress Bar**: The package displays a progress bar, showing you how much of the process has been completed and how much is still remaining. It takes the guesswork out of waiting!


- **Past Loading Time Cache**: One unique feature of LoadTime is its ability to remember the time it took to load a model in the past. The package automatically caches the total loading time of your operations. The next time you load the same model, LoadTime uses this cached information to provide an even more accurate progress bar.


- **Customizable Display**: LoadTime allows you to customize the progress display with your own messages. You can tailor the tool to fit your personal needs.


- **Optimized for HuggingFace Models**: LoadTime has been optimized for loading HuggingFace models, with special handling of the download progress display when the model is not cached locally.


## Basic Usage

Here is a simple example of how to use the LoadTime package:

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from loadtime import LoadTime

model_path = "togethercomputer/RedPajama-INCITE-Chat-3B-v1"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = LoadTime(name=model_path,
                 fn=lambda: AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16))()
```


## Initial Parameters

  | Parameter | Description |
    |-----------|-------------|
    | name      | Name of the long-term process. For loading HuggingFace models, specify the model name. |
    | message   | Specify the message to be displayed. If omitted, the default message is used. |
    | pbar      | Set to True to display the progress bar and percentage. |
    | dirname   | Directory name for cache storage. |
    | hf        | Set to True to use for time display for loading HuggingFace models. If the model data has not yet been downloaded to the disk, HuggingFace's loader displays the download progress, so this library does not display it. |
    | fn        | Function to execute the long-term process. |
    | fn_print  | Function to perform the display. If omitted, it will be output to the console. |


Take control of your loading times with LoadTime!


