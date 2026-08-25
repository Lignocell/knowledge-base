# 245.货仓选址

---

## 一、题目

 在一条数轴上有 *N* 家商店，他们的坐标分别为 *A*[1]~A*[*N*]。现在需要在数轴上建立一家货仓，每天清晨，从货仓到每家商店都要运送一车商品。为了提高效率，求把货仓建在何处，可以使得货仓到每家商店的距离之和最小，输出最短距离之和。

------

#### 输入

 第一行输入一个数 *N*。（1≤*N*≤100000）

 接下来一行，输入 *N* 个数，表示商店的坐标。

#### 输出

 输出最短距离之和。

------

#### 样例输入

```
5
1 3 5 6 10
```

#### 样例输出

```
12
```

---

## 二、解析

### 思路

题目中要求距离最小，那么当货仓处在中间位置时，距离最小。

### 代码

```cpp
#include<iostream>
#include<algorithm>
#include<vector>
using namespace std;

int main()
{
    int n;//n表示商店的数量
    cin>>n;
    vector<int>arr;
    
    for(int i=0,a;i<n;i++)
    {
        cin>>a;//a表示每个商店在坐标轴的位置
        arr.push_back(a);
    }
    sort(arr.begin(),arr.end());//以algorithm为头文件的排序算法
    int sum=0;
    int p=arr[n/2];//p表示货仓位置
    for(int i=0;i<n;i++)
    {
        sum+=abs(arr[i]-p);//abs表示取绝对值
    }
    cout<<sum<<endl;
    return 0;
}
```

