# RTKLIB用于实时GNSS数据采集手册

**应用场景**

- 静态短基线解算（大坝、桥梁、滑坡等形变监测）

- 动态后处理差分（PPK，无人机遥感或倾斜摄影测量等）

- 实时动态差分（RTK、必须立马出结果）

- 实时精密单点定位（PPP，海洋上）

  **ppp：**
  
  实时ppp：需要IGS/MGEX分析中心播发的**实时卫星轨道产品(sp3)**和**钟差产品(clk)**，在结合**广播星历（o,n）**，实现实时定位。
  
  事后/近似ppp：需要**精密星历（sp3）**和**钟差产品（clk）**，结合其他精密改正信息，实现点位。
  
  **注意（rtkpost）：如果ppp要进行模糊度固定，需要格外提供伪距和载波的硬件延迟偏差改正信息。**

**数据下载**

* 访问该博客：(https://blog.csdn.net/wuwuku123/article/details/106300701)

* 法国一个分析中心（CENS）可对精密星历（也称精密轨道）和钟差下载：ftp://94.23.202.142/PRODUCTS/REAL_TIME/

  1. 武汉大学：ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/ 
  2. 德国GFZ：ftp://ftp.gfz-potsdam.de/GNSS/products/mgex/
  
  <img src="Image/image-20220924164804792.png" alt="image-20220924164804792" style="zoom:50%;" />
  
  <img src="../AppData/Roaming/Typora/typora-user-images/image-20220925102842718.png" alt="image-20220925102842718" style="zoom: 33%;" />

## 一、RTKPOLT.exe

RTKPLOT模块用于使用图像或者图表的方式分析定位解算的水平，我们可以点击rtkplot可执行文件使用该功能，也可以在rtkpost和rtknavi模块中点击plot进入。其界面如下：

<img src="C:\Users\孤泉冷月\AppData\Roaming\Typora\typora-user-images\image-20220923104118266.png" alt="image-20220923104118266" style="zoom: 50%;" />

点击File菜单下的opensolution选项可以加载要显示的解算结果，可以选择rtklib数据处理输出的文件也可以选择NMEA-0183格式的文件。如果文件为空那么会显示接收机地面跟踪轨迹图像。跟踪轨迹的线条、颜色可通过edit选项进行更改。在窗口的下方会显示解算历元的个数、基线长度等信息。

<img src="Image/image-20220923105432640.png" alt="image-20220923105432640" style="zoom:50%;" />

点击file菜单下的open map image选项我们可以打开一个图片作为gnd trk图像的背景。图像可以通过edit菜单进行设置以适应窗口。

​                        <img src="Image/image-20220923105716262.png" alt="image-20220923105716262" style="zoom:50%;" /><img src="Image/image-20220923105953109.png" alt="image-20220923105953109" style="zoom: 50%;" />

菜单栏中的第一个下选框用来选择图像的类型，包含：轨迹跟踪图，接收机坐标在E/N/U方向的分量，接收机速度和加速度在E/N/U方向的分量，在这些图像上，我们滚动鼠标滚轮可以改变坐标系的尺度，还可以选择是否显示跟踪轨迹，坐标系中心及地图的网格线。

​                        <img src="Image/image-20220923110338686.png" alt="image-20220923110338686" style="zoom:50%;" /><img src="Image/image-20220923110514949.png" alt="image-20220923110514949" style="zoom:50%;" />



## 二、RTKCONV.exe

**功能：数据转换**

采集原始的接收机观测数据，通过rtkconv将数据转换为我们通用的**Rinex**格式（RINEX OBS(观测数据)、RINEX
NAV (GNSS导航消息)），便可进行两种模式处理，一是相对定位，即求取两个点的相对位置，二是精密单点定位（ppp）。

**1、主界面**:

<img src="Image/image-20220923154617926.png" alt="image-20220923154617926" style="zoom:67%;" />

**介绍：**

* 标记1：设置时间，区间在采集开始到采集结束这个时间段。（默认）；interval：设置采样率（默认）
* 标记2：表示需要转换的接收机观测数据（Rover流动站）
* 标记3：表示流动站采集的数据类型。rtcm2、rtcm3、novatel oem3,4,6,7、u-blox、trimble rt17、……
* 标记4：表示转换后的数据类型：常用的是（**.obs*或者*.o）,（*.nav），也是定位解算常用的文件。转换输出路径可自定义。

**2、option转换设置界面：**

<img src="Image/image-20220923161701100.png" alt="image-20220923161701100" style="zoom:67%;" />

**介绍：（设置头文件，了解一下O文件格式就清楚了）**

* rinex版本：就是转换后的rinex版本，2.10、2.11、2.12、3.01、3.02、3.03，目前支持到3.04了。

* 中间部分：这部分主要是设置一些基本信息，包括，制作机构，天线类型，版本啥的，不重要。

* Approx pos XYZ：站点近似坐标。

* Antnna Delta H/E/N：天线相位中心偏差

* 各项改正、周跳：是否加入电离层、时间改正、周跳跳等码信息。

* 输出的卫星系统：常用四个

* Exclude satellites：排除一些不需要的卫星号，比如G30，G21、……

* 观测值类型：伪距C、载波L、多普勒D、载噪比S

* GNSS Signals：载波通道

* Signal Mask：信号通道，一般是全选状态，可以根据自己需要选择。如果不知道可以从IGS下载观测文件看一下有哪些信号频道

  <img src="Image/image-20220923211451128.png" alt="image-20220923211451128" style="zoom: 50%;" />

**3、设置完成后，点击convert，开始转换**

<img src="Image/image-20220923211833310.png" alt="image-20220923211833310" style="zoom: 80%;" />

**案例实现**

（1）分别将Physical base station.dat、UAV.bin、Virtual base station.rtcm3三个文件转换为通用的rinex格式。

<img src="Image/image-20220923212154960.png" alt="image-20220923212154960" style="zoom:50%;" />

（2）设置参数，分别转换。

  <img src="Image/image-20220923212621821.png" alt="image-20220923212621821" style="zoom:50%;" /><img src="Image/image-20220923213203128.png" alt="image-20220923213203128" style="zoom: 67%;" />

<img src="Image/image-20220923213308327.png" alt="image-20220923213308327" style="zoom: 50%;" />

（3）查看转换结果

<img src="Image/image-20220923213449401.png" alt="image-20220923213449401" style="zoom:50%;" />



##  三、RTKNAVI.exe

**功能**

实时定位解算（实时导航）。应用程序RTKNAVI，必须输入原始**观测数据（.obs/.o）、导航电文（.nav）**才能够进行实时处理。设置定位模式为Kinematic ,并将基准站和移动站数据输入到RTKNAVI，将会进行整周模糊度解算，并输出高质量的定位结果。

**两大功能：**

1、单点定位：如果做单点定位（ppp），只需要配置Rover和correction改正数即可；

2、RTK定位：如果做RTK（实时动态差分）的话，就需要设置Rover和Base Station

**1、主界面**

​                                       <img src="Image/image-20220923220557673.png" alt="image-20220923220557673" style="zoom: 50%;" />

<img src="Image/image-20220923221042872.png" alt="image-20220923221042872" style="zoom:50%;" />

<img src="Image/image-20220924082851012.png" alt="image-20220924082851012" style="zoom:50%;" />

**介绍：**

* 标记1：切换显示时间（GPST、UTC、LT）

* 标记2，4，5：输入流（后面详解）、输出流、日志流

* 标记3：状态显示

  ​         **-   Gray/灰色**：代表不能用；

  ​        **-   Orange/橙色**：代表等待连接；

  ​        **-   Deep-Green/深绿色**：代表连接、正在运行；

  ​        **-   Light-Green/亮绿色**： 代表数据激活；

  ​       **-   Red/红色**：代表通信错误；

**2、输入流设置**

<img src="Image/image-20220923222240199.png" alt="image-20220923222240199" style="zoom:67%;" />

（1）为每一个“流”进行配置，如果只是**做单点定位（ppp），只需要配置Rover和correction改正数即可；但是如果是做RTK（实时动态差分）的话，就需要设置Rover和Base Station**，。数据流的类型/来源：

* Serial：通过RS232C或USB接入rtknavi；

* TCP Client：通过TCP协议，连接TCP Server；TCP Server将数据送给RTKLIB；

* TCP Server：通过TCP协议，RTKLIB拿TCP Client的数据；

* Ntrip Client：通过NTRIP协议，连接Ntrip Caster;**（需要申请）**

  rover：rtk2go.com    2101  

  correction：  可以在ntrip.gnsslab.cn    2101  (武汉大学的ntrip数据源)中下载具有广播星历的数据，因为ppp没有广播星历无法定位

  

* File：通过记录文件输入RTKLIB；

* FTP：仅支持Correction, 通过FTP下载输入，导入RTKLIB；

* FTTP：仅支持Correction, 通过FTTP下载输入，导入RTKLIB；

（2）流类型中的Opt：ʺTCP Clientʺ or ʺTCP Serverʺ

<img src="Image/image-20220923222905660.png" alt="image-20220923222905660" style="zoom:67%;" />

（3）流类型中的Opt：ʺNTRIP Clientʺ

需要配置：NTRIP Caster Host、Port、 Mount‐point、User‐ID、Password；配置好后点击“Browse”可以浏览查询结

​               <img src="Image/image-20220923223254255.png" alt="image-20220923223254255" style="zoom: 50%;" />  <img src="Image/image-20220923223513677.png" alt="image-20220923223513677" style="zoom: 50%;" />

（4）如果基准站（Base Station）为以下服务类型：“serial”、"Tcp Client"、"Tcp Server"、"Ntrip Client"；需要选择“Transmit NMEA GPGGA to Base Station”。有两种发送移动站坐标到基准站的方式：

* 1、如果知道当前移动站的坐标，选择“Latitude/Longitude”，手动输入坐标（经纬高）

* 2、选择“Single Solution”，将移动站坐标传送到基准站，不要输入。

注意：负号表示南纬、西经。

<img src="Image/image-20220923224023357.png" alt="image-20220923224023357" style="zoom:50%;" />

**3、options界面**（rtkpost和rtknavi的options是一样的）

<img src="Image/image-20220923224619905.png" alt="image-20220923224619905" style="zoom: 67%;" />

各项参数介绍：

**Setting1**

<img src="Image/image-20220923232346231.png" alt="image-20220923232346231" style="zoom: 67%;" />

| 参数                                                         | 含义                                                         |
| :----------------------------------------------------------- | ------------------------------------------------------------ |
| Positioning Mode（定位模式）                                 | 主要分为两种定位模式，一种是相对定位，需要两个测站的数据；一种是精密单点定位PPP。  ①Single（伪距单点定位）  ②DGPS/DGNSS（伪距差分/伪距相对定位）  ③Kinematic（基于载波的动态定位）  ④Static（基于载波的静态定位）  ⑤Moving-Base（移动基线）  ⑥Fixed（约束坐标）  ⑦PPP Kinematic/Static/Fixed（精密单点定位动态/静态/定位） |
| Frequencies（频率）                                          | 单频、双频、三频                                             |
| Filter Type（滤波类型）                                      | ①Forward（从前往后处理：前向滤波）  ②Backward（从后往前处理）  ③Combined（先从前往后，再从后往前处理）  ④Combined-no phase reset（无相位重置）   “Backward”从后往前处理可以保证起始时间阶段有高精度的解算结果，  “Combined”先从前往后，再从后往前，再按照一定运算规则取终值。 |
| Elevation Mask/  SNR Mask  <br />（卫星截止高度角）/（信噪比模板） | 一般在卫星数多（>10）的情况下选15°，因为低高度角的卫星，质量不能保证，会影响定位解算精度。信噪比模板一般不做设置。 |
| Rec Dynamics（接收机动力学模型）                             | 接收机动态点“ON”，他会估计一个速度和加速度参数，如果是“OFF”，就只会估算静态的坐标参数。 |
| Earth Tides  Correction(地球潮汐改正)                        | ①OFF（不应用）  ②Solid（固体潮汐改正）  ③Solid/OTL（固体潮汐改正、海潮荷载、极潮修正）地球潮汐校正，在处理PPP的时候需要设置。 |
| Ionosphere  Correction（电离层改正）                         | ①OFF（不应用）  ②Broadcast（广播电离层模型）  ③SBAS（SBAS电离层模型）  ④Iono-Free LC（无电离层线性组合，具有双频（GPS/GLONASS/QZSS的L1-L2或伽利略的L1-L5测量用于电离层校正）  ⑤Estimate TEC（电离层参数估计）  ⑥IONEX TEC（使用IONEX TEC网格数据）  ⑦QZSS Broadcast（应用QZSS提供的广播电离层模型） |
| Troposphere  Correction（对流层改正）                        | ①OFF（不应用）  ②Saastamoinen（模型）  ③SBAS（应用SBAS对流层模型）  ③Estimate ZTD将ZTD（天顶总延迟）参数估计为EKF状态  ④Estimate ZTD+Grad将ZTD和水平梯度参数估计为EKF状态 |
| Satellite  Ephemeris/Clock（卫星星历/时钟）                  | ①Broadcast（广播星历）  ②Precise（精密星历）  ③Broadcast+SBAS（具有SBAS长期快速校正的广播星历）  ④Broadcast+SSR APC（带RTCM SSR校正的广播星历（天线相位中心值））  ⑤Broadcast+SSR CoM（带RTCM SSR校正的广播星历（卫星质心值）） |
| Sat PCV（卫星天线PCV-相位中心变化模型）                      | Rec PCV：设置是否使用接收器天线PCV型号  PhWU：设置是否应用PPP模式的相位结束校正  Rej Ed：设置是否排除eclipse中的GPS  Block IIA卫星。由于偏航姿态的不可预测行为，日蚀Block IIA卫星通常会降低PPP解决方案的性能。  RAIM FDE：设置是否启用RAIM（接收器自主完整性监视）FDE（故障检测和排除）功能 |

**Setting2**

<img src="Image/image-20220923232407239.png" alt="image-20220923232407239" style="zoom:67%;" />

**注意：如果ppp要进行模糊度固定，需要格外提供伪距和载波的硬件延迟偏差改正信息。**

|                参数                 | 含义                                                         |
| :---------------------------------: | :----------------------------------------------------------- |
| Integer Ambiguity Res (GPS/GLO/BDS) | 整周模糊度(GPS/GLO/BDS)<br /<br />OFF:不进行模糊度固定；<br />instantaneo：各个历元模糊度重新固定；<br />contious：通过前前面的历元的模糊度固定，提高后续历元的模糊度固定率；<br />Fix and Hold：模糊度固定之后，在不发生周跳的情况下，模糊度不变； |
|     Min Ratio to Fix Ambiguity      | 最小比固定模糊度                                             |
| Min Confidence / Max FCB to Fix Amb | 最小置信度/最大FCB到Fix Amb                                  |
|  Min Lock / Elevation 0 to Fix Amb  | 最小锁定/提升0到Fix Amb                                      |
| Min Fix / Elevation (0) to Hold Amb | 最小修正/海拔(0)保持Amb                                      |
| Outage to Reset Amb/Slip Thres (m)  | 中断以重置Amb/SILE(M)                                        |
| Max Age of Diff (s) / Sync Solution | Dff(S)/同步解的最大年龄                                      |
| Reject Threshold of GDOP/Innov (m)  | GDOP/Innov(M)的拒绝阈值                                      |
|  Max # of AR Iter/# of Filter Iter  | 最大AR Iter/滤波器Iter#                                      |

**Output**

<img src="../AppData/Roaming/Typora/typora-user-images/image-20220924175922697.png" alt="image-20220924175922697" style="zoom: 67%;" />

|                     参数                      | 含义                                                         |
| :-------------------------------------------: | :----------------------------------------------------------- |
|                Solution Format                | 输出方案格式<br />基线解算时：选择E/N/U-Baseline<br />ppp解算时：可以选择输出地心地固坐标系下的坐标X/Y/Z-ECEF<br />或者lat/lon/height或者NMEAO 183 |
|   Output Header / Proc. Options / Velodity    | 是否输出头文件/proc选项/速度                                 |
|          Time Format/ # of Decimals           | 输出时间/小数的#                                             |
|  Latitude Longitude Format / Field Separator  | 纬度经度格式/字段分隔器                                      |
| Output Single if Sol Outage / Max Sol Std (m) | 输出单次Sol中断/最大SOL STD(M)                               |
|                Datum / Height                 | 基准/高度                                                    |
|                  Geoid Model                  | 大地水准面模型                                               |
|           Solution for Static Mode            | 静态模式的解决方案                                           |
|      NMEA Interval (s) RMC/GGA, GSA/GSV       | NMEA间隔RMC/GGA，GSA/GSV                                     |
|     Output Solution Status / Debug Trace      | 输出解决方案状态（**可以选择输出残差residuals，方便查找问题**）/调试跟踪level |

**Positions**

<img src="Image/image-20220923232424889.png" alt="image-20220923232424889" style="zoom:67%;" />

|     参数     | 含义                                                         |
| :----------: | :----------------------------------------------------------- |
|    Rover     | 如果流动站天线固定，则设置流动站天线的位置                   |
| Antenna Type | 选择移动站天线的类型。如果要选择天线类型，需要在（file）中设置接收器天线PCV文件路径。如果使用了（*），表示天线类型和天线增量由RINEX OBS报头（RTKPOST）或RTCM天线信息（RTKNAVI）的天线信息识别。 |
| Delta-E/N/U  | 将流动站天线的增量位置设置为参考标记（m）的ARP（天线参考点）位置的E\/N\/U偏移。 |
| Base Station | **做相对定位时比较重要的一个是基准站的坐标如何得到（可以直接输入、或者从文件获取）（一般输入星号*自动获取）**<br />设置基站天线的位置纬度/经度/高度（deg\/m），纬度\经度\高度（度数）/米；纬度\经线\高度（dms/m）；纬度\经纬度\高度度数\分\秒/米；X\/Y\/Z‐ECEF（m）：ECEF框架中的X\/Y\/Z分量；RTCM站位置：使用RTCM消息中包含的天线位置＊‐单点平均值‐位置；使用单点解的平均值‐从位置文件获取：使用位置文件中的位置。通过使用漫游者观测数据文件路径的头4个字符ID搜索站点。-RINEX标题位置：使用应用程序 |

**File**

<img src="Image/image-20220923232759893.png" alt="image-20220923232759893" style="zoom:67%;" />

| 含义                                                         |
| ------------------------------------------------------------ |
| 1 如果使用精确星历表或SSR校正，请输入卫星天线PCV（相位中心变化）校正的ANTEX天线参数文件路径。 |
| 2 如果应用接收机天线相位中心偏移 和 PCVPCVPCV校正，输入ANTEX或 NGS 类型的天线文件。 |
| 3 如果选择外部模型作为大地水准面模型，则输入大地水准面数据文件的文件路径。 |
| 4 输入PPP的DCB硬件延迟偏差校正文件路径，IGS 为**BIA**格式版本 |
| 5 输入EOP地球自转文件的文件路径。EOP数据文件的格式应为IGS **erp**格式版本 |
| 6 输入OTL潮汐文件的文件路径。OTL系数文件的格式为BLQ格式      |
| 7 选择电离层数据文件                                         |

**BCD（BIA）,EPH,ERP,clk下载：**http://ftp.aiub.unibe.ch/CODE/

**4、案例实现**

（一）、RTKnavi实现**伪距单点定位（single）**

配置：流动站，基准站

<img src="../AppData/Roaming/Typora/typora-user-images/image-20220925135953345.png" alt="image-20220925135953345" style="zoom:50%;" />

https://www.rtklib.com/rtklib_tutorial.htm



## 四、RTKPOST.exe

**功能**

RTKPOST是RTKLIB中比较关键的软件，属于**后处理模块**。功能一应俱全，基本能满足所有GNSS数据处理的应用要求，缺点是精度可能不太可靠（与其他高精度科研软件相比）；能够处理RINEX 2.10、2.11、2.12、3.00、3.01、3.02、3.03、3.04观测数据和导航电文(GPS, GLONASS、Galileo、QZSS、BeiDou 、 SBAS),并且包含多种定位方式：Single‐point、 DGPS/DGNSS、 Kinematic、 Static、Moving-Base、Fixed、PPP‐Kinematic 、 PPP‐Static、PPP Fixed（模糊度固定定位）。

**ppp：**

ppp精密单点定位不需要基准站信息。

* 实时ppp：需要IGS/MGEX分析中心播发的**实时卫星轨道产品**和**钟差产品**，在结合**广播星历**，实现实时定位。

* 事后/近似ppp：需要**精密星历（sp3）**和**钟差产品（clk）**，结合其他精密改正信息，实现点位。

注意：ppp要进行模糊度固定，需要格外提供伪距和载波的硬件延迟偏差（DCB Data File）改正信息。（没有的话就采用浮点解）

**ppp数据下载**

法国一个分析中心（CENS）可对精密星历（也称精密轨道）和钟差下载：ftp://94.23.202.142/PRODUCTS/REAL_TIME/

1. 武汉大学：ftp://igs.gnsswhu.cn/pub/gnss/products/mgex/ 
2. 德国GFZ：ftp://ftp.gfz-potsdam.de/GNSS/products/mgex/

**1、主界面**

<img src="Image/image-20220924085706739.png" alt="image-20220924085706739" style="zoom:67%;" />

**介绍：**

* 1： 表示你处理的时段，O、N文件中会有写，一般不用管。
* 2： 表示采样率。
* 4、5、6、8：5表示处理的移动站O文件（观测值文件）；点击 4、6 中“圆盘”会打开RTLPLOT.exe打开观测值文件查看卫星的状态。点击 4 、6、8中的“文本框”会显示观测文件的信息。如下图所示：**RTLPLOT.exe**后面做详细的介绍

​                          <img src="Image/image-20220924090912394.png" alt="image-20220924090912394" style="zoom:50%;" /><img src="Image/image-20220924091711281.png" alt="image-20220924091711281" style="zoom: 50%;" />

*  7 基准站的观测值文件
* 9 、10、11、12：一般为广播星历（N文件）、精密星历（sp3）、精密钟差文件（clk）
* 13 自定义结果文件输出路径。结果文件有三个，最主要的是后缀为.pos的文件，可以用“RTKPLOT”打开成图，也可以用记事本打开，看文字内容。
* 14 表示你生成的结果文件的名字。一般软件默认是移动站O文件的前缀。
* 15 两个方框文本，点了以后看其他两种结果文件的文本内容。
* 16 表示“RTKPLOT”的快捷按钮，当你运算结束后，点16，就会自动用“RTKPLOT”打开你的结果文件“.pos”
* 17 表示“绿底记事本”的快捷按钮，当你运算结束后，点17，就会自动用“绿底记事本”打开你的结果文件“.pos”
* 18 表示运用谷歌地球，在谷歌地球上显示你运算结束后的点，点的位置和过程中的漂移，没试过。
* 19 为“OPTIONS”，最重要的设置，里面包含了许多的参数设置，也是最影响解算结果的设置，**在上一节RTKNAVI.exe中已经介绍了**。
* 20 表示开始解算。
* 21 表示退出。

**2、案例实现（用2.4.2版本的RTKLIB）**：

**（一）、先实现kinematic动态定位**

（1）加载流动站的观测值文件（O\N），基准站的观测值文件（O\N）,流动站的导航电文（nav）。

（2）配置参数，如下所示；定位模式：动态定位；频率选择双频的；滤波类型：从前向后滤波计算；卫星系统：常用四大卫星系统；其他参数根据需要自行配置。**不同的参数配置定位精度可能会不一样，多尝试**。

<img src="Image/image-20220924094134387.png" alt="image-20220924094134387" style="zoom:50%;" />

（3）配置完成后，点击“Execute”解算。Q的大小表示解算结果的好坏，1表是很好，一般大于5就认为错误。橙色的进度条表示解算的进度。解算完成后点击“Plot”和“View”均可查看结算的pos文件信息。

<img src="Image/image-20220924093925505.png" alt="image-20220924093925505" style="zoom: 50%;" />

（4）查看pos文件。

<img src="Image/image-20220924095734479.png" alt="image-20220924095734479" style="zoom: 50%;" />

**（二）、实现ppp kinematic定位**

ppp必须提供天线文件

https://blog.csdn.net/weixin_44986362/article/details/107715558

https://blog.csdn.net/unbiliverbal/article/details/123639263

**（三）、实现精密单点定位**

精密星历.sp3文件读取存在问题：

<img src="Image/image-20220927091456677.png" alt="image-20220927091456677" style="zoom:67%;" />

改正：

<img src="Image/image-20220927091553569.png" alt="image-20220927091553569" style="zoom:67%;" />

## 五、RTKPOLT.exe

**功能**

RTKPLOT模块用于使用图像或者图表的方式分析定位解算的水平。我们可以点击rtkplot可执行文件使用该功能，也可以在rtkpost和rtknavi模块中点击plot进入。其界面如下：

该博客介绍很详细，欢迎去查看：http://blog.sciencenet.cn/blog-3386358-1137198.html

**1、界面**

<img src="Image/image-20220924105652015.png" alt="image-20220924105652015" style="zoom: 50%;" />

点击File菜单下的opensolution选项可以加载要显示的解算结果，可以选择rtklib数据处理输出的文件也可以选择NMEA-0183格式的文件。如果文件为空那么会显示接收机地面跟踪轨迹图像。跟踪轨迹的线条、颜色可通过edit选项进行更改。在窗口的下方会显示解算历元的个数、基线长度等信息。

<img src="Image/image-20220924105723881.png" alt="image-20220924105723881" style="zoom: 50%;" />

点击file菜单下的open map image选项我们可以打开一个图片作为gnd trk图像的背景。图像可以通过edit菜单进行设置以适应窗口。

<img src="Image/image-20220924105810530.png" alt="image-20220924105810530" style="zoom:50%;" />



菜单栏中的第一个下选框用来选择图像的类型，包含：轨迹跟踪图，接收机坐标在E/N/U方向的分量，接收机速度和加速度在E/N/U方向的分量，在这些图像上，我们滚动鼠标滚轮可以改变坐标系的尺度，还可以选择是否显示跟踪轨迹，坐标系中心及地图的网格线。

**轨迹跟踪图**

<img src="Image/image-20220924105856967.png" alt="image-20220924105856967" style="zoom:50%;" />

**接收机坐标在E/N/U方向的分量，接收机速度和加速度在E/N/U方向的分量**

<img src="Image/image-20220924105928700.png" alt="image-20220924105928700" style="zoom:50%;" />



并且我们可以选择Nsat图像类型用于显示可见的卫星、通过研究差分改正信息的讯龄，从而分析了定位误差的时间相关性、模糊度检验的ratio因子。如果我们在定位解算时选择输出文件中输出定位坐标残差，我们还可以选择Residuals图来查看随历元变化的坐标三个分量的残差值。并且我们可以选择显示的卫星频点，选择单个卫星还是全部卫星。在残差图中红色的线代表了周跳。还可以显示伪距残差、载波相位残差、截止高度角和信号强度的变化。

**残差图**

<img src="Image/image-20220924110038955.png" alt="image-20220924110038955" style="zoom:50%;" />

本模块还支持引入google map和google earth的图像，可通过view菜单下的选项来选择。并且我们可以利用google map和google earth工具对图像进行修改**（但是目前国内无法使用）**。

若想显示多幅图像我们可以选择file下的open solution2选项来产生另一幅图像。并可以点击图像窗口中的1、2来改变当前显示的图像，我们可以通过edit下的Time Span/Interval选项来选择显示需要的图像时间段及点的采样间隔。并且可以通过Solution Source选项查看这些样点的信息日志。





除了上述可通过rtkplo查看定位解算的分析结果之外，我们还可以用此工具查看原始的**观测文件**。可通过File下的Open Obs Data打开RINEX observation和navigation信息文件。打开原始观测和导航数据我们可以选择skyplot图和visible satellites图来查看可视卫星变化情况，选择DOP/NSat plot、SNR/Multipath/Elevation plot (SNR/MP/EL) 和SNR/Multipath ‐ EL plot (SNR/MP‐EL).图，elevation图来查看相应的信噪比和截止高度角变化图。

<img src="Image/image-20220924111349847.png" alt="image-20220924111349847" style="zoom:67%;" />

如果要查看相应的原始观测文件我们可以选择ʺEditʺ 下的ʺObs Data Sourceʺ或 ʺObs Data QC”。

<img src="Image/image-20220924111438804.png" alt="image-20220924111438804" style="zoom: 67%;" />

我们可以预测GNSS卫星的可见性，步骤为在ʺOptionsʺ下的选择ʺReceiver Positionʺ to ʺLat/Lon/Hgtʺ. 接着执行ʺFileʺ ‐ ʺVisibilityAnalysis...ʺ, 这样我们就可以进行分析时间的选择 ʺTime Span/Intervalʺ 。

<img src="Image/image-20220924111653740.png" alt="image-20220924111653740" style="zoom:80%;" />

## 六、STRSVR.exe

**功能**

STRSVR是一款支持串口、FTP 、 HTTP、 TCP客户端/服务器模式、文件、NTRIP协议的网络互传辅助工具。STRSVR模块功能强大全面，简单易用，使用后可以帮助用户更轻松便捷的进行服务器互传操作。软件用于设置远程服务器并在远程服务器上进行转发，数据转发的操作非常方便。

**1、界面**

<img src="Image/image-20220924112854050.png" alt="image-20220924112854050" style="zoom:67%;" />

| 类型         | 简介                                                         |
| ------------ | ------------------------------------------------------------ |
| Serial       | 从接收机通过硬件传输至网络输出原始数据                       |
| TCP Client   | 主动角色，发送连接请求，等待服务器的响应                     |
| TCP Server   | 等待来自客户端的连接请求，处理请求并回传结果                 |
| Ntrip Client | 登录Ntrip Caster获取RTCM数据                                 |
| UDP Server   | 与TCP协议一样，它只支持UDP的服务框架，同步多进程模型传输数据 |
| File         | 以文件形式输入数据                                           |

**2、案例实现**

（1）打开STRSVR.exe，在Input栏中可选择TCP Cient，并在Opt选项中进行配置信息。

<img src="Image/image-20220924113828824.png" alt="image-20220924113828824" style="zoom:67%;" />

（2）Server Address输入服务器地址，Port输入端口。

（3）如下图，可以在远程服务器中自行查看各监测站的数据收发情况

<img src="Image/image-20220924114139382.png" alt="image-20220924114139382" style="zoom: 50%;" />

当Output为橙色时，代表未接入该端口数据流，当Output为绿色时，则成功接入数据。（均可在服务器上的STRSVR查看）

<img src="Image/image-20220924114216625.png" alt="image-20220924114216625" style="zoom:50%;" />



（4）设置完成即可start进行实时接收数据。

此时状态为TCP 协议接收数据，以文件的形式存储到本地

<img src="Image/image-20220924114720082.png" alt="image-20220924114720082" style="zoom: 67%;" />



（5）数据存储

* output->type选择File，点开Opt

* Opt中swap intv表示可选的时间间隔，单位是小时，比如选择每24h存储一个文件，即将测站实时流数据每24小时存成一个文件

  <img src="Image/image-20220924115027803.png" alt="image-20220924115027803" style="zoom:67%;" />

* 点开Output File path后面的问号，弹出下面的窗体，表示在文件命名中可以替代的关键字，比如我将文件名命名为%Y%m%d%hstation1，则输出的文件名自动生成为2021081300station1。当再过24小时之后，会生成新的文件名为2021081400station1。

<img src="Image/image-20220924115114280.png" alt="image-20220924115114280" style="zoom: 50%;" />

**注意**

1）时间是以UTC时间表示的，和北京时间差8小时。

2）每次储存起点从0时起，第一个文件不从0时开始的话就存到当天23:59:59，再从0时存储。

* 下图为实时数据接收并输出界面，绿色且有字节变化，即代表正常运行，若Input为绿色但无数据传输，原因是地址或端口输入错误，检查重新start即可。

  <img src="Image/image-20220924115300699.png" alt="image-20220924115300699" style="zoom: 50%;" />

* 在实时接收数据过程中，可点击左下方小框，可监视数据流的信息状态

​                                           <img src="Image/image-20220924115545612.png" alt="image-20220924115545612" style="zoom:50%;" /><img src="Image/image-20220924115554712.png" alt="image-20220924115554712" style="zoom:50%;" />







## 七、RTKGET.exe

**功能**

GNSS数据下载模块，对于**PPP定位**，需要在IGS网站下载**精密星历、钟差**等产品；另一方面，你也可以在网络上下载存储在网络上的，关于CORS站的观测/导航数据等。利用此模块可直接进行需要下载。

**1、界面**

<img src="Image/image-20220924115815130.png" alt="image-20220924115815130" style="zoom:67%;" />

**2、案例实现**（比如选择IGS数据中心下载AMC2站点的观测数据（obs））

（1）设置好所需的时间段

（2）点击Options进行设置，将URL_LIST.txt 加载进来

<img src="Image/image-20220924120526093.png" alt="image-20220924120526093" style="zoom:50%;" />

（3）输入站点AMC2，我们可以选择想要下载的的数据类型（obs）：

* 主要用到了OBS(观察值文件，包含了伪距和载波；NAV(导航电文数据)、EPH(精密轨道)、ATX(天线文件)、CLK(精密钟差),

<img src="Image/image-20220924120612003.png" alt="image-20220924120612003" style="zoom:50%;" />

（4）然后Download，就可以下载成功，不过我们一般不使用这个方法。主要是下载速度慢，一个是每次选择都比较麻烦；我们可以使用FTP进行下载。

<img src="Image/image-20220924121130215.png" alt="image-20220924121130215" style="zoom:50%;" />

<img src="Image/image-20220924121535632.png" alt="image-20220924121535632" style="zoom:50%;" />

**注意：**

GPST:GPS时间
UTC:美国时间
GPS WEEK； GPS开始以后经过了多少周
GPS Time：在这一周的多少秒
day of year：这一年的第几天
Day of week: 这一周的第几天
Time of day： 这一天的第几秒
leap seconds：跳秒

![image-20220924121219718](Image/image-20220924121219718.png)









<img src="Image/image-20220927113754427.png" alt="image-20220927113754427" style="zoom:67%;" />

国家科学数据中心：[国家空间科学数据中心(National Space Science Data Center) (nssdc.ac.cn)](https://www.nssdc.ac.cn/mhsy/html/major2.html)



# 数据下载网址大全

连接1：https://blog.csdn.net/rstaotao/article/details/96274662

连接2：https://blog.csdn.net/qq_35099602/article/details/108183607



关于观测站数据下载，网上有很多各种各样的链接，但其中部分链接已失效。
现重新整理，以期能够快速获得所需资料，减少在寻找资料上的时间耗费。

一、一般观测文件（o、n、sp3）
武汉大学IGS中心
http://www.igs.gnsswhu.cn/index.php/Home/DataProduct/igs.html
IGS 观测数据：
ftp://cddis.gsfc.nasa.gov/pub/gps/data/daily （包括 m文件）
广播星历(brdc/brdm)：
ftp://cddis.gsfc.nasa.gov/pub/gps/data/daily/YYYY/brdc
ftp://epncb.oma.be/pub/obs/BRDC
IGS 精密轨道/钟差:
ftp://cddis.gsfc.nasa.gov/pub/gps/products
ftp://garner.ucsd.edu/pub/products/ （按周）
ftp://igs.ign.fr/pub/igs/products
站坐标文件(snx):
ftp://igs.ign.fr/pub/igs/products
ftp://cddis.gsfc.nasa.gov/pub/gps/products
天线改正文件(ATX文件)下载
www.igs.org/pub/station/general
ftp://ftp.igs.org/pub/station/general

二、MGEX/北斗观测数据文件（RINEX3.x格式）
北斗卫星发射时间、原子钟相关信息
http://mgex.igs.org/IGS_MGEX_Status_BDS.php#Satellites
https://en.wikipedia.org/wiki/List_of_BeiDou_satellites
北斗星座状态
http://www.csno-tarc.cn/system/constellation
国际GNSS监测评估系统IGMAS
http://www.igmas.org/Product/Search/search/
IGS MGEX项目简介及说明：
http://mgex.igs.org/IGS_MGEX_Data.php
武汉大学IGS数据中心（最近的数据找不到）：
http://www.igs.gnsswhu.cn/index.php/Home/DataProduct/mgex.html

可以接收北斗三号新信号的MGEX观测站
POTS SGOC SUTM ULAB URUM WIND WUH2

MGEX 观测数据：
BKG网址 ftp://igs.bkg.bund.de/IGS/obs/2020/
ING网址（不稳定） ftp://igs.ign.fr/pub/igs/data/campaign/mgex/daily/rinex3/2020/
CDDIS网址（不是RINEX3.x格式） ftp://ftp.cddis.eosdis.nasa.gov/pub/gnss/data/daily/2020/
ftp://cddis.gsfc.nasa.gov/pub/gps/data/daily
ftp://cddis.gsfc.nasa.gov/pub/gps/data/campaign/mgex/daily/rinex3/
IGS/MGEX 1s观测数据 ftp://cddis.gsfc.nasa.gov/pub/gps/data/highrate
MGEX广播星历：
https://igs.bkg.bund.de/root_ftp/IGS/BRDC/2020/
ftp://cddis.gsfc.nasa.gov/pub/gps/data/campaign/mgex/daily/rinex3/2020/brdm
**MGEX 精密轨道/钟差:**MGEX站SP3标准格式（按周进行选择）
（1）CDDIS机构提供：
ftp://cddis.gsfc.nasa.gov/pub/gps/products/mgex/
CODFIN、GFZRAP、GRGFIN、JAXFIN、
SHARAP、WUMFIN、WUMULA、wumsp3
（2）IGN机构提供： ftp://igs.ign.fr/pub/igs/products/mgex
CODFIN、GFZRAP、GRGFIN、JAXFIN、
SHARAP、WUMFIN、WUMULA、wumsp3
包含精密星历星钟ERP产品
（3）北三星历GFZ GBM
ftp://ftp.gfz-potsdam.de/pub/GNSS/products/mgex
包含GBMRAP、gbmsp3
【新发现】老格式gbm22222.sp3这种 只到C16
新RINEX3.04格式：
GBM已经到C60
COD只到C16
WUM只到C36
GRG和JAX没有C

三、相关产品Products
一、 DCB文件:
GNSS差分码偏差（DCB，Differential Code Bias）是由不同类型的GNSS信号在卫星和接收机不同通道产生的时间延迟（硬件延迟/码偏差）差异，按照频率相同或者不同又可以细分为频内偏差（例如GPS P1-C1）和频间偏差（例如GPS P1-P2）。
DCB文件主要提供机构：CODE（欧洲定轨中心）、DLR（德国宇航中心）、CAS（中科院测地所）

GPS DCB CODE P1-C1 P1-P2 P2-C2
http://ftp.aiub.unibe.ch/CODE/YYYY/
测绘小兵-关于码间偏差（DCB）

MGEX DCB下载地址（能同时下载ERP、ION、SNX、CLK等文件）
http://ftp.aiub.unibe.ch/CODE/
MGEX DCB DLR CAS *.BSX.Z
ftp://cddis.gsfc.nasa.gov/pub/gps/products/mgex/dcb/YYYY/
ftp://igs.ign.fr/pub/igs/products/mgex/dcb/YYYY/
ftp://cddis.nasa.gov/gnss/products/bias/

GPS OSB COD*****. BIA. Z
http://ftp.aiub.unibe.ch/CODE/YYYY/
MGEX OSB CODOSB. BIA. gz
ftp://cddis.gsfc.nasa.gov/pub/gps/products/mgex/YYYY
ftp://igs.ign.fr/pub/igs/products/mgex/YYYY/
CASOSB. BIA. gz
ftp://cddis.gsfc.nasa.gov/pub/gps/products/mgex/dcb/YYYY/
ftp://igs.ign.fr/pub/igs/products/mgex/dcb/YYYY/ IGS DCB文件
MGEX 下载ERP、ION、SNX、CLK等文件
http://ftp.aiub.unibe.ch/CODE/
CODE分析中心使用的各种信息文件（配合BERNESE）:
ftp://ftp.unibe.ch/BSWUSER52/ 包含C04.EOP,DCB产品，卫星PCO PCV 及各种接收机天线相位信息等。
二、最终对流层产品zpd文件：
ftp://cddis.gsfc.nasa.gov/pub/gps/products/troposphere/zpd/
m文件参数
PR : Pressure (mbar)
TD : Dry temperature (deg Celsius)
HR : Relative Humidity (percent)
ftp://cddis.gsfc.nasa.gov/gps/products/trop_zpd/2020

**BLQ下载**
BLQ(只是核心站点的海潮改正，要真正需要的海潮文件：
BLQ文件获取（http://froste.oso.chalmers.se/loading//）
http://ftp.aiub.unibe.ch/BSWUSER52/STA/FES2004.BLQ

附：GNSS产品下载地址（2020-08-25）

5.SOPAC网站：可以下载观测数据 测站坐标及速度等，非常实用。http://sopac.ucsd.edu/sector.shtml
6.IGS产品精度分析：http://beta.igs.org/products/data
8.IGG的多系统DCB产：ftp://cddis.gsfc.nasa.gov/pub/gps/products/mgex/dcb/　
（测地所提交至IGS的多系统DCB产品的文件名为：CAS0MGXRAP_0000_01D_01D_DCB.BSX）
9.地球自转参数EOP文件 https://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html
10.ATX天线相位中心文件：http://reason.scign.org/input/processing/gamit/tables/ svnav.dat（卫星PCO出厂）

IGS 各家分析中心全称
COD Centre for Orbit Determination in Europe, Bern, Switzerland欧洲定轨中心
ESA European Space Agency, Darmstadt, Germany
GFZ Geoforschungszentrum, Potsdam, Germany
GRG Groupe de Recherche en Geodesie Spatiale, Toulouse, France
JPL Jet Propulsion Labs, Pasadena, California, U.S.A.
MIT Massachusetts Institute of Technology, Cambridge, Mass., U.S.A.
NGS National Geodetic Survey, Silver Springs, Maryland, U.S.A.
NRC Natural Resources Canada, Ottawa, Ontario, Canada
SIO Scripps Institute of Oceanography, San Diego, California, U.S.A.
WHU 武汉大学

