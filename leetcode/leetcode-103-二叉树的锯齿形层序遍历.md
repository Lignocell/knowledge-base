# 103. 二叉树的锯齿形层序遍遍历

----

## 一、题目

给你二叉树的根节点`root`，返回其节点值的 **锯齿形层序遍历**。（即先从左往右，再从右往左进行下一层遍历，以此类推，层与层之间交替进行）。

 

**示例 1，*

![img](https://assets.leetcode.com/uploads/2021/02/19/tree1.jpg)

```
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[20,9],[15,7]]
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

先将二叉树进行遍历，然后存放进数组中，然后对偶数层进行遍历，将数组中存放的数据进行翻转。

### 代码

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
      void dfs(TreeNode*root,int k,vector<vector<int>>&ans)//遍历数组
      {
          if(root==NULL) return NULL;
          if(k==ans.size()) ans.push_back(vector<int>());//当k与ans的大小相同时，证明数组中没有空位置添加元素，现需要开辟新元素
          ans[k].push_back(root->val);
          dfs(root->left,k+1,ans);
          dfs(root->right,k+1,ans);
          return;

      }
     vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
         vector<vector<int>>ans;
         dfs(root,0,ans);//先将二叉树存放如ans 中
         for(int k=1;k<ans.size();k+=2)//遍历奇数层
         {
             for(int i=0,j=ans[k].size()-1;i<j;i++,j--)
             {
                 swap(ans[k][i],ans[k][j]);//将第k层的i号数据与j号数据交换

             }
         }
     }
};
```

