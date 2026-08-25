# 838.三元组

---

## 一、题目

定义三元组（a,b, c）（a,b,c 均为正数）的距离 D=|a-b|+|b-c|+|c-a|。给定3个非空整数集合 S1, S2 ,S3, 按升序分别存储在 3 个数组中。请设计一个尽可能高效的算法，计算并输出所有可能的三元组（a, b, c）（a∈S1,b∈S2,c∈S3）中的最小距离。例如 S1={-1, 0, 9}, S2={-25，10，0，1}，S3={2，3，7，0，1}，则最小距离为 2，相应的三元组为（0，1，0）。

程序中的主要部分已经帮你写好了，你只需要将如下代码拷贝到你的环境中，并且补充 func函数功能即可。函数功能描述如下：

### 输入参数

输入三个参数，分别为存储三个非空集合的队列

### 返回值说明

返回一个整形值，表示所有可能的三元组（a, b, c）（a∈S1,b∈S2,c∈S3）中的最小距离

### 模版代码

```cpp
/*************************************************************************
    > File Name: solve.cpp
    > Author:
    > Mail:
    > Created Time:
 ************************************************************************/
#include <iostream>
#include <cstdlib>
#include <queue>
using namespace std;

int min_num(int a, int b, int c) {
    if (a > b) swap(a, b);
    if (a > c) swap(a, c);
    return a;
}

int func(queue<int> que1, queue<int> que2, queue<int> que3) {
    //TODO
}

int main() {
    int m, n, k, x;
    queue<int> que1, que2, que3;
    cin >> m >> n >> k;
    for (int i = 0; i < m; i++) {
        cin >> x;
        que1.push(x);
    }
    for (int i = 0; i < n; i++) {
        cin >> x;
        que2.push(x);
    }
    for (int i = 0; i < k; i++) {
        cin >> x;
        que3.push(x);
    }
    cout << func(que1, que2, que3) << endl;
    return 0;
}
```

---

## 二、解析

### 思路

本题会分为三个数组，分别是：
S1= { -1,      0， 9}, 
S2= {-25，10，0，1}：
S3= {  2，  9，  17，0，1}

当选取{-1，-25，2}时，画出一个横轴，分别标出点位所在的位置，其中计算距离时，相当于<u>首尾两个节点之间距离的二倍的绝对值</u>（即中间的点位可以只要不出那个范围，中间可以忽略不计），这三个点所形成的距离为54；然后三个数向后移动。

此时，4便是-25的唯一解，即只有用-25与其他两个数字进行匹配，方能求出54这个值，那么便可以解释说将-25进行排除，以此作为循环。

### 代码

```cpp
/*************************************************************************
    > File Name: solve.cpp
    > Author:
    > Mail:
    > Created Time:
 ************************************************************************/
#include <iostream>
#include <cstdlib>
#include <queue>
using namespace std;

int min_num(int a, int b, int c) {
    if (a > b) swap(a, b);
    if (a > c) swap(a, c);
    return a;
}

int func(queue<int> que1, queue<int> que2, queue<int> que3) {
    //TODO
    int n=0x3f3f3f3f;//这个值代表int中能初始化最大的数字
    while(!que1.empty() && !que2.empty() && !que3.empty())//当三个数组中，但凡有一个没有元素时，循环停止
    {
        int a=que1.front(),b=que2.front(),c=que3.front();//将每个数组的首元素赋值给a,b,c
        int temp=abs(a-b)+abs(a-c)+abs(b-c);//abs指绝对值
        if(temp<n)n=temp;
        //接下来，将三元组中的最小值进行剔除
        int d=min_num(a,b,c);//d就是三元组中的最小值
        if(d==a) que1.pop();
        else if(d==b) que2.pop();
        else if(d==c) que3.pop();
    }
    return n;
}

int main() {
    int m, n, k, x;
    queue<int> que1, que2, que3;
    cin >> m >> n >> k;
    for (int i = 0; i < m; i++) {
        cin >> x;
        que1.push(x);
    }
    for (int i = 0; i < n; i++) {
        cin >> x;
        que2.push(x);
    }
    for (int i = 0; i < k; i++) {
        cin >> x;
        que3.push(x);
    }
    cout << func(que1, que2, que3) << endl;
    return 0;
}
```

