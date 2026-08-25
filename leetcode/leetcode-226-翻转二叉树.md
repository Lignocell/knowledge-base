# 226.翻转二叉树

---

## 一、题目

给你一棵二叉树的根节点 `root` ，翻转这棵二叉树，并返回其根节点。

 

**示例 1，*

![img](https://assets.leetcode.com/uploads/2021/03/14/invert1-tree.jpg)

```
输入：root = [4,2,7,1,3,6,9]
输出：[4,7,2,9,6,3,1]
```

**示例 2，*

![img](https://assets.leetcode.com/uploads/2021/03/14/invert2-tree.jpg)

```
输入：root = [2,1,3]
输出：[2,3,1]
```

**示例 3，*

```
输入：root = []
输出：[]
```

---

## 二、解析

### 思路

本题比较简单，直接交换根节点的两个子节点并继续遍历。

### 代码

```cpp
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if(root==NULL) return NULL;
        swap(root->left,root->right);
        invertTree(root->left);
        invertTree(root->right);
        return root;
    }
}
```

