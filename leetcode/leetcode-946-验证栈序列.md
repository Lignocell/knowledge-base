# 946.验证栈序列

---

## 一、题目

给定 `pushed` 和`popped` 两个序列，每个序列中**值都不重复*，只有当它们可能是在最初空栈上进行的推入push 和弹出pop 操作序列的结果时，返回`true`；否则，返回 `false` 。

 

**示例 1，*

```
输入：pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
输出：true
解释：我们可以按以下顺序执行：
push(1), push(2), push(3), push(4), pop() -> 4,
push(5), pop() -> 5, pop() -> 3, pop() -> 2, pop() -> 1
```

**示例 2，*

```
输入：pushed = [1,2,3,4,5], popped = [4,3,5,1,2]
输出：false
解释：不能在2之前弹出1
```

 

**提示，*

- `1 <= pushed.length <= 1000`
- `0 <= pushed[i] <= 1000`
- `pushed` 的所有元素**互不相同**
- `popped.length == pushed.length`
- `popped` 是`pushed` 的一个排列

---

## 二、解析

### 思路

这道题同样也和火车进栈相似，push进栈时，按照顺序进栈，示例二中，先入1~4，当栈顶与poped第1号位置相同时，执行出栈，出栈4 后，当要求出栈3时，那么先入5；然后会发现，此时，1是栈底元素，2是栈顶元素，poped的出栈顺序却是先1，再2，显然，该序列是非法序列，返回false。

### 代码

```cpp
class Solution {
public:
    bool validateStackSequences(vector<int>& pushed, vector<int>& popped) {
        int x=0,n=pushed.size();
        stak<int>s;
        
        for(int i=0;i<n;i++)
        {
            if(s.empty() || s.top()!=poped[i])//先判断栈顶是否是要出栈的元素
            {
                while(x<pushed.size() && pushed[i]!=poped[i])//然后进行入栈，两种情况，第一种是当所有的元素均已经入栈                                                                 了，并没有找到相应的弹栈元素；第二种是当找到了出栈的元素                                                                时，停止循环
                {
                    s.push(pushed[x]);
                    x++;
                }
                if(x == pushed.size()) return false;//对应第一种情况
                else if(pushed[i] == poped[i])//对应第二种情况
                {
                    s.push(pushed[i]);
                    x++;
                }
                s.pop();
            }
            return true;
        }
    }
};
```
