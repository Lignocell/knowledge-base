# 知识点文档库

这是一个以 Markdown 维护的个人技术知识库，记录 Java 后端、数据结构与算法、LeetCode、项目实践、面试题以及日常工具使用经验。

当前文档统一使用 UTF-8 编码，适合使用 Typora、Obsidian、VS Code 或其他 Markdown 编辑器阅读和维护。

## 内容目录

| 目录 | 内容 |
| --- | --- |
| `JavaSE` | Java 基础语法、面向对象、集合、异常、IO、反射、JVM 等 |
| `Java八股文` | Java 面试高频知识点和原理总结 |
| `JavaWeb` | Servlet、Cookie、Session、MyBatis、数据库、前端基础等 |
| `Spring` | Spring 核心、IOC、AOP、事务、源码和设计思想 |
| `SpringBoot` | Spring Boot 快速上手、配置、整合和项目实践 |
| `SpringMvc` | Spring MVC 请求处理、文件上传下载等 |
| `SpringSecurity` | 认证、授权、过滤器链和网络安全基础 |
| `数据结构` | 线性表、栈、队列、树、复杂度和其他基础结构 |
| `算法` | 排序、查找、贪心、递归、动态规划等算法笔记 |
| `leetcode` | LeetCode 题解和解题思路 |
| `Leetcode（Java）` | 使用 Java 编写的 LeetCode 题解 |
| `HZOJ` | HZOJ 在线题库题解 |
| `Project` | 项目开发、业务分析和工程实践记录 |
| `模拟面试` | 模拟面试问题和复盘记录 |
| `混` | Docker、Typora、指针等零散技术笔记 |
| `ainstec` | Ainstec 相关学习和实践资料 |
| `images` | 文档中使用的图片资源 |

## 推荐阅读顺序

如果从零开始学习，可以按下面的顺序阅读：

1. `JavaSE`：掌握 Java 基础语法和面向对象思想。
2. `数据结构`、`算法`：建立基本的数据结构和算法能力。
3. `leetcode`、`HZOJ`：通过题目巩固基础。
4. `JavaWeb`：理解 Web 请求、数据库和持久层。
5. `Spring`、`SpringBoot`、`SpringMvc`：进入 Java 后端工程开发。
6. `SpringSecurity`：补充认证、授权和安全知识。
7. `Project`、`模拟面试`、`Java八股文`：结合项目和面试进行复习。

## 本地使用

直接克隆仓库后，用 Markdown 编辑器打开即可：

```bash
git clone <仓库地址>
cd knowledge_point
```

推荐使用以下工具阅读：

- Typora：适合连续阅读和编辑 Markdown。
- Obsidian：适合建立知识点之间的双向链接。
- VS Code：适合搜索、批量修改和 Git 管理。

## 文档规范

- 所有 Markdown 文件使用 UTF-8 编码。
- 图片统一放在 `images` 或对应主题目录中，并使用相对路径引用。
- 文件名尽量使用清晰、稳定的中文标题；LeetCode 文件保留题号。
- 新增内容优先补充到已有分类，不要在根目录堆放临时文件。
- 代码示例注明语言类型，例如 ````java`、````cpp`、````sql`。
- 不要把密码、Token、私钥、数据库连接信息等敏感数据提交到仓库。
- 修改较大的章节时，使用清晰的 Git 提交信息，方便回滚和定位问题。

## 编码检查

提交前至少检查以下问题：

- 文件能否以严格 UTF-8 编码读取。
- 文档中是否出现 U+FFFD 替换字符。
- 是否出现典型的 GBK/UTF-8 混码残片。
- 图片链接和相对路径是否仍然有效。

建议在仓库中添加 `.editorconfig`，统一编辑器行为：

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
indent_style = space
indent_size = 2
```

## 发布建议

推荐采用下面的结构：

```text
GitHub 私有仓库
        |
        +-- GitHub Pages 或 Cloudflare Pages：发布文档站
        |
        +-- 掘金 / 知乎 / CSDN：同步精选文章，获取阅读流量
        |
        +-- 本地硬盘或 NAS：保留额外备份
```

GitHub 仓库作为唯一源文件和版本记录，发布平台只负责展示。这样即使博客站点出现问题，也可以从 Git 历史恢复任意版本。

## 初始化 Git 仓库

如果本地目录还没有有效的 Git 仓库，可以执行：

```bash
git init
git add .
git commit -m "docs: initialize knowledge base"
git branch -M main
git remote add origin https://github.com/<用户名>/<仓库名>.git
git push -u origin main
```

第一次发布前，建议先创建私有仓库，确认没有敏感信息后再改为公开仓库。

## 维护原则

- 原始 Markdown 是唯一可信来源，发布站点中的内容由仓库生成。
- 每次修复编码问题后立即提交，避免一次积累大量不可追踪修改。
- 大规模修改前建立 Git 提交点，不再依赖散落的手工备份目录。
- 定期执行 UTF-8 和乱码扫描，并检查图片链接。
- 重要版本使用 Git tag 标记，例如 `v1.0.0`。

## License

本仓库暂未指定统一开源许可证。转载或二次使用其中内容时，请保留原作者信息，并确认代码、图片和引用资料的来源许可。
