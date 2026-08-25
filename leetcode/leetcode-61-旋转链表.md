# 61.旋转链表

----

## 一、题目

给你一个链表的头节点`head` ，旋转链表，将链表每个节点向右移动`k` 个位置。

 

**示例 1，*

```
输入：head = [1,2,3,4,5], k = 2
输出：[4,5,1,2,3]
```

**示例 2，*

```
输入：head = [0,1,2], k = 4
输出：[2,0,1]
```

## 二、解析

### 思路：

使用两个指针进行旋转，利用快慢指针找出旋转时需要断裂的节点，让一个指针成为新链表的头部。<u>这道题建议画图/u>)

### 代码：

```cpp
class Solution {
public:
    
    int getlen(ListNode*head)
    {
        int m=0;
        while(head!=NULL)//通过遍历整个链表，利用m进行计数
        {
        head=head->next;
            m++;
        }
    }
    
    
    ListNode* rotateRight(ListNode* head, int k) {
        if(head==NULL) return head;
        
        //首先需要将k化简，减少时间复杂度
        ListNode*n=getlen(head);
        k%=n;
        if(k==0)return head;//如果k 等于，那么不需要进行旋转了
        
        ListNode*p=head,*q=head;
        for(int i=0;i<k+1;i++) p=p->head;//将p移动到新链表的首节点
        while(p->next!=NULL) //将p移动到NULL，q移动到新链表首节点的前一个
        {
            p=p->next;
            q=q->next;
        }
        p=q->next;//p指向即将成为新链表的第一个节点
        q->next=NULL，/断开链表，让q成为新的尾节点
        
        //接下来，需要让p旋转到链表的头部（原来是在断裂位置的头部），即p这部分的尾部与原链表的头部相连
            q=p;//重新定位q的位置
        while(q->next!=NULL) q=q->next;//让q走到p为首地址的链表的尾部
        q->next=head;//连接链表
        return p;
    }
};
```
