# 141.环形链表

## 一、题目

给你一个链表的头节点`head` ，判断链表中是否有环。

如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。为了表示给定链表中的环，评测系统内部使用整数 `pos` 来表示链表尾连接到链表中的位置（索引从0 开始）。*注意：`pos` 不作为参数进行传递* 。仅仅是为了标识链表的实际情况。

*如果链表中存在环* ，则返回 `true` 。否则，返回`false` 。

 

**示例 1，*

![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2018/12/07/circularlinkedlist.png)

```
输入：head = [3,2,0,-4], pos = 1
输出：true
解释：链表中有一个环，其尾部连接到第二个节点。
```

**示例 2，*

![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2018/12/07/circularlinkedlist_test2.png)

```
输入：head = [1,2], pos = 0
输出：true
解释：链表中有一个环，其尾部连接到第一个节点。
```

**示例 3，*

![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2018/12/07/circularlinkedlist_test3.png)

```
输入：head = [1], pos = -1
输出：false
解释：链表中没有环。
```

---

## 二、解析

### 思路：

进行跑步比赛，假设q与p两个人进行跑步，p跑的快，如果是环形链表，则跑到快的可以从后面 追上p，否则，两人不会相遇。

### 代码演示：

```cpp
class Solution {
public:
    bool hasCycle(ListNode *head) {
        ListNode *p=head,*q=head;//假设两个人从头开始
        while(p&&p->next)//确定p不是空链表或者只有一个节点的链表
        {
         q=q->next;
         p=p->next->next;//p跑的比q快
        if(p==q) return 1;
        }
        return 0;
    }
```
