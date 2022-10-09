## 在虚拟机中安装：GAMIT10.71

### 一、安装虚拟机

本人使用的是VM16.0 PRO

安装包下载：微信公众号（安装包中自带有安装教程）

### 二、安装ubuntu

本人使用的是：ubuntu22.04.1LST

ubuntu系统官网下载链接：[Download Ubuntu Desktop | Download | Ubuntu](https://ubuntu.com/download/desktop)

安装教程请看博文：《VMware虚拟机安装Ubuntu20.04详细图文教程》

链接：https://blog.csdn.net/weixin_41805734/article/details/120698714

### 三、安装GAMIT10.71

软件获取：网上自行下载。或者去我的GitHub仓库

Ubuntu安装完成。

（1）以普通用户登录系统，创建root用户的密码，在终端输入命令：

```
sudo passwd root
```

（2）安装必要的组件：

```
sudo apt-get install csh
sudo apt-get install tcsh
sudo apt-get install gcc
sudo apt-get install gfortran
sudo apt-get install libx11
sudo apt-get install ftp
apt-get install curl
apt-get install ncftp
apt-get install gmt
apt-get install make
```

（3）安装完成后，为了避免后续安装失败，需要进行一下操作：

安装快结束时会出现的错误：

```
Error: Type mismatch between actual argument at (1) and actual argument at (2) (INTEGER(2)/INTEGER(4)). make: *** [Makefile:164: com_lib.a(get_value.o)] Error 1 Failure in make_gamit -- install_software terminated
```

解决办法：

以上问题说明可能是**编译器版本的问题**，在命令行输入：

```
gfortran -v #查看gortran版本
gcc -v      #查看gcc版本
```

 发现版本均为11.xx，对比曾经成功安装的服务器上的版本为9.xx，因此认为是**gcc、gfortran版本过高导致编译出问题\***。

解决步骤：

1、在命令行输入以下命令，下载9.xx版本的gcc、gfortran

    sudo apt-get install gcc-9
    sudo apt-get install gfortran-9   

2.继续输入命令，调整编译器默认使用的版本：

调整gcc-11的优先级为40，gcc-9的优先级为100

```
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 40
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 100
```

调整gfortran-11的优先级为40，gfortran-9的优先级为100

```
sudo update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-11 40
sudo update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-9 100
```

参考的原文链接：https://blog.csdn.net/qq_36107898/article/details/126705712

（4）将window下的安装包移动到Ubuntu的opt文件中：“Other Locations”-"Computer"-“opt”

（5）进入opt找到安装包，右键选择在终端中打开（也可以在终端中用cd指令打开）

输入指令运行安装程序：

```text
./install_software
```

（6）输入y回车就可以开始安装，这里在安装过程中需要注意，当问到“Are these paths complete and correct in your system”时不要着急回车。复制命令行中的两行文件位置，打开“安装包”-“libraries”找到“Makefile.config”双击打开，此时要进行3处更改：

```
一、修改 X11 的路径
需要做的是将文档中 X11 的路径从
X11LIBPATH /usr/lib/X11
X11INCPATH /usr/include/X11
修改为
X11LIBPATH /usr/lib/x86_64-linux-gnu
X11INCPATH /usr/include/X11

二、修改 GAMIT 的一些内部参数
分别是MAXSIT（最大测站数）、MAXSAT（最大卫星颗数）、MAXATM（最大天顶延迟）和MAXEPC（最大历元数）。这里需要改的将MAXSIT改为99，MAXSAT改为40，MAXATM改为25，MAXEPC改为8640。
修改前：
MAXSIT 80
MAXSAT 32
MAXATM 13
MAXEPC 2880
修改后：
MAXSIT 99
MAXSAT 40
MAXATM 25
MAXEPC 8640

三、检查 Linux 操作系统版本号
Ctrl+F 查找“Linux"
OS_ID Linux 0001 4930
另开一个终端，输输入命令查看自己的 Linux 版本： uname -a
只需记住linux版本的前四位编号，如果小于4930，不需要修改，如果大于4930，则修改为自己的linux版本的前四位编号。笔者的linux版本4.4.0-17763-Microsoft，则编号为4400，小于4930不需修改。
原文链接：https://blog.csdn.net/m0_65958744/article/details/124987220
```

（7）更改完成并保存后，重新./install_software，之后一直点“y”，直到安装结束。

结束标志：

```
+++++++++++++
GLOBK installed
+++++++++++++
Greate the gg link in your home directory to the version of gamit/globk you just 
installed?(y/n)
```

（8）配置 GAMIT 环境变量

```
在Home界面，ctrl+H，显示隐藏的文件，找到bashrc文件
打开.bashrc 文档后，将以下代码加在在文档末尾：
export PATH="$PATH:/opt/gamit10.71/gamit/bin:/opt/gamit10.71/com:/opt/gamit10.71/kf/bin"
export HELP_DIR=/opt/gamit10.71/help
需要注意的是，这里的路径必须是用户自己安装 GAMIT 的路径，不要照搬这里的代码。然后保存退出，
```

（9）测试安装是否成功，输入以下命令：

```
doy
sh_get_rinex
```

其中，doy 命令回车后显示帮助文档，则说明 GAMIT 安装成功，环境变量也配置成功。

