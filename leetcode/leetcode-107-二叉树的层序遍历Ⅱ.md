# 107.二叉树的层序遍历遍历

---

## 一、题目

给你二叉树的根节点`root`，返回其节点值**自底向上的层序遍历**。（即按从叶子节点所在层到根节点所在的层，逐层从左向右遍历）

 

**示例 1，*

![img](https://assets.leetcode.com/uploads/2021/02/19/tree1.jpg)

```
输入：root = [3,9,20,null,null,15,7]
输出：[[15,7],[9,20],[3]]
```

**示例 2，*

```
输入：root = [1]
输出：[[1]]
```

**示例 3，*

```
输入：root = []
输出：[]
```

---

## 二、解析

### 思路

先进行二叉树的深搜，然后将数组的头部和尾部调换位置，达到从下往上遍历的目的。

### 代码

```cpp
class Solution {
public:
    void dfs(TreeNode* root,int k,vector<vector<int>>ans)
    {
        if(root==NULL) return;
        if(k==ans.size()) ans.push_back(vector<int>());//防止越界
        ans[k].push_back(root->val);
        dfs(root->left,k+1;ans);
        dfs(root->right,k+1,ans);
        return ans;
    }
vector<vector<int>> levelOrderBottom(TreeNode* root) {
    vector<vector<int>>ans;//定义ans将结果存储到数组中去
    dfs(root,0,ans);//ans是结果变量
    for(int i=0,j=ans.size();i<j;i++,j--)
    {
        swap(ans[i],ans[j]);
    }
  }
    return ans;
}
```

