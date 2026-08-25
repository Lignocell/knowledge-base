# 206.反转链表

## 题目

给你单链表的头节点`head` ，请你反转链表，并返回反转后的链表。

 

**示例 1，*

![img](https://assets.leetcode.com/uploads/2021/02/19/rev1ex1.jpg)

```
输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]
```

**示例 2，*

![img](https://assets.leetcode.com/uploads/2021/02/19/rev1ex2.jpg)

```
输入：head = [1,2]
输出：[2,1]
```

**示例 3，*

```
输入：head = []
输出：[]
```

---

## 解析

###  方法一：头插法

进行链表的遍历，然后将链表插入到新链表的头部，完成链表的反转。

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        listNode* p=head,new_head,*q;
       //将head的头地址指向p，创建一个新的链表，此时新链表的头地址为new_head
        new_head=NULL;//先将new_head初始化
        while(p)
        {
            q=p->next;//先将p的下一个节点存储到q，防止原链表丢失
            p->next=new_head.next;//将p的下一个节点指向新链表，即完成新链表的插入
            new_head.next=p;//更新新链表的下一个节点指向p
            p=q;//将p指向下一个节点，进行循环
        }
        return new_head.next;//返回新链表的头节点，new_head不是新链表的一部分，即虚拟头节点
    }
};
```

### 方法二：递归解法

将除第一节点以外所有节点利用递归函数进行翻转，然后将头节点接入末尾，完成链表反转。

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        if(head==NULL||head->next==NULL) return head;//即空链表与只有一个节点的链表不需要反转
        ListNode* tail=head->next;//用tail将除了head以外的节点储存起来
        ListNode*new1=reverseList(head->next);//将除head以外的链表进行反转
        //反转后原来的链表从head的后面转到了head的前面
        tail->next=head->next;//进行递归返回时，tail的next指针与head的next指针并不相等，即head的next指向的最终位置为NULL。所以，目的是维护head的朝向
        
        tail->next = head;//将tail->next指针所代表的值指向head，将head放到链表的末尾
    }
};
```

==注意==：反转链表时箭头不变，即最后一个节点依然指向NULL。

## 关于方法二AI解释（仅供参考）

假设我们有一个链表`1 -> 2 -> 3 -> 4 -> NULL`。

####  递归过程示例

1. **第一次递归**：
    - 当前节点 `head` 是`1`。
   - `tail = head->next`：此时`tail` 指向节点 `2`。
   - 递归调用 `reverseList(head->next)`，即 `reverseList(2)`。
2. **第二次递归**：
    - 当前节点 `head` 是`2`。
   - `tail = head->next`：此时`tail` 指向节点 `3`。
   - 递归调用 `reverseList(head->next)`，即 `reverseList(3)`。
3. **第三次递归**：
    - 当前节点 `head` 是`3`。
   - `tail = head->next`：此时`tail` 指向节点 `4`。
   - 递归调用 `reverseList(head->next)`，即 `reverseList(4)`。
4. **第四次递归（基本情况）**：
    - 当前节点 `head` 是`4`。
    - `tail = head->next`：此时`tail` 指向 `NULL`。
    - 递归调用 `reverseList(head->next)`，即 `reverseList(NULL)`，返回`NULL`。

### 反向回溯

现在开始回溯，逐步反转链表：

#### 第三次递归返回

 - 当前节点 `head` 是`3`，返回的 `new1` 是`4`（反转后的链表的头节点）。

- `head->next = tail->next;`

  ：

   - `tail` 是`4`，所以`tail->next` 是`NULL`。
   - 这行代码将`head->next`（即 `3->next`）设置为 `NULL`，将 `3` 的`next` 指向 `NULL`。

- `tail->next = head;`

  ：

  - 这行代码将`4->next` 指向 `3`，现在链表变成`4 -> 3 -> NULL`。

#### 第二次递归返回

 - 当前节点 `head` 是`2`，返回的 `new1` 仍然是`4`。
- **`head->next = tail->next;`**：
   - `tail` 是`3`，所以`tail->next` 是`NULL`。
   - 这行代码将`head->next`（即 `2->next`）设置为 `NULL`，将 `2` 的`next` 指向 `NULL`。
- **`tail->next = head;`**：
  - 这行代码将`3->next` 指向 `2`，现在链表变成`4 -> 3 -> 2 -> NULL`。

#### 第一次递归返回

 - 当前节点 `head` 是`1`，返回的 `new1` 仍然是`4`。
- **`head->next = tail->next;`**：
   - `tail` 是`2`，所以`tail->next` 是`NULL`。
   - 这行代码将`head->next`（即 `1->next`）设置为 `NULL`，将 `1` 的`next` 指向 `NULL`。
- **`tail->next = head;`**：
  - 这行代码将`2->next` 指向 `1`，最终链表变成`4 -> 3 -> 2 -> 1 -> NULL`。
