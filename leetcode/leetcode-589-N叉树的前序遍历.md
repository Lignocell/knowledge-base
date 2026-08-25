# 589.N叉树的前序遍历

---

## 一、题目

给定一棵n 叉树的根节点 `root` ，返回*其节点值的 **前序遍历*** 。

n 叉树 在输入中按层序遍历进行序列化表示，每组子节点由空值`null` 分隔（请参见示例）。


**示例 1，*

![img](https://assets.leetcode.com/uploads/2018/10/12/narytreeexample.png)

```
输入：root = [1,null,3,2,4,null,5,6]
输出：[1,3,5,6,2,4]
```

**示例 2，*

![img](https://assets.leetcode.com/uploads/2019/11/08/sample_4_964.png)

```
输入：root =[1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
输出：[1,2,3,6,7,11,14,4,8,12,5,9,13,10]
```

---

## 二、解析

前序遍历的方法课参考二叉树的遍历与线索化，我在这里就不过多赘述了。

#### 方法一：

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    vector<Node*> children;

    Node() {}

    Node(int _val) {
        val = _val;
    }

    Node(int _val, vector<Node*> _children) {
        val = _val;
        children = _children;
    }
};
*/

class Solution {
public:
     vector<int> preorder(Node* root) {
    if(root==NULL) return vector<int>();//首先如果子节点为空，那么返回空容器。
         vector<int>ans;//建立一个容器数组
         ans.push_back(root->val);//先将根节点压入到容器中
         for(auto x:root->children)//遍历root的子节点，让x等于root的子节点
        {
             vector<int>temp=preorder(x);//递归调用子节点，并赋值给temp
             for(auto y:temp) ans.push_back(y);//将temp的结果赋值给y，并压入到容器中
        } 
         return ans;
     }
};
```

#### 方法二：

两层封装，相较于方法一节省时间

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    vector<Node*> children;

    Node() {}

    Node(int _val) {
        val = _val;
    }

    Node(int _val, vector<Node*> _children) {
        val = _val;
        children = _children;
    }
};
*/

class Solution {
public:
    
void __preorder(Node* root,vector<int>&ans)//记得这里是引用ans
    {
     if(root==NULL) return;
    ans.push_back(root->val);
    for(auto x:root->children)
    {
        __preorder(x,ans);
    }
    return;
}
    
     vector<int> preorder(Node* root) {
         vector<int>ans;
         __preorder(root,ans);
         return ans;
     }
}：
```

