> 如果觉得本文对你有帮助的话，请点个赞再走哦！

> 今年的华为软件精英挑战赛终于结束了（大佬们去深圳决赛了），当时初赛赛区第5，进了复赛也没能冲进前4（前4进决赛），也算有些遗憾吧。本文梳理下比赛思路，分享下比赛代码。
# 赛题简介
此次比赛题目是关于利用虚拟机历史申请使用记录来预测未来一周虚拟机的申请情况，并对预测的虚拟机合理分配到服务器上，详见[官网](http://codecraft.devcloud.huaweicloud.com/home/detail)。开始看到这个题目，以为用机器学习、时间序列来做，后来发现自己太天真。

# 比赛思路
## 预测模型

预测模型试过很多，但很多用心写的代码，不如取平均值。试过的模型有：
- 二次指数平滑
- 局部加权模型
- 线性模型
- Arima模型

除了模型，还有试了很多去噪方法，试过不同的滑窗方式，比赛还是很累的，特别是辛苦写的代码完全没有作用，这很打击士气。建议大家找好队友，分工合作，这样才不至于中途就放弃了。最后初赛使用二次指数平滑，复赛使用局部加权模型。

感觉预测算法没什么好讲的，毕竟全靠玄学，都是瞎写一通，再瞎调参，为什么分高也完全不知道。

## 放置算法

- 放置算法采用动态规划的背包算法，其实贪心算法采用恰当的放置策略已经能取得接近最优解的结果，最后初赛对比了我的python代码和队友的C++代码，最后采用的是队友C++版代码，预测是动态规划，放置是贪心算法。
- 由于C++代码主要部分是队友完成，没有队友许可，这里只将自己python版代码开源，此代码初赛可取得235+的成绩。开源代码使用的是二维背包进行，即以优化CPU为例，将CPU作为价值，内存作为重量（限制条件），但这样的问题是很容易产生内存放满了，CPU占比很低的情况。于是加入判断，若放置的服务器放置率小于阈值，则回收此服务器的虚拟机，打散顺序重新放置。
- 此放置算法，线下测试了很多情况均可得最优解，后期花了2天移植倒C++版本，但是计算出的结果和python版相差很多，至今不知道原因。
- 放置算法的改进：建议使用3维背包，即以CPU和内存作为约束条件，去max(CPU+MEM)，这样代码的运行速度更快，而且效果是一样的。
- 关于放置率的提升：根据放置结果，最后一个服务器可能存在放置率不足的情况，可向最后一个添加虚拟机直至放满，或者直接将此虚拟机删除，即通过放置结果修改预测结果，初赛加入此条策略，提高了接近8分，还是挺有效的。
