# libra-core

## build过程

1、python setup.py sdist bdist_wheel 后会产生dist/libra_core_py-0.0.x.tar.gz

2、本地安装：pip install dist/libra_core_py-0.0.x.tar.gz

3、测试无问题后，twine upload dist/* ，提示输入账号和密码（在.pypirc文件里）

4、上传成功后可以在 https://pypi.org/project/libra-core-py/ 可查看最新版本。

说明：上传成功后在应用的项目里修改libra_core_py的版本，需要注意的是，如果docker使用的是国内镜像源，最新版本可能需要一天后才能install上。

## 配置文件

1、依赖libra-core的项目需要在项目根目录创建settings.ini文件。在多环境的情况，可以通过环境后缀区分配置文件，settings.test.ini。
以libra-crawler为例，通过环境变量SETTING_FILE传入settings文件名。

2、应用的项目需要在在执行脚本的入口处调用log_init_config进行系统的配置初始化工作。原理上来说，config是以代码文件当前目录查找settings文件，
如果找不到，则到上一层路径查找。所以，如果不在脚本启动的时候初始化config，容易造成找不到配置文件的情况。

3、config包含local和apollo两种，当前除了log路径，建议其他配置都写到apollo。

4、config函数的使用方式可参考test/test_config.py。

## 日志

1、日志文件输出格式和java日志一致。

2、log默认使用自己的日志切割模式，但在多进程环境下，日志切割会有问题，这时log_init_config里的use_rotate需要为False，
然后使用操作系统的logrotate配置日志切割模式。

3、set_log_callback可用于对日志的特定处理，比如将日志存到数据库等。

