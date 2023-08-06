
# <div align="center"><img src="https://s1.ax1x.com/2023/04/23/p9e0XDA.png" width="20%" ></img></div>

<div align="center">
<p align="center">
  <a href="#预览">预览</a> •
  <a href="#安装">安装</a> •
  <a href="#快速开始">快速开始</a> 
</p>

</div>

![version](https://img.shields.io/badge/version-v1.0.6-green)




## 新闻

 

- ❗️ 2023年4月：版本更新，支持[ChatGLM](https://github.com/THUDM/ChatGLM-6B), 可以使用SohuPrompt工具对ChatGLM进行微调。
- 2023年4月：SohuPrompt v1.0.1版本发布，欢迎大家为SohuPrompt贡献代码。

## 预览

Prompt-learning是最新的训练范式，它可以将预训练语言模型（PLMs）更好的适配下游NLP任务，详细了解请参考[Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing](https://arxiv.org/pdf/2107.13586.pdf)。SohuPrompt库提供了一个标准、灵活和可扩展的框架，用于部署prompt-learning流水线，它支持直接从[huggingface transformers](https://github.com/huggingface/transformers)加载PLMs。在未来，我们将支持[deepspeed](https://github.com/microsoft/DeepSpeed)或[colossal ai](https://github.com/hpcaitech/ColossalAI)来加快训练和预测速度。


<div align="center">


<img src="https://z3.ax1x.com/2021/11/03/IAdT3D.png" width="85%" align="center"/>

</div>




## 安装

### 使用 pip


```shell
pip install sohuprompt
```
你也可以从gitlab源安装最新版本的SohuPrompt。




## 快速开始
### 第一步 定义config
详细了解config的配置，请参考[config](sohuprompt/default_config.py)
```yaml
environment:
  num_gpus: 1
  cuda_visible_devices:
        - 1
  local_rank: 0

logging:
    path: pretrained_model/
    unique_string: chatglm

dataset:
  name: generate_comment
  path: ./data/

task: generation

dataloader:
  decoder_max_length: 128 
  max_seq_length: 128
  truncate_method: tail

train:
  num_epochs: 1
  batch_size: 1
  teacher_forcing: True
  gradient_accumulation_steps: 4
  bf16: False
  fp16: False
  deepspeed: False
  label_smoothing_factor: 0

dev:
  batch_size: 1
  shuffle_data: False

test:
  batch_size: 2
  shuffle_data: False

generation:
  parent_config: task
  max_new_tokens: 64
  num_beam_groups: 5
  num_beams: 5
  diversity_penalty: 3.0
  temperature: 2.0
  repetition_penalty: 5.0
  early_stopping: False
  length_penalty: 3.0
  bad_words_ids:
  - - 3473
    - 1837
  - - 3473
    - 27556
  - - 259
    - 3473

plm:
  model_name: chatglm 
  model_path: pretrained_model/chatglm-6b/
  optimize:
    freeze_para: True
    lr: 0.00003

template: ptuning_template
verbalizer: 

ptuning_template:
  choice: 0
  file_path: ptuning_prompt.txt
  placeholder_mapping:                                     
    <text_a>: text_a
    <text_b>: text_b
    <text_c>: text_c
```
### 第二步：加载数据集
```python
from sohuprompt.data_utils import load_dataset

train_dataset, valid_dataset, test_dataset, Processor = load_dataset(config, test=False)
# 数据集中的数据源通过config确定，config是一个yaml文件，我们通过config来对代码进行各种有效的配置
```

### 第三步：加载预训练模型
```python
from sohuprompt.plms import load_plm_from_config

plm_model, plm_tokenizer, plm_config, plm_wrapper_class = load_plm_from_config(config)
# 模型的配置也是通过config来确定的
```
### 第四步：加载prompt-template与verbalizer
```python
from sohuprompt.prompts import load_template, load_verbalizer

template = load_template(config=config, model=plm_model, tokenizer=plm_tokenizer, plm_config=plm_config)
verbalizer = load_verbalizer(config=config, model=plm_model, tokenizer=plm_tokenizer, plm_config=plm_config, classes=Processor.labels)
# template和verbalizer的配置也是通过config来确定
```
### 第五步：加载prompt-learning模型
```python
from sohuprompt.pipeline_base import PromptForClassification, PromptForGeneration

prompt_model = PromptForGeneration(plm_model, template, freeze_plm=config.plm.optimize.freeze_para, gen_config=config.generation, )
# 这里需要注意的是，prompt_model的类型是PromptForGeneration，即生成任务，如果是分类任务，那么prompt_model的类型是PromptForClassification
# prompt_model = PromptForClassification(plm_model, template, verbalizer, freeze_plm = config.plm.optimize.freeze_para)
```
### 第六步：加载dataloader
```python
from sohuprompt import PromptDataLoader

# 为了更好的适配prompt-learning，我们重新对prompt dataloader进行包装
def build_dataloader(
        dataset, template, tokenizer, tokenizer_wrapper_class, config, split
):
    dataloader = PromptDataLoader(
        dataset=dataset,
        template=template,
        tokenizer=tokenizer,
        tokenizer_wrapper_class=tokenizer_wrapper_class,
        batch_size=config[split].batch_size,
        shuffle=config[split].shuffle_data,
        teacher_forcing=config[split].teacher_forcing
        if hasattr(config[split], "teacher_forcing")
        else None,
        predict_eos_token=True if config.task == "generation" else False,
        **config.dataloader
    )
    return dataloader
# 定义完build_dataloader之后，我们就可以加载dataloader了
train_dataloader = (build_dataloader(train_dataset, template, plm_tokenizer, plm_wrapper_class, config, "train") if train_dataset else None)
valid_dataloader = (build_dataloader(valid_dataset, template, plm_tokenizer, plm_wrapper_class, config, "dev") if valid_dataset else None)
test_dataloader = (build_dataloader(test_dataset, template, plm_tokenizer, plm_wrapper_class, config, "test") if test_dataset else None)
```
### 第七步：加载trainer
```python
from sohuprompt.trainer import ClassificationRunner, GenerationRunner

runner = GenerationRunner(model=prompt_model, train_dataloader=train_dataloader, valid_dataloader=valid_dataloader, test_dataloader=test_dataloader, config=config, )
# 注意，这里的runner要与第五步中的prompt_model的类型相对应，如果是PromptForGeneration，那么runner的类型就是GenerationRunner，如果是PromptForClassification，那么runner的类型就是ClassificationRunner
# runner = ClassificationRunner(model=prompt_model, train_dataloader=train_dataloader, valid_dataloader=valid_dataloader, test_dataloader=test_dataloader, config=config, )
```
### 第八步：训练模型
```python
runner.run()
```
## 代码贡献
欢迎大家使用SohuPrompt和为SohuPrompt贡献代码

