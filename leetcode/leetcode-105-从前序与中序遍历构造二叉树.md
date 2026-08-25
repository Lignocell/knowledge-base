# 105.从前序与中序遍历构造二叉树

---

## 一、题目

给定两个整数数组 `preorder` 和`inorder`，其中`preorder` 是二叉树的*先序遍历**，`inorder` 是同一棵树的*中序遍历**，请构造二叉树并返回其根节点。

 

**示例 1:**

![img](https://assets.leetcode.com/uploads/2021/02/19/tree.jpg)

```
输入: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
输出: [3,9,20,null,null,15,7]
```

**示例 2:**

```
输入: preorder = [-1], inorder = [-1]
输出: [-1]
```

---

## 二、解析

通过前序遍历与中序遍历还原二叉树我在二叉树的遍历与线索化中已经写到了，这里就不过多赘述了。

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left),
 * right(right) {}
 * };
 */
class Solution {
public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        if(preorder.size()==0) return NULL;
        int pos=0,n=preorder.size();
        while(preorder[0]!=inorder[pos]) pos++;//定位pos的位置，让pos指向中序遍历的根节点所在的                                                 位置
        vector<int>prearr,inarr;
        TreeNode*root=new TreeNode(preorder[0]);//创建根节点
        //根据前序遍历与中序遍历的结果，将左子树提取出来，赋值给prearr和inarr，然后构建root的左子树。
        for(int i=1;i<=pos;i++) prearr.push_back(preorder[i]);//前序遍历的左子树从1到pos
        for(int i=0;i<=pos-1;i++) inarr.push_back(inorder[i]);//中序遍历的左子树从0到pos-1
        root->left=buildTree(prearr,inarr);
        prearr.clear();
        inarr.clear();

        for(int i=pos+1;i<n;i++) prearr.push_back(preorder[i]);
        for(int i=pos+1;i<n;i++) inarr.push_back(inorder[i]);
        root->right=buildTree(prearr,inarr);
        return root;
    }
};
```
