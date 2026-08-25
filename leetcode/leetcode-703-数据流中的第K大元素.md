# 703.数据流中的第K大元素

---

## 一、题目

设计一个找到数据流中第 `k` 大元素的类（class）。注意是排序后的第`k` 大元素，不是第`k` 个不同的元素。

请实现`KthLargest` 类：

- `KthLargest(int k, int[] nums)` 使用整数 `k` 和整数流 `nums` 初始化对象。
- `int add(int val)` 将`val` 插入数据流`nums` 后，返回当前数据流中第`k` 大的元素。

 

**示例 1，*

**输入：*
["KthLargest", "add", "add", "add", "add", "add"]
[[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]

**输出：*[null, 4, 5, 5, 8, 8]

**解释：*

KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]);
kthLargest.add(3); // 返回 4
kthLargest.add(5); // 返回 5
kthLargest.add(10); // 返回 5
kthLargest.add(9); // 返回 8
kthLargest.add(4); // 返回 8

 

**示例 2，*

**输入：*
["KthLargest", "add", "add", "add", "add"]
[[4, [7, 7, 7, 7, 8, 3]], [2], [10], [9], [9]]

**输出：*[null, 7, 7, 7, 8]

**解释：*

KthLargest kthLargest = new KthLargest(4, [7, 7, 7, 7, 8, 3]);
kthLargest.add(2); // 返回 7
kthLargest.add(10); // 返回 7
kthLargest.add(9); // 返回 7
kthLargest.add(9); // 返回 8

---

## 二、解析

### 思路

本题需要注意一些点，其一：因为要求比K大的元素，即从第K个元素开始一直到结束，证明本题需要进行排序；其二：要求保证元素之间允许重复而不是让元素进行合并。

同时，要求找从K==开始=，比K大的值，那么可以认为后半边的数据流是从K开始的小顶堆。

### 代码

```cpp
class KthLargest {
public:
    multiset<int>mt;//set容器会合并同类元素，而multiset不会
    int k;
        KthLargest(int kValue, vector<int>& nums) {
            this->k=kValue;//将kValue赋值给k
            //this->指的是当前对象的指针
            for(auto x:nums)//遍历nums，并将数据存放到容器内，使其自动排序
            {
                mt.insert(x);
            }
            return;
        }
        int add(int val) {
            if(mt.size()<k)//此时k相当于后面小顶堆的大小，此时小顶堆还没由达到预定大小
            {
                mt.insert(val);
            }
            else if(val>*mt.begin())//val值比小顶堆的顶部元素大
                //*mt.begin()表示此时小顶堆的节点指向的值，而不加解引用符只能说明指的是此时小顶堆的顶部节点，只是一个迭代器
            {
                mt.insert(val);
            }
            //无论前边两个if如何筛选，都需要进入这个if当中，查看此时小顶堆的数量大小
            if(mt.size()>k)
            {
               mt.erase(*mt.begin()); 
            }
            return *mt.begin();
        }
};
```
