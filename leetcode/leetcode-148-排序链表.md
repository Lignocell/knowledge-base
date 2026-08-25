# 148.排序链表

## 一、题目

给你链表的头结点 `head` ，请将其按**升序** 排列并返回**排序后的链表** 。

 

**示例 1，*

![img](https://assets.leetcode.com/uploads/2020/09/14/sort_list_1.jpg)

```
输入：head = [4,2,1,3]
输出：[1,2,3,4]
```

**示例 2，*

![img](https://assets.leetcode.com/uploads/2020/09/14/sort_list_2.jpg)

```
输入：head = [-1,5,3,4,0]
输出：[-1,0,3,4,5]
```

**示例 3，*

```
输入：head = []
输出：[]
```

 

**提示，*

- 链表中节点的数目在范围`[0, 5 * 104]` 鍐?
- `-105 <= Node.val <= 105`

 

**进阶，*你可以在 `O(nlogn)` 时间复杂度和常数级空间复杂度下，对链表进行排序吗：

## 二、解析

### 思路

本题排序时要求时间复杂度为nlongn，那么只有快速排序与归并排序满足时间复杂度的要求。

快速排序选择中间项作为基准值，这样才能降低时间复杂度。

### 代码

#### 快速排序

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
        ListNode* sortList(ListNode* head) {
            if(head==nullptr||head->next==nullptr) return head;//如果数组为空或者只有一个，那么返回即可。
            int l=head->val,r=head->val,z;//l和r用于确定最小值和最大值
            ListNode*p=head,*h1=nullptr,*h2=nullptr;//将head赋值给p,h1作为基准值前面部分的首地址，h2作为基准值后面部分的首地址
            while(p){//遍历数组，找到其中的最小值和最大值
                l=min(p->val,l);
                r=max(p->val,r);
                p=p->next;
            }
            p=head;//在上面的循环中，p在末尾，现在重新将p指回head
            z=(l+r)>>1;//z=(l+r)/2会选择向零取整，意味着无论正负，都会在向零方向取整，而z=(l+r)>>1，是向下取整，比如说z的结果如果是-1.5，那么会变为-2。
            if(l==r) return head;//如果最大值与最小值相等说明此时链表中元素均相等。
            while(p){
                ListNode* q=p->next;//作为备份
                if(p->val<=z){//分割链表
                    p->next=h1;//采用头插法，将数据放入h1的头部去
                    h1=p;//将h1更新到p，让p作为链表的头节点
                }else{
                    p->next=h2;
                    h2=p;
                }
                q=p;//将p指向原链表的下一位，继续遍历
            }
            //排序两个链表
            h1=sortList(h1);
            h2=sortList(h2);
            if(!h1) return h2;
            p=h1;
            while(p->next) p=p->next;//遍历h1，让p跑到h1的尾部
            p->next=h2;//将h1与h2链接在一起，形成一个新的链表。
            return h1;
        }
};
```

#### 归并排序

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    int getlenth(ListNode* head){
        int m=0;
        while(head){
            m++;
            head=head->next;
        }
        return m;
    }
   
    ListNode*merge_sort(ListNode* head,int n){
        if(n<=1) return;
        int l=n/2,r=n-1;//l为左链表的长度，r为右链表的长度
        ListNode*p=head,*p1,*p2,*ret;//p1作为左链表的首地址，p2作为右链表的首地址
        for(int i=0;i<l-1;i++) p=p->next;//遍历链表，直到p走到左链表的尾部
        p1=head,p2=p->next;
        merge_sort(p1,l);
        merge_sort(p2,r);
        p=&ret;//ret作为虚拟头节点
        ret->next=NULL;//初始化p的next节点变为NULL
        ListNode*cur=ret;//用cur遍历结果链表
        while(p1||p2){
            if(p2==NULL||(p1&&p1->val<=p2->val)){
                cur->next=p1;//将p1接入结果链表
                cur=cur->next;//让cur更进一步
                p1=p1->next;//在原左链表中，让p1向后移动一步
            }else{//同理
                cur->next=p2;
                cur=cur->next;
                p2=p2->next;
            }
        }
        return ret->next;
    }
    
        ListNode* sortList(ListNode* head) {
            int n=getlenth(head);//计算链表的长度
            merge_sort(head,n);//排序
            return head;
        }
};
```
