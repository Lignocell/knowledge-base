# 102.二叉树的层序遍历

---

## 一、题目

给你二叉树的根节点`root` ，返回其节点值的 **层序遍历** 。（即逐层地，从左到右访问所有节点）。

 

**示例 1，*

![img](https://assets.leetcode.com/uploads/2021/02/19/tree1.jpg)

```
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]
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

有关二叉树的深度遍历与层序遍历我在树的章节写过，在此就不过多赘述了。

#### 方法一：广度遍历

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
    vector<vector<int>> levelOrder(TreeNode* root) {
        if(root==NULL) return;
        vector<vector<int>>ans;//创建一个二维数组的容器
        queue<TreeNode*>q;
        TreeNode*node;
        q.push(root);//先将根节点压入队列中
        while(!q.empty())
        {
            int n=q.size();//获取当前队列中节点的数量，表示这一层的节点数
            vector<int>temp;//创建一个临时变量来存储节点
            for(int i=0;i<n;i++)//遍历当前层的所有节点
            {
                node=q.front();//将q的队首赋值给node
                temp.push_back(root->val);
                if(node->left) q.push(node->left);//层序遍历左子树
                if(node->right) q.push(node->right);//层序遍历右子树
                q.pop();//删除节点
            }
            ans.push_back(temp);
        }
        return ans;
    }
};
```

#### 方法二：深度遍历（用栈的方式完成层序遍历）

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
    
    void dfs(TreeNode*root,int k,vector<vector<int>>&ans)//k表示层级
        //在二叉树中，如果k与ans的大小相等，证明k所指向的这一层还没有节点进入ans 中
    {
        if(root==NULL) return;
        if(k==ans.size()) ans.push_back(vector<int>());//当if条件成立，创建一个空容器存放每一层节点
        ans[k].push_back(root->val);
        dfs(root->left,k+1,ans);
        dfs(root->right,k+1,ans);
        return;

    }
    
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>>ans;
        dfs(root,0,ans);
        return ans;
    }
};
```
