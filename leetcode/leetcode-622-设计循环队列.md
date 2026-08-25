# 622.设计循环队列

---

## 一、题目

设计你的循环队列实现。循环队列是一种线性数据结构，其操作表现基于FIFO（先进先出）原则并且队尾被连接在队首之后以形成一个循环。它也被称为“环形缓冲器”。

循环队列的一个好处是我们可以利用这个队列之前用过的空间。在一个普通队列里，一旦一个队列满了，我们就不能插入下一个元素，即使在队列前面仍有空间。但是使用循环队列，我们能使用这些空间去存储新的值。

你的实现应该支持如下操作：

- `MyCircularQueue(k)`: 构造器，设置队列长度为 k 。
- `Front`: 从队首获取元素。如果队列为空，返回 -1 。
- `Rear`: 获取队尾元素。如果队列为空，返回 -1 。
- `enQueue(value)`: 向循环队列插入一个元素。如果成功插入则返回真。
- `deQueue()`: 从循环队列中删除一个元素。如果成功删除则返回真。
- `isEmpty()`: 检查循环队列是否为空。
- `isFull()`: 检查循环队列是否已满。

 

**示例，*

```
MyCircularQueue circularQueue = new MyCircularQueue(3); // 设置长度为3
circularQueue.enQueue(1);  // 返回 true
circularQueue.enQueue(2);  // 返回 true
circularQueue.enQueue(3);  // 返回 true
circularQueue.enQueue(4);  // 返回 false，队列已满
circularQueue.Rear();  // 返回 3
circularQueue.isFull();  // 返回 true
circularQueue.deQueue();  // 返回 true
circularQueue.enQueue(4);  // 返回 true
circularQueue.Rear();  // 返回 4
```

 

**提示，*

- 所有的值都在 0 到 1000 的范围内：
- 操作数将在 1 到 1000 的范围内：
- 请不要使用内置的队列库。

---

## 二、解析

### 思路

本题打算以单向循环链表为底层进行设计循环队列。

### 代码

```cpp
struct node
{
    int node;
    node*next;
}

class MyCircularQueue {
public:
    int size,count;
    node *head,*tail;
       MyCircularQueue(int k) {
           head=new node();
           tail=head;//先让尾指针指向头指针
           for(int i=0;i<k;i++)
           {
               tail->next=new node();
               tail=tail->next;//让尾指针后面开辟一个节点
           }
           tail->next=head;//让该节点指向头指针
           size=k;
           count=0;
       }
    
    bool enQueue(int value) { 
        if(isFull()) return false;
        tail=tail->next;//让尾指针后面开辟一个新的尾节点
        tail->data=value;
        count++;
        return true;
    }
    
    bool deQueue() {
        if(isEmpty()) return false;
        head=head->next;
        count--;
        return true;
    }
    
    int Front() {
        if(isEmpty()) return false;
        return head->data;
    }
    
    int Rear() {
        if(isEmpty()) return false;
        return tail->data;
    }
    
    bool isEmpty() {
        return count==0;
    }
    
     bool isFull() {
     return count==size;
    }
}：
```

