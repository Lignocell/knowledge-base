# 284.超市卖货

---

#### 题目描述

 超市里有*N*个商品，第 *i* 个商品必须在保质期 *d**i* 之前卖掉, 若卖掉可让超市获得 *p**i* 的利润

 每天只能卖一个商品

 现在你要让超市获得最大的利润.

#### 输入

 每组数据第一行为一个整数 N（0<*N*≤10000），即超市的商品数目

 之后*N*N行，每行各有两个整数, 第i行为*p**i*,*d**i*(1<=*p**i*,*d**i*<=10000)pi,di(1<=pi,di<=10000)

#### 输出

 输出当前条件下超市的最大利润

------

#### 输入样例1

```
7
20 1 
2 1 
10 3 
100 2 
8 2 
5 20 
50 10
```

#### 输出样例1

```
185
```

---

## 二、解析

### 思路

本题着眼于要获得最大的利润，那么如果此时商店中某件商品的保质期在7天内，那么优先卖这件商品，保质期在7天以外，那么就不在这7天卖了。

如果保质期在7天内的两件商品的保质期相同，那么就观察利润，获得利润大的放到前，获得利润小的，放在后面。

### 代码

```cpp
#include<iostream>
#include<vector>
#include<set>
#include<algorithm>
using namespace std;

struct data{
    data(int p,int d):p(p),d(d){}//构造了一个名为data的函数，其中，p和d是他的整型变量
  int p,d;//p是利润，d是保质期  
    //以下是运算符重载的相关概念
    bool operator <(const data&obj)const//第一个const表示不会修改obj内的对象，第二个const表示这个函数不会修改调用它的任何成员
    {
        if(d!=obj.d) return d<obj.d;//如果d与obj的d不相等，那么返回最小的那一项
        return p>obj.p;//反之，则返回利润较大的那一项
    }
};

int main()
{
    int n;//n是商品总数
    cin>>n;
    vector<data>arr;
    multiset<int>mt;
    //输入功能实现
    for(int i=0,p,d;i<n;i++){
        cin>>p>>d;
        arr.push_back(data(p,d));
    }
    sort(arr.begin(),arr.end());
    
    for(int i=0;i<n;i++)
    {
        if(arr[i].d>mt.size())//表示插入的商品的有效期比临期的要大，直接插入
        {
            mt.insert(arr[i].p);
        }
        else
        {
            if(arr[i].p>mt.begin())//由于multiset是自动排序，那么起始值就是最小值，将商品利润进行比较。
            {
                mt.erase(mt.begin());
                mt.insert(arr[i].p);
            }
        }
    }
    //计算最大利润
    int ans=0;
    for(auto x:mt)
    {
        ans+=x;
    }
    cout<<ans<<endl;
    return 0;
}
```

