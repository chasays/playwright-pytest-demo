
[toc]
# xxx(web)测试用例

用playwright-pytest来测试 xx 项目的核心功能。

可以对M端题型的排版进行截图然后对比，这样不用每一个元素都比对。

xx的工程在 xxxx 目录里面，其他的工程可以放到同一级目录下面，比如：同类webUI自动化等，或者其他需要的项目。
`core` 和` utils`里面封装的方法可以共用。

## 环境切换

在文件 globaldata/data.py 里面的变量 `CUR_ENV = 'test'` ，这样就是执行的测试环境的账号登录的，非test就是用的预发和线上环境。也可以使用`--env`从命令行传入，具体见下面[运行单个测试用例](#运行单个测试用例)。




## 框架
  TBD

```flow

```

## 依赖 

可以用 `pip install -r requirements.txt` 来安装所有的依赖。
目前运行环境是 macOS 10.14。

1. python 3.7+
2. playwright-pytest
3. [Pillow、pixelmatch](https://pypi.org/project/pixelmatch/)

`Playwright` 是一个CS架构，具体可以参考[这篇文章](https://yrq110.me/post/front-end/dive-into-playwright/)
，通过Connection 与Client 通信，收发消息执行对应的自动化操作。看完上面这篇文章对写自动化有非常好的理解，比如什么是Browser、Page。

## 如何执行

### 运行单个测试用例

用`-k` 来指定具体的用例，单独执行。
对于不同的环境，可以用`--env`来区分。
用`--env` 来指定运行的环境，`test`是测试环境，其他是预发和正式。
这里主要用于登录，预发和正式有区别需要单独实现。

```python
pytest -k test_case_invalid --headed --env test
```

### 运行测试集
在项目根目录执行如下命令，指定具体的 py 文件里面的所有 test_ * 都会被执行。
```py
python  xxx/xxx.py --alluredir=./result
allure serve result/report

```
### 配置 pytest.ini

也可以用配置pytest的配置文件`pytest.ini`，
```
addopts = --alluredir xxxx/result/report --headed

```
###  举例

举个例子，用执行answer这个测试集合。

```py
python testcase/edit/test_answer_survey.py --alluredir=./result

# 或者直接用pytest来执行test也是可以的
pytest -k test_create_anwser --headed --env test

allure serve result/report # 就可以打开页面看到结果了。
```

## 图片对比

用`pixelmatch` 对图片进行比较，并保存 diff 图片到本地。
优点是不用对比所有的元素。
缺点是比较耗时，大概一张图片对比需要5~20s左右。
```python
def test_diff_screenshot(login_fixture, assert_snapshot,request):
    page = login_fixture
    assert_snapshot(page.screenshot(), f'{request.node.name}.png')
```


## 其他更多用法
1. 参考 playwright-pytest
可以参考playwright-pytest的其他用法。
https://github.com/microsoft/playwright-pytest
   
2. 以及pytest的官方文档
https://docs.pytest.org/en/6.2.x/#
