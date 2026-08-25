# 23.合并K个升序链表

---

## 一、题目

给你一个链表数组，每个链表都已经按升序排列。

请你将所有链表合并到一个升序链表中，返回合并后的链表。

 

**示例 1，*

```
输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
解释：链表数组如下：
[
  1->4->5,
  1->3->4,
  2->6
]
将它们合并到一个有序链表中得到。
1->1->2->3->4->4->5->6
```

**示例 2，*

```
输入：lists = []
输出：[]
```

**示例 3，*

```
输入：lists = [[]]
输出：[]
```

## 二、解析

### 思路

将示例一的链表列出

```
1->4->5
1->3->4
2->6
```

对这三个链表进行合并排序，首先分别在三个链表取出首节点，分别为1、1、2。

比较大小，拿出他们的最小值放入结果链表中，然后删除它的链表节点，并让他们本身的链表向前移动一位，以此类推，结果变为了：

```
1->1->1->2->3->4->4->5->6
```



### 代码

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
    ListNode* mergeKLists(vector<ListNode*>& lists){
        multiset<int>mt;//使用mt来存储所有链表的节点
        for(int i=0;i<lists.size();i++){
            ListNode *current=lists[i];//使用current来遍历链表的每个节点
            while(current!=nullptr){
                mt.insert(current->val);//将所有的节点都插入mt中
                current=current->next;
            }
            ListNode new_head,*p=&new_head;//建立一个p指向结果链表的头节点
            for(auto x:mt){
                p->next=new ListNode(x);
                p=p->next;
            }
        }
        return new_head->next;
    }
};
```
