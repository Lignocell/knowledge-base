# 295.数据流的中位数

---

## 一、题目

**中位数*是有序整数列表中的中间值。如果列表的大小是偶数，则没有中间值，中位数是两个中间值的平均值。

- 例如 `arr = [2,3,4]` 的中位数是`3` 。
- 例如 `arr = [2,3]` 的中位数是`(2 + 3) / 2 = 2.5` 。

实现 MedianFinder 类

- `MedianFinder() `初始化`MedianFinder` 对象。
- `void addNum(int num)` 将数据流中的整数 `num` 添加到数据结构中。
- `double findMedian()` 返回到目前为止所有元素的中位数。与实际答案相差 `10-5` 以内的答案将被接受。

**示例 1，*

```
输入
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
输出
[null, null, null, 1.5, null, 2.0]

解释
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // 返回 1.5 ((1 + 2) / 2)
medianFinder.addNum(3);    // arr[1, 2, 3]
medianFinder.findMedian(); // return 2.0
```

---

## 二、解析

### 思路

本题其实主要在于大小顶堆的头部碰撞，即将数据流从中间分割，前面一个是大顶堆（小顶堆的取反），另一个是小顶堆。

### 代码

```cpp
class MedianFinder {
public:
    multiset<int> mt1, mt2; // mt1 用于保存较小的一半，mt2 用于保存较大的一半

    MedianFinder() {}

    void addNum(int num) {
        // 将新数字插入到适当的集合中
        if (mt1.empty() || num <= *mt1.rbegin()) {//rbegin指向的是最后一个元素；end指向的是容器的最后一个位置
            mt1.insert(num);
        } else {
            mt2.insert(num);
        }

        // 平衡两个集合的大小
        if (mt1.size() > mt2.size() + 1) {//此时证明mt1的个数大的多
            mt2.insert(*mt1.rbegin());
            mt1.erase(--mt1.end());
        } else if (mt2.size() > mt1.size()) {//此时证明mt2的数量多与mt1
            mt1.insert(*mt2.begin());
            mt2.erase(mt2.begin());
        }
    }
    
    double findMedian() {
        if (mt1.size() > mt2.size()) {
            return *mt1.rbegin();  // mt1 的最大值
        } else {
            return (*mt1.rbegin() + *mt2.begin()) / 2.0;  // 两个集合的中位数
        }
    }
};
```

