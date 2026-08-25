# 844.比较含退格的字符串

---

## 一、题目描述

给定 `s` 和`t` 两个字符串，当它们分别被输入到空白的文本编辑器后，如果两者相等，返回 `true` 。`#` 代表退格字符。

**注意，*如果对空文本输入退格字符，文本继续为空。

 

**示例 1，*

```
输入：s = "ab#c", t = "ad#c"
输出：true
解释：s 和t 都会变成 "ac"。
```

**示例 2，*

```
输入：s = "ab##", t = "c#d#"
输出：true
解释：s 和t 都会变成 ""。
```

**示例 3，*

```
输入：s = "a#c", t = "b"
输出：false
解释：s 会变成"c"，但 t 仍然是"b"。
```

 

**提示，*

- `1 <= s.length, t.length <= 200`

- `s` 和`t` 只含有小写字母以及字符`'#'`
---

## 解析

### 思路

本题的题意是出现＃将#前一位字母删除即模拟栈中弹出一个字符，没有则向栈中放入一个字符最后比较两个字符串，相同返回truue，不相同返回false

### 代码

```cpp
class Solution {
public:
    void pushpop(stack<char>&s1,string &s)//在函数内部对s的修改都会影响到它的调用，如果只是值传递，则不会影响原始字符串
        //s1是一个字符栈的引用。通过使用引用，避免了在函数调用时复制整个栈的内容，节省了内存和时间。
    {
        for(int i=0;i<s.length();i++)//遍历s
        {
            if(s[i]=='#') //如果遇到#，则从栈中弹出一个字符
            {
                if(!s.empty()) s1.pop();//确保s不为空，弹出栈中的元素
            }
            else s1.push(s[i]);//将元素推入栈中
        }
    }
    
        bool backspaceCompare(string s, string t) {
            stack<char>s1,s2;
            pushpop(s1,s);
            pushpop(s2,t);
            
            //比较两个字符栈
            if(s1.size()!=s2.size()) return false;//先比较两个字符串的大小
            while(!s1.empty())//如果s1为空，证明循环结束
            {
                if(s1.top()!=s2.top()) return false;//比较两个数组的顶部
                else
                {
                    s1.pop();
                    s2.pop();
                }
            }
            return true;                      
        }
};
```

