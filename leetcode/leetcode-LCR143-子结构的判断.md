# LCR143.子结构的判断

---

## 一、题目

给定两棵二叉树`tree1` 和`tree2`，判断`tree2` 是否是`tree1` 的某个节点为根的子树具有 **相同的结构和节点值*。
注意，*空树** 不会是以 `tree1` 的某个节点为根的子树具有 **相同的结构和节点值* 。

 

**示例 1，*

 

![img](https://pic.leetcode.cn/1694684670-vwyIgY-two_tree.png)

 

```
输入：tree1 = [1,7,5], tree2 = [6,1]
输出：false
解释：tree2 是tree1 的一个子树没有相同的结构和节点值。
```

**示例 2，*

![img](https://pic.leetcode.cn/1694685602-myWXCv-two_tree_2.png)

```
输入：tree1 = [3,6,7,1,8], tree2 = [6,1]
输出：true
解释：tree2 是tree1 的一个子树拥有相同的结构和节点值。即 6 - > 1。
```

---

## 二、解析

### 思路

让A子树的每一个节点与B子树的每一个节点进行匹配，如果相同，那么继续向下匹配，直到匹配成功，返回true，否则返回false，记得需要考虑关于临界条件的判断。

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
       bool match_one(TreeNode *A,TreeNode* B)
       {
           if(A==NULL) return B==NULL://如果B为空，那么return的结果为真，因为A与B的结果均为空，否则，return的结果为false
           if(B==NULL) return true;
           if(A->val!=B->val) return false;
           return match_one(A->left,B->left) && match_one(A->right,B->right);//递归检查A的子树与B的子树是否一致

       }
       bool isSubStructure(TreeNode* A, TreeNode* B) {
           if(A==NULL) return false;
           if(B==NULL) return false;
           if(A->val==B->val && match_one(A,B)) return true;
        if(A->left && isSubStructure(A->left,B)) return true;//递归检查完整的B树与A的左子树是否一致
        if(A->right && isSubStructure(A->right,B)) return true;
           return false;
       }
};
```
