# 19.删除链表的倒数第N个节点

---

## 一、题目

给你一个链表，删除链表的倒数第`n` 个结点，并且返回链表的头结点。

 

**示例 1，*

![img](https://assets.leetcode.com/uploads/2020/10/03/remove_ex1.jpg)

```
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
```

**示例 2，*

```
输入：head = [1], n = 1
输出：[]
```

**示例 3，*

```
输入：head = [1,2], n = 1
输出：[1]
```

##  二、解析

### 思路

利用快慢指针进行定位，让慢指针跳过所需要删除的节点，直接指向下一个节点。=（注意：在实际代码中跳过的指针记得内存释放，以免造成内存浪费）=

### 代码

```cpp
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode new_head,*p=&new_head,*q=p;//定义虚拟头节点，防止插入头节点时造成链表丢失
        new_head.next=head;//虚拟头节点指向链表
        for(int i=0;i<n+1;i++) q=q->next;//让q走到倒数第n+1的节点，遍历时q到达NULL时，p刚好到达倒数第N个节点的前一                                            个位置
        while(q)//pq二指针移动
        {
            q=q->next;
            p=p->next;
        }
        p->next=p->next->next;//跳过要删除的节点，达到删除的目的
        return new_head.next;//返回原链表，记得跳过虚拟头节点
    }
};
```



