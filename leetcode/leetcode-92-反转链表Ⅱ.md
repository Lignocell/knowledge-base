# 92.反转链表

---

## 一、题目

给你单链表的头指针`head` 和两个整数`left` 和`right`，其中`left <= right`。请你反转从位置 `left` 到位置`right` 的链表节点，返回 **反转后的链表**。

 

**示例 1，*

![img](https://assets.leetcode.com/uploads/2021/02/19/rev2ex2.jpg)

```
输入：head = [1,2,3,4,5], left = 2, right = 4
输出：[1,4,3,2,5]
```

**示例 2，*

```
输入：head = [5], left = 1, right = 1
输出：[5]
```

##  二、解析

### 思路

本题的思路其实是将head进行递归化，什么意思呢，如下所示。

- 1->2->3->4->5->NULL，反转234三个节点，那么进行缩小化。
- 2->3->4，左边缩小一个，右面缩小一个，使得2->3->4重新排序变为1->4->3->2

### 代码

```cpp
class Solution {
public:
    ListNode* reverseBetween(ListNode* head, int left, int right) {

        if(left==1 && right ==1) return head;//当链表只有一个节点时直接返回
        else if(left!=1) head->next=reverseBetween(head->next,left-1,right-1);//当反转的链表不包括头节点但包括尾节点时
        else//当翻转链表的内部包括头节点时
        {
           ListNode new_head,*tail=head->next;//使用tail记录新链表的尾节点，即当前旧链表的节点的下一个节点，是反转过后的                                                 尾节点。
            new_head=reverseBetween(head->next,left,right-1);
            head->next=tail->next;//将head的下一节点指向tail的下一个节点，为head插入进tail做准备
            tail->next=head;//将head插入到tail节点的后面去
            head=new_head;
        }
        return head;
    }
};
```
