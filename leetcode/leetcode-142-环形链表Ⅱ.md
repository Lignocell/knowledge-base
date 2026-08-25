# 142.环形链表Ⅱ

---

## 一、题目

给定一个链表的头节点 `head` ，返回链表开始入环的第一个节点。*如果链表无环，则返回 `null`。

如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。为了表示给定链表中的环，评测系统内部使用整数 `pos` 来表示链表尾连接到链表中的位置（**索引从0 开始*）。如果`pos` 是`-1`，则在该链表中没有环。*注意：`pos` 不作为参数进行传递*，仅仅是为了标识链表的实际情况。

**不允许修改* 链表。

 

**示例 1，*

![img](https://assets.leetcode.com/uploads/2018/12/07/circularlinkedlist.png)

```
输入：head = [3,2,0,-4], pos = 1
输出：返回索引为 1 的链表节点
解释：链表中有一个环，其尾部连接到第二个节点。
```

**示例 2，*

![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2018/12/07/circularlinkedlist_test2.png)

```
输入：head = [1,2], pos = 0
输出：返回索引为 0 的链表节点
解释：链表中有一个环，其尾部连接到第一个节点。
```

**示例 3，*

![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2018/12/07/circularlinkedlist_test3.png)

```
输入：head = [1], pos = -1
输出：返回null
解释：链表中没有环。
```

##  二、解析

### 思路

使用快慢指针进行解答,图解请参考https://leetcode.cn/problems/linked-list-cycle-ii/solutions/12616/linked-list-cycle-ii-kuai-man-zhi-zhen-shuang-zhi-

### 代码

```cpp
class Solution {
public:
    ListNode *detectCycle(ListNode *head) {
        ListNode*p=head,*q=head;//快慢指针同意起跑线
        while(q&& q->next)//由于要定义q的速度比p快，如果p先一步到达终点，证明该链表并不是环状链表。
        {
            p=p->next;
            q=q->next->next;
            if(p==q) break;
        }
        if(q==NULL || q->next==NULL) return NULL;//与上面的理由同理。
            p=head;//让一个指针返回原点
            while(p!=q)
            {
            p=p->next;
            q=q->next;
            }
           return p;
    }
};
```
