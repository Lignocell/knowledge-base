# 20.有效的括号

---

## 一、题目

给定一个只包括 `'('`，`')'`，`'{'`，`'}'`，`'['`，`']'` 的字符串 `s` ，判断字符串是否有效。

有效字符串需满足：

1. 左括号必须用相同类型的右括号闭合。
2. 左括号必须以正确的顺序闭合。
3. 每个右括号都有一个对应的相同类型的左括号。

 

**示例 1，*

**输入:** s = "()"

**输出:** true

**示例 2，*

**输入:** s = "()[]{}"

**输出:** true

**示例 3，*

**输入:** s = "(]"

**输出:** false

**示例 4，*

**输入:** s = "([])"

**输出:** true

---

## 二、解析

### 思路：

本题其实就是一个消消乐玩法，先创建一个空栈，然后开始遍历，左括号进栈，右括号先与左括号匹配，如果是同一类型的括号，则出栈，最后观察是否有多余的符号。

### 代码：

```cpp
class Solution {
public:
    bool isValid(string s) {
        stack<char>buffer;//创建一个栈
        int len=s.size();
        
        for(int i=0;i<len;i++)
        {
            char c=s[i];
            switch(c)//s代表的是整个字符串，而这里是需要每个字符都要判断，所有用c获取s的字符。
            {
                case '(':
                case '[':
                case '{':
                    buffer.push(c);//将左括号插入
                    break;
                case ')':
                    if(buffer.empty()||buffer.top()!='(') return false;//判断栈是空的或者顶针并不是相匹配的符号。
                    buffer.pop();//到达这一步，证明括号匹配。
                    break;
                case ']':
                    if(buffer.empty()||buffer.top!='[') return false;
                    buffer.pop();
                    break;
                case '}':
                    if(buffer.empty()||buffer.top!='{') return false;
                    buffer.pop();
                    break;                                 
            }
        return buffer.empty();//返回栈是空的，说明所有括号全部匹配完毕，否则证明是非法的。
        }        
    }
};
```
