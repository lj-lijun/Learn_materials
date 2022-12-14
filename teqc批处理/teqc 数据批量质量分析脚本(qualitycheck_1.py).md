# GNSS 数据批量质量分析脚本(qualitycheck_1.py)

来源网址：[GNSS 数据批量质量分析脚本](https://www.gnss.help/2017/02/03/pinot-qualitycheck/)



在对 GNSS 观测数据进行处理之前，我们一般都需要进行观测质量分析。其中 TEQC、GFZRNX 等都是常用的质量检查工具。但这些程序处理大量的数据时皆显得略有不便。并且，很多时候我们只需记录一些最关键的质量分析指标。

qualitycheck.py 脚本是一个批量进行 RINEX 数据质量分析的脚本，通过调用 TEQC 程序对输入数据处理，输出观测时长、信噪比、多路径效应、周跳等质量检查成果。



## 运行环境

由于本程序的质量分析操作依赖于 TEQC 程序，但是因不同版本的 TEQC 的输出信息格式有略微不同，本脚本保证在使用 2016Nov7 及以后版本的 TEQC 时测试通过。

需注意的是：对于 Windows 10、Windows 7 等操作系统，只需将 TEQC 程序放入系统能搜索到的路径下，即在任意目录中启动命令提示符执行 teqc 命令能显示 TEQC 程序的提示信息；但对于 Windows XP 或 Windows server 2008 等操作系统，需保证运行脚本的文件夹内有 TEQC 程序，否则可能出现 “’teqc’ 不是内部或外部命令，也不是可运行的程序或批处理文件。” 的错误。

## 参数说明

该脚本可接受的参数有：

```
$ python qualitycheck.py <file> [<file> ...] -out <format> [-r] [-v] [-h]
```

参数释义：

- `<file>`：要处理的文件名，可由通配符指定；
- `-out <format>`：信息输出的方式，该参数有两个选项：列表或表格（默认）。列表输出方式以 `list` 或 `l` 指定，表格输出方式以 `table` 或 `t` 指定；
- `-r`、`--recursive`：指定用 “**/” 的通配符前缀表示递归搜索子文件夹的内容，不加该参数默认为不递归；
- `-v`、`--version`：显示版本信息；
- `-h`、`--help`：显示帮助。

## 输出示例

前文已经提到，该脚本的输出信息有两种形式：列表和表格，采用 `-out` 参数指定。该参数为 `l`、`list` 或未指定时为列表；为 `t` 或 `table` 时为表格形式。

### 列表形式

一个列表形式的输出消息如下：

```
test\2016\001\16o\bjfs0010.16o quality marks:
date: 2016-01-01
start: 00:00:00.000
end: 23:59:30.000
hours: 23.99
SN1: 5.22
SN2: 7.21
MP1: 0.42
MP2: 0.31
CSR: 0.20
```

### 表格形式

表格形式的输出信息方便使用 Excel 或 Pandas 等程序做进一步处理。一个表格形式的输出消息如下：

```
    file         date        start          end       hours   SN1   SN2   MP1   MP2   CSR
bjfs0010.16o  2016-01-01  00:00:00.000  23:59:30.000  23.99  5.22  7.21  0.42  0.31  0.20
bjfs0200.16o  2016-01-20  00:00:00.000  23:59:30.000  23.99  5.42  7.25  0.41  0.35  0.21
```

## 使用示例

处理 rinex/ 文件夹中观测年为 2016 年的观测文件，将最终成果以表格形式输出到屏幕：

```
$ python qualitycheck.py rinex/*.16[oO] -out table
```

处理 rinex/ 内 001、009 两个子文件夹内的观测文件，将最终成果以表格形式输出到当前路径下的 result.txt 文件：

```
$ python qualitycheck.py rinex/00[19]/*[oO] -out t > result.txt
```

处理 rinex/ 文件夹及其子文件夹中观测年为 2016 年，年积日为 042 至 045 的 RINEX O-文件，将最终成果以列表形式输出到当前路径下的 result.txt 文件：

```
$ python qualitycheck.py rinex/**/*04[2-5]0.16[oO] -out list -r > result.txt
```