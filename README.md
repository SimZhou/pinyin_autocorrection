## Pinyin Autocorrection

This is a simple pinyin autocorrection resolution. 

This repository is for learning and communicating purpose only. 

![](https://github.com/SimZhou/pinyin_autocorrection/blob/master/doc/Pinyin%20Autocorrection.png?raw=true)

## Functions

#### 1. Pinyin correction

This program takes a sequence of pinyin as input, and guesses the most possible sequence you want. 

For instance, 

if you wanna type "苹果" and inputs "zhognguo" (which is wrong), the program fixs it into "zhongguo":

```python
>>> correct("zhognguo")
"zhongguo"
```

if you wanna type "清华大学" and you made it wrong with "qignhuadaxeu", it will be fixed into "qinghuadaxue":

```python
>>> correct("qignhuadaxeu")
"qinghuadaxue"
```

#### 2. Pinyin split

This function splits a continuous sequence of pinyin inputs into separate tokens. For example:

```python
>>> split("pingguo")
"ping guo"
>>> split("qinghuadaxue")
"qing hua da xue"
```

### Algorithm

The algorithm under the hood is basically *edit distance* + *probabilistic model* + *n-gram*. 

