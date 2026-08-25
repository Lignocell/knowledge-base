# 266.表达式求值

---

## 一、题目

 给出一个表达式,其中运算符仅包含 `+,-,*,/,^` 要求求出表达式的最终值。

 数据可能会出现括号情况，还有可能出现多余括号情况，忽略多余括号，正常计算即可：

 数据保证不会出现大于 *m**a**x* *l**o**n**g* *i**n**t* 的数据；

 数据可能会出现负数情况，幂次不可能为负数，除法采用向 0 取整。

 注意：−9 和 +9 分别代表负数和正数的 9

------

#### 输入

 共一行，即为表达式。表达式长度不会超过1000.

#### 输出

 共一行，既为表达式算出的结果。

------

#### 样例输入1

```
(2+2)^(1+1)
```

#### 样例输出1

```
16
```

#### 样例输入2

```
9/-9
```

#### 样例输出2

```
-1
```

------

#### 数据规模与约束

 时间限制， s

 内存限制，56 M

 100% 的数据保证数据合法

---

## 二、解析

### 思路

这道题的根本在于求出每个运算符号的运算顺序，也就是说每个运算符号的权重。

| 3 | * | ( | 4 | + | 5 | ) |
| :------: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| 符号权重 |  0   |  2   |  0   |  0   |  1   |  0   |  0   |
| 附加权重 |  0   |  0   | 100  | 100  | 100  | 100  |  0   |
| 真实权重 |      |  2   |      |      | 101  |      |      |

- 附加权重：当遇到左括号时加 100，遇到右括号时减100。
- 符号权重：优先级越高，数字越小。

### 代码

```cpp
#include<iostream>
#include<math.h>
using namespace std;
#define max 0x3f3f3f3f
//判断是不是运算符
bool is_operator(char c)
{
    switch (c)
    {
    case '+':
    case '-':
    case '*':
    case '/':
    case '^':
        return true;
    default:
        return false;
    }
    return false;
}

long long aclac(string& s, long long l, long long r)//由于数据要求保证不会出现大于 max long int的数据，所以定义为long long
{
    //如果传入的是数字，让pri=最大值会使得if (pri >= cur_pri)运行，所以需要让pri减一
    long long pos=-1,pri = max - 1,cur_pri, temp_pri=0;//pri是真实权重，cur_pri是符号权重，temp_pri是附加权重
    for (long long i = l; i < r; i++)
    {
        cur_pri = max;
        switch (s[i])
        {
        case '(':
            temp_pri += 100;
            break;
        case ')':
            temp_pri -= 100;
            break;
        case '+':
        case '-':
            cur_pri = temp_pri + 1;
            break;
        case '*':
        case '/':
            cur_pri = temp_pri + 2;
            break;
        case '^':
            cur_pri = temp_pri + 3;
            break;
        }

        //判断负号是否和数字绑定，比如 -9
        if ((s[i] == '-' || s[i] == '+') && (i - 1 < 0 || is_operator(s[i - 1])))
        {
            cur_pri += 1000;
        }

        //更新真实权重
        if (pri >= cur_pri)
        {
            pri = cur_pri;
            pos = i;
        }
    }
        if (pos == -1)//证明进入函数的是一个数字，而不是符号
        {
            long long num = 0;
            for (long long i = l; i < r; i++)
            {
                if (s[i] > '9' || s[i] < '0') continue;//如果不是数字，将跳过这一次循环
                num = num * 10 + (s[i] - '0');//将字符串转化为数字，括号内部是用来减去尾部的ACSII值。
            }
            return num;
        }

        //进入函数的是一个数字
            //以pos为中心，分成两部分，因为pos位置代表的是运算符
        else
        {
            long long a = aclac(s, l, pos);//左闭右开
            long long b = aclac(s, pos + 1, r);
            switch (s[pos])
            {
            case '+':
                return a + b;
                break;
            case '-':
                return a - b;
                break;
            case '*':
                return a * b;
                break;
            case '/':
                return a / b;
                break;
            case '^':
                return pow(a, b);
            }

        }
        return 0;
    
}


int main()
{
    string n;
    cin >> n;

    cout << aclac(n, 0, n.size()) << endl;
    return 0;
}

```


