# 1.两数之和

## 一、题目

给定一个整数数组`nums` 和一个整数目标值`target`，请你在该数组中找出 **和为目标值* *`target`* 的那 **两个** 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

你可以按任意顺序返回答案。

 

**示例 1，*

```
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为nums[0] + nums[1] == 9 ，返回[0, 1] 。
```

**示例 2，*

```
输入：nums = [3,2,4], target = 6
输出：[1,2]
```

**示例 3，*

```
输入：nums = [3,3], target = 6
输出：[0,1]
```

 

**提示，*

- `2 <= nums.length <= 104`
- `-109 <= nums[i] <= 109`
- `-109 <= target <= 109`
- **只会存在一个有效答案*

## 二、解析

### 思路

本题的关键在于推导出两个元素之和是否与目标值相同，并且不允许有重复的元素。

那么我们可以设两个指针分别指向数组中的最大值和最小值，如何两个指针所指的元素之和大于目标值，那么将尾指针向前移动一位；反之，向后移动一位；如果二者相等，那么结果就可以推断出了。

**注意**：数组的顺序不允许改变，允许改变的数组的下标。

### 代码

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int n=nums.size();
        vector<int>ind(n);//创建一个大小为n的容器来存储下标值。
        for(int i=0;i<n;i++) ind[i]=i;//为ind赋值
        sort(ind.begin(),ind.end(),[&](int i,int j)->bool{
            return nums[i]<nums[j];//定义一个规则，按照下标所对应的元素进行排序规则是ind[i]小于ind[j]。
        });
        int p1=0,p2=n-1;
        while(nums[ind[p1]]+nums[ind[p2]]!=target){
            if(nums[ind[p1]]+nums[ind[p2]]<target){
                p1++;
            }else{
                p2--;
            }
        }
        //此时，p1与p2所对应的值，就是target的两个分数
        vector<int>ret(2);//定义一个ret容器，按照从小到大的顺序返回结果
        ret[0]=ind[p1],ret[1]=ind[p2];
        if(ret[0]>ret[1]) swap(ret[0],ret[1]);
        return ret;
    }
};
```

