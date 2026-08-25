# Thymeleaf

虽然JSP为我们提供了便捷，但是缺点显而易见，那么，有没有那种即能实现模板，又能实现前后端分离的模板引擎呢：

Thymeleaf（百里香叶）是一种适合Web和独立环境的现代化服务端Java模板引擎，官方文档：https://www.thymeleaf.org/documentation.html。

那么，它与JSP相比，好在哪里呢，我们来看官网给出的例子：

```html
<table>
  <thead>
    <tr>
      <th th:text="#{msgs.headers.name}">Name</th>
      <th th:text="#{msgs.headers.price}">Price</th>
    </tr>
  </thead>
  <tbody>
    <tr th:each="prod: ${allProducts}">
      <td th:text="${prod.name}">Oranges</td>
      <td th:text="${#numbers.formatDecimal(prod.price, 1, 2)}">0.99</td>
    </tr>
  </tbody>
</table>
```

我们可以在前端页面中填写占位符，而这些占位符的实际值则是由后端进行提供，这样，我们就不用再像JSP那样前后端都写在一起了。

我们来创建一个例子感受一下，首先还是新建项目，注意创建时勾选Thymeleaf依赖。

编写一个前端页面，名称为test.html，注意，是放在resource目录下，在html标签内部添加`xmlns:th=“http://www.thymeleaf.org”`，引入Thymeleaf定义的标签属性：

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <div th:text="${title}"></div>
</body>
</html>
```

接着，我们编写一个Servlet作为默认界面：

```java
@WebServlet("/index")
public class HelloServlet extends HttpServlet {

    TemplateEngine engine;  //引擎模板对象
    @Override
    public void init() throws ServletException {
        engine = new TemplateEngine();
        //类加载模板解析器，主要用于找到我们写的HTML模板文件
        ClassLoaderTemplateResolver r = new ClassLoaderTemplateResolver();  
        engine.setTemplateResolver(r);  //将解析器放入对应的模板内
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Context context = new Context();
        context.setVariable("title", "我是标题");  //将html中用到title的地方替换为我是标题
        engine.process("test.html", context, resp.getWriter());
        //1.找模板
        //2.填数据：将context填入进去
        //3.返回结果：生成对应的html文件后，通过resp.getWriter()把内容写到响应中，发送给浏览器。
    }
}
```

我们发现，浏览器得到的页面，就是已经经过模板引擎解析好的页面，而我们的代码依然是后端处理数据，前端展示数据，因此使用Thymeleaf就能使得当前Web程序的前后端划分更清晰。

虽然Thymeleaf在一定程序上分离了前后端，但是其依然是在后台渲染HTML页面并发送给前端，并不是真正意义上的前后端分离。

## Thymeleaf语法基础

那么，如何使用Thymeleaf呢？

首先我们看看后端部分，我们需要通过TemplateEngine对象来将模板文件渲染为最终的HTML文件：

```java
TemplateEngine engine;
@Override
public void init() throws ServletException{
    engine=new TemplateEngine();
    ClassLoaderTemplateResolver r=new ClassLoaderTemplateResolver();
    engine.setTemplateResolver(r);
}
```

此对象只需要创建一次，以后就可以一直使用了。接着，我们来看看如何使用模板引擎进行解析：

```java
@Override
protected void doGet(HttpServletRequest req, HttpServeltResponse resp) throws ServletException,IOException{
    //创建上下文，上下文中包含了所有需要替换到模板的内容
        Context context = new Context();
        context.setVariable("title", "我是标题");  //将html中用到title的地方替换为我是标题
        engine.process("test.html", context, resp.getWriter());
}
```

接下来，我们就可以在前端页面通过上下文提供的内容，将Java数据解析到前端页面。

接着，我们来了解Thymeleaf如何为普通的标签添加内容，比如：

```html
<div th:text="${title}"></div>
```

我们使用了th:text来为当前标签指定内部文本，注意任何内容都会变成普通文本，即使传入了一个HTML代码，如果我希望向内部添加一个HTML文本呢？我们可以使用th：utext属性：

```html
<div th:utext="${title}"></div>
```

并且，传入的title属性，不仅仅只是一个字符串的值，而是一个字符串的引用，我们可以直接通过此引用调用相关的方法：

```html
<div th:text="${title.toLowerCase()}"></div>
```

除了替换文本，他还支持替换一个元素的任意属性，我们发现，th:能够拼接几乎所有的属性，一旦使用`th:属性名称`，那么属性的值就可以通过后端提供了，比如我们现在想替换一个图片的链接：

```java
@Override
protected void doGet(HttpServletRequest req, HttpServeltResponse resp) throws ServletException,IOException{
    Context context=new Context();
    context.setVariable("url","http://n.sing.cn/123343453.jpg");  //向容器内添加url图片地址
    context.seVariable("alt","图片加载失败);  //如果加载不出来，替换为。。。
    engine.process("test.html",context,resp.getWriter());
}
```

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <img width="700" th:src="${url}" th:alt="${alt}">
</body>
</html>
```

现在访问我们的页面，就可以看到替换后的结果了。

Thymeleaf还可以进行算术运算，几乎Java中的运算都支持：

```html
<div th:text="${value % 2}"></div>
```

同样的，它还支持三元运算：

```html
<div th:text="${value % 2 == 0 ? 'yyds' : 'lbwnb'}"></div>
```

多个属性也可以通过`+`进行拼接，就像Java中的字符串拼接一样，这里要注意一下，字符串不能直接写，要添加单引号：

```html
<div th:text="${name}+' 我是文本 '+${value}"></div>
```

## Thymeleaf流程控制语法

除了一些基本操作，我们还可以使用Thymeleaf来处理流程控制语句，当然，不是直接编写Java代码的形式，而是添加一个属性即可。

首先我们来看if语句，如果if条件满足，则标签留下，如果不满足，则标签被自动移除：

```java
@Override
protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    Context context = new Context();
    context.setVariable("eval", true);  //false时标签不显示给用户
    engine.process("test.html", context, resp.getWriter());
}
```

```html
<div th:if="${eval}">
    我是判断条件的标签
</div>
```

th:if会根据其中传入的值或是条件表达式的结果进行判断，只有满足的情况下，才会显示此标签，具体的判断规则如下：

- 如果值不是空：
	- 如果值是布尔值并且为true。
	- 如果值是一个数字，并且不为0
	- 如果值是一个字符，并且不为0
	- 如果值是一个字符串，并且不是“错误”，“关闭”，“否”。
	- 如果值不是布尔值、数字、字符或字符串。
- 如果值为空，th:if将计算为false

th:if还有一个相反的属性th:unless，效果完全相反，这里不解释了。

我们接着来看多分支条件判断，我们可以使用th:switch属性来实现：

```html
<div th:switch="${eval}">
    <div th:case="1">
        我是1
    </div>
    <div th:case="2">
        我是2
    </div>
    <div th:case="3">
        我是3
    </div>
</div>
```

只不过没有default属性，我们可以使用th:case="*"代替：

```html
<div th:case=th:case="*"我是Default</div>
```

最后，我们来看看如何实现遍历，假如我们有一个存放书籍信息的List需要显示，那么如何快速生成一个列表呢？我们可以使用th:each来进行遍历操作：

```java
@Override
protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    Context context = new Context();
    context.setVariable("list", Arrays.asList("伞兵一号的故事", "倒一杯卡布奇诺", "玩游戏要笑着哭", "十七张牌前的电脑屏幕"));
    engine.process("test.html", context, resp.getWriter());
}
```

```html
<ul>
    <li th:each="title : ${list}" th:text="'。+${title}+'。"></li>
</ul>
```

th:each中需要填写单个元素名称：${列表}，这样，所有的列表项都可以使用遍历的单个元素，只要使用了th:each，都会被循环添加。因此最后生成的结果为：

```html
<ul>
        <li>《伞兵一号的故事》/li>
        <li>《倒一杯卡布奇诺》/li>
        <li>《玩游戏要喵着玩》</li>
        <li>《十七张牌前的电脑屏幕》/li>
    </ul>
```

我们还可以获取当前循环的迭代状态，只需要在最后添加`iterStat`即可，从中可以获取很多信息，比如当前的顺序：

```html
<ul>
    <li th:each="title, iterStat : ${list}" th:text="${iterStat.index}+'.。+${title}+'。"></li>
</ul>
```

状态变量在`th:each`属性中定义，并包含以下数据：

- 当前*迭代索引*，以0开头。这是`index`属性。
- 当前*迭代索引*，以1开头。这是`count`属性。
- 迭代变量中的元素总量。这是`size`属性。
- 每个迭代中的迭代变量*。这是`current`属性。
- 当前迭代是偶数还是奇数。这些是`even/odd`布尔属性。
- 当前迭代是否是第一个迭代。这是`first`布尔属性。
- 当前迭代是否是最后一个迭代。这是`last`布尔属性。

通过了解了流程控制语法，现在我们就可以很轻松地使用Thymeleaf来快速替换页面中的内容了。

## Thymeleaf模板布局

在某些网页中，我们会发现，整个网站的页面，除了中间部分的内容会随着我们的页面跳转而变化外，有些部分是一直保持一个状态的，比如我们打开b站，我们翻动评论或者切换视频的时候，变化的只是对应区域内容，实际上，其他地方的内容无论内部页面如何跳转，都不会改变。

Thymeleaf就可以轻松实现这样的操作，我们只需要将不会改变的地方设定为模板布局，并在不同的页面中插入这些模板布局，就无需每个页面都去编写同样的内容了。现在我们来创建两个页面：

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <div class="head">
        <div>
            <h1>我是标题内容，每个页面都</h1>
        </div>
        <hr>
    </div>
    <div class="body">
        <ul>
            <li th:each="title, iterStat : ${list}" th:text="${iterStat.index}+'.。+${title}+'。"></li>
        </ul>
    </div>
</body>
</html>
```

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <div class="head">
        <div>
            <h1>我是标题内容，每个页面都</h1>
        </div>
        <hr>
    </div>
    <div class="body">
        <div>这个页面的样子是这样</div>
    </div>
</body>
</html>
```

接着，将模板引擎写成工具类的形式：

```java
public class ThymeleafUtil{
    private static final TemplateEngine engine;
    static{
        engine=new TemplateEngine();
        ClassLoaderTemplateResolver r=new ClassLoaderTemplateResolver();
        engine.setTemplateResolver(r);
    }
    public static TemplateEnfine getEngine(){
        return engine;
    }
}
```

```java
@WebServlet("/index2")
public class HelloServlet2 extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Context context = new Context();
        ThymeleafUtil.getEngine().process("test2.html", context, resp.getWriter());
    }
}
```

现在就有两个Servlet分别对应两个页面了，但是这两个页面实际上是存在重复内容的，我们要做的就是将这些重复内容提取出来。

我们单独编写一个`head.html`来存放重复部分：

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="en">
<body>
    <div class="head" th:fragment="head-title"> 
        <div>
            <h1>我是标题内容，每个页面都</h1>
        </div>
        <hr>
    </div>
</body>
</html>
```

 fragment是复用代码核心属性，给当前标签head起了一个唯一标识head-title，表示这个代码可以被其他页面复用。

现在，我们就可以直接将页面中的内容快速替换：

```html
<div th:include="head.html::head-title"></div>
<div class="body">
    <ul>
        <li th:each="title, iterStat : ${list}" th:text="${iterStat.index}+'.。+${title}+'。"></li>
    </ul>
</div>
```

我们可以使用insert，replace，include(include已过时，建议使用insert)三种方法进行页面内容替换，那么有什么区别呢：

- `th:insert`最简单：它只会插入指定的片段作为标签的主体。
- `th:replace`实际上将标签直接*替换*为指定的片段。
- `th:include`和`th:insert`相似，但它没有插入片段，而是只插入此片段*的内容

它还支持参数传递，比如我们现在希望插入二级标题，并且由我们的子页面决定：

```html
<div class="head" th:fragment="head-title">
    <div>
        <h1>我是标题内容，每个页面都</h1>
        <h2>我是二级标题</h2>
    </div>
    <hr>
</div>
```

稍加修改，就像JS那样添加一个参数名称：

```html
<div class="head" th:fragment="head-title(sub)">
    <div>
        <h1>我是标题内容，每个页面都</h1>
        <h2 th:text="${sub}"></h2>
    </div>
    <hr>
</div>
```

sub是参数名，类似于形参。

现在直接在替换位置添加一个参数即可：

```html
<div th:include="head.html::head-title('这个是第1个页面的二级标题')"></div>
<div class="body">
    <ul>
        <li th:each="title, iterStat : ${list}" th:text="${iterStat.index}+'.。+${title}+'。"></li>
    </ul>
</div>
```

这样，不同的页面还有着各自的二级标题。
