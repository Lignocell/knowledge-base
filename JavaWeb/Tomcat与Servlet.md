# Tomcat与Servlet

现在，我们正式进入后端开发。

## Tomcat

Tomcat就是一个典型的Web应用服务器软件，通过运行Tomcat服务器，我们就可以快速部署我们的Web项目，并交由Tomcat进行管理，我么们只需要直接通过浏览器访问我们的项目即可。

- bin目录：所有可执行文件，包括启动和关闭服务器的脚本。
- conf目录：服务器配置文件目录。
- lib目录：Tomcat服务器运行的一些依赖，不用关心。
- logs目录：所有的日志信息。
- temp目录：存放运行时产生的一些临时文件，不用关系。
- work目录：工作牡蛎，Tomcat会将jsp文件转换为Java文件（后面会将，这里暂时不提及）
- webapp目录：所有的Web项目都在这里，每个文件夹都是一个Web应用程序。

在了解了Tomcat之后，具体部署这里就不细讲了，接下来，我们来看如何创建一个Web项目

## 创建web项目

打开IDEA，新建项目，选择我们打开IDEA，新建一个项目，选择Jakarta EE（社区版没有此选项！）项目名称随便，项目模板选择Web应用程序，然后我们配置Web应用程序服务器，选择Tomcat即可。配置完成后，点击下一步即可，依赖项使用默认即可，然后点击完成，之后IDEA会自动帮助我们创建Maven项目。

我们可以将项目直接打包为war包（默认），打包好之后，放入webapp文件夹，就可以直接运行我们通过Java编写的Web应用程序了，访问路径为文件的名称。

## Servlet

前面我们已经完成了基本的环境搭建，那么现在我们就可以开始来了解我们的第一个重要类——Servlet。

它是Java EE的一个标准，大部分的Web服务器都支持此标准，包括Tomcat，就像之前的JDBC一样，由官方定义了一系列接口，而具体实现由我们来编写，最后交给Web服务器（如Tomcat）来运行我们编写的Servlet。

那么，它能做什么呢？我们可以通过实现Servlet来进行动态网页响应，使用Servlet，不再是直接由Tomcat服务器发送我们编写好的静态网页内容（HTML文件），而是由我们通过Java代码进行动态拼接的结果，它能够很好地实现动态网页的返回。

当然，Servlet并不专用于HTTP协议通信，也可用于其他的通信，但是一般都用于HTTP。

### 创建Servlet

那么，如何创建一个Servlet呢？很简单，实现Servlet类即可，并添加注解@WebServlet来进行注册。

```java
@WebServlert("/test")
public calss testServlet implements Servlet{
    
}
```

我们现在可以去访问页面：http://localhost:8080/test/test

我们发现，直接访问页面是没有内容的，大概是因为我们还没有为该请求方法编写实现，这里先不做讲解，后面详细介绍。

除了直接编写一个类，我们也可以在web.xml中进行注册，先将类上的@WebServlet的注解去掉：

```xml
<servlet>
    <servlet-name>test</servlet-name>
    <servlet-class>com.example.webtest.TestServlet</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>test</servlet-name>
    <url-pattern>/test</url-pattern>
</servlet-mapping>
```

这个方法也可以注册Servlet，但是显然直接使用注解更方便，因此之后我们一律使用注解进行开发，只有比较新的版本才支持此注解，老版本不支持。

实际上，Tomcat服务器会为我们提供一些默认的Servlet，也就是在服务器启动后，即使我们什么都不编写，Tomcat也自带了几个默认的Servlet，它们编写在conf目录下的web.xml中：

```xml
<!-- The mapping for the default servlet -->
    <servlet-mapping>
        <servlet-name>default</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>

    <!-- The mappings for the JSP servlet -->
    <servlet-mapping>
        <servlet-name>jsp</servlet-name>
        <url-pattern>*.jsp</url-pattern>
        <url-pattern>*.jspx</url-pattern>
    </servlet-mapping>
```

我们发现，默认的Servlet实际上可以帮助我们去访问一些静态资源，这也是为什么我们启动Tomcat服务器之后，能够直接访问webapp目录下的静态页面。

我们可以将之前编写的页面放入到webapp目录下，来测试一下是否能直接访问。

### 探究Servlet的生命周期

我们已经了解了如何注册一个Servlet，我们接下来看，Servlet是如何运行的。

首先我们需要来了解，Servlet中的方法各自是在什么时候被调用的，我们先来打印语句看看：

```java
public class TestServlet implements Servlet {

    public TestServlet(){
        System.out.println("我是构造方法！");
    }

    @Override
    public void init(ServletConfig servletConfig) throws ServletException {
        System.out.println("我是init");
    }

    @Override
    public ServletConfig getServletConfig() {
        System.out.println("我是getServletConfig");
        return null;
    }

    @Override
    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
        System.out.println("我是service");
    }

    @Override
    public String getServletInfo() {
        System.out.println("我是getServletInfo");
        return null;
    }

    @Override
    public void destroy() {
        System.out.println("我是destroy");
    }
}
```

启动服务器，访问我们定义的页面，然后关闭服务器，得到顺序：

> 我是构造方法！
>
> 我是init
>
> 我是service
>
> 我是service（出现两次是因为浏览器请求了2次，是因为第二次是请求favicon.ico，也就是获取图标，浏览器通病）
>
> 我是destroy

我们可以多次尝试访问此页面，但是init和构造方法只会执行一次，所有每次访问都会执行的是service方法，因此，一个Servlet的生命周期为：

- 首先执行构造方法完成Servlet初始化
- 调用init()方法
- 调用service()方法来处理客户端的请求
- Servlet销毁前调用destroy()方法
- 最后，Servlet是由JVM的垃圾回收器进行垃圾回收的。

现在我们发现，实际上在Web应用程序执行时，每当浏览器向服务器发起了一个请求时，都会创建一个线程执行一次service方法，来让我们处理用户的请求，并将处理结果响应给用户。

在service方法中，有两个参数，`ServletRequest`和`ServletResponse`，实际上，用户发起的HTTP请求，就被Tomcat服务器封装为一个ServletRequest，我们得到的其实是Tomcat服务器帮助我们创建的一个实现类，HTTP请求报文中的所有内容，都可以从ServletRequest对象中获取；同理，ServletResponse就是我们需要返回给浏览器的HTTP响应报文实体类封装。

那么我们再来看看ServletRequest中有哪些内容，我们可以获取请求的一些信息：

```java
@Override
public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
    //首先将其转换为HttpServletRequest（继承自ServletRequest，一般是此接口实现）
        HttpServletRequest request = (HttpServletRequest) servletRequest;
        
        System.out.println(request.getProtocol());  //获取协议版本
        System.out.println(request.getRemoteAddr());  //获取访问者的IP地址
  		  System.out.println(request.getMethod());   //获取请求方法
        //获取头部信息
        Enumeration<String> enumeration = request.getHeaderNames();
        while (enumeration.hasMoreElements()){
            String name = enumeration.nextElement();
            System.out.println(name + ": " + request.getHeader(name));
        }
}
```

我们发现，整个http请求报文中的所有内容，都可以通过HttpServletRequest对象来获取，当然，他的作用还有很多，后面一一讲解。

那么，我们再来看看ServletResponse，这个是服务端的响应内容，我们可以在这里填写我们想要发送浏览器显示的内容：

```java
//转换为HttpServletResponse
HttpServletResponse response=(HttpServletResponse)servletResponse;
//设定内容类型以及编码格式（普通HTML文本用text/html，之后会讲文件传输）
response.setHeader("Content-type","text/html;charset=UTF-8");
//获取Writer直接写入内容
response.getWriter().write("我是响应内容，);
//所有内容写入完成后，再发送给浏览器。
```

![点击查看源网页](https://oss.itbaima.cn/internal/markdown/2023/03/06/OpTzXU5b8VjkSiB.jpg)

### 解读和使用HttpServlet

前面，我们学习了如何创建，注册和使用Servelt，那么我们继续来深入学习Servlet接口的一些实现类。

首先Servlet有一个直接实现抽象类`GenericServlet`，我们来看看此类做了什么事情。

我们发现，这个类完善了配置文件读取和Servlet信息相关的操作，但是没有去实现service方法，因为此类仅仅用于完善一个Servlet的基本操作。

接着，我们来看HttpServlet，它是遵循HTTP协议的一种Servlet，继承自GenericServlet，他根据HTTP的协议规则，完善了service方法。

在阅读HttpServlet源码之后，我们发现，其实我们只需要继承HttpServlet来编写我们的Servlet就可以了，并且它已经帮助我们提前实现了一些操作，这样会给我们省去很多时间。

```java
@Log
@WebServlet("/test")
public class TestServlet extends HttpServlet{
    @Override
    prtected void doGet(HttpServletRequest req,HttpServletResponse resp) throws ServletException,IOException{
        resp.setContentType("text/html;charset=UTP-8");
        resp.getWriter().write("<h1>恭喜你</h1>");
    }
}
```

现在，我们只需要重写对应的请求方式，就可以快速完成Servlet的编写。

### @WebServlet注解详解

接着，我们来看看WebServlet注解，我们前面已经得知，可以快速使用此注解来注册一个Servlet，那么我们来看看其他的用法。

反编译WebServlet，name属性是Servlet名称，而urlPatterns和value实际上是同样功能，就是代表当前Servlet的访问路径，它不仅仅是一个固定值，还可以用通配符进行匹配：

```java
@WebServlet("/test/*")
```

上面的路径表示，所有test下的随便什么的路径名称，都可以访问Servlet。

也可以进行某个扩展名称的匹配：

```java
@WebServlet("*.js")
```

这样的话，获取任何以js结尾的文件，都会由我们自己定义的Servlet处理。

但，如果路径为`/`呢？

```java
@WebServlet("/")
```

此路径和Tomcat默认为我们提供的Servlet冲突，会直接替换掉默认的，改成我们自己的，意思是，如果没有找到匹配当前访问路径的Servlet，那么就会使用此Servlet进行处理。

我们还可以为Servlet配置多个访问路径：

```java
@WebServlet({"/test1","/test2"})
```

我们接着来看loadOnStartup属性，此属性决定了是否在Tomcat启动时就加载此Servlet，默认情况下，Servlet只有在被访问时才会加载，它的默认值为-1，表示不在启动时加载，我们可以将其修改为大于等于0的数来开启启动时加载。并且数字的大小决定了此Servlet的启动优先级。

```java
@Log
@WebServlet(value="/test",loadOnStartup=1)
public class TestServlet extends HttpServlet{
    @Override
    public void init()throws ServletException{
        super.init();
        log.info("我被初始化了");
    }
    @Override
    protected void doGet(HttpServletRrquest req,HttpServletResponse resp) throws ServletException,IOException{
        resp.setContentType("text/html;charset=UTP-8");
        resp.getWriter().write("<h1>恭喜你</h1>");
    }
}
```

其他内容都是Servlet的基本配置，这里不细讲了。

### 使用POST请求完成登录

我们前面已经了解了如何使用Servlet来处理HTTP请求，那么现在，我们结合一下前端，来实现登录操作。

我们需要修改一下Servlet，现在我们要让其能够接收一个POST请求：

```java
@Log
@WebServlet("/login")
public class LoginServlet extends HttpServlet{
    @Override
    protected void doPost(HttpServletRequest req,HttpServletResponse resp)throws ServletException,IOException{
        req.getParameterMap().forEach((k,v)->{
            System.out.println(k+":"+Arrays.toString(v));
        });
    }
}
```

ParameterMap存储了我们发送的POST请求所携带的表单数据，我们可以直接将其遍历查看，浏览器发送了什么数据。

现在修改前端：

```html
<body>
    <h1>登录到系统</h1>
    <form method="post" action="login">
        <hr>
        <div>
            <label>
                <input type="text" placeholder="用户名" name="username">
            </label>
        </div>
        <div>
            <label>
                <input type="password" placeholder="密码" name="password">
            </label>
        </div>
        <div>
            <button>登录</button>
        </div>
    </form>
</body>
```

method表示表单的提交方式，action指定表单提交的目标地址

通过修改form属性，现在我们点击登录按钮，会自动向后台发送一个POST请求。

运行服务器，测试后发现，在点击按钮后，确实向服务器发起了一个POST请求，并且携带了表单中文本框的数据。

现在，我们根据已有的基础，将其与数据库打通，我们进行一个真正的用户登陆操作，首先修改一下Servlet的逻辑：

```java
@Override
protected void doPost(HttpServletRequest req,HttpServletResponse resp) throws ServletException,IOException{
    resp.setContentType("text/html;charset=UTP-8");
    //获取POST请求携带的表单数据
    Map<String String[]>map=req.getParameterMap();
    //判断表单是否完整
    if(map.contain("usename") && map.containsKey("password")){
        String username=req.getParameter("username");
        String password=req.getParameter("password");
        
        try(SqlSession sq=factory.openSession(true)){  //自动保存
            UserMapper um=sq.getMapper(UserMapper.class);  //获取表单
            User user=um.getUser(username,password);  //提取表单用户
            if(user!=null){
                resp.getWriter().write("用户"+username+"登录成功");
            }else{
                resp.getWriter("您登录的用户密码不正确或此用户不存在");
            }
        }
    }else{
        resp.getWriter.write("错误，您的表单数据不完整，);
    }
}
```

接着，我们编写Myabtis的依赖和配置文件，创建一个表，用于存放我们的账号密码。

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="${驱动类（含包名）}"/>
                <property name="url" value="${数据库连接URL}"/>
                <property name="username" value="${用户名}"/>
                <property name="password" value="${密码}"/>
            </dataSource>
        </environment>
    </environments>
</configuration>
```

导入Mybatis和mysql依赖。

配置完成后，在我们的Servlet的init方法中编写Mybatis初始化代码，因为它只需要初始化一次。

```Java
SqlSessionFactory factory;
@SneakyThrows  //Lombok提供的注解，抛出受检异常，无需在方法中签名中声明throws
@Override
public void init() throws ServletExcetpion{
    factory=new SqlSessionFactoryBuilder().build(Resources.getResourceReader("mybatis.config.xml"));
    //读取文件内的内容
}
```

现在，我们创建一个实体类以及Mapper来进行用户信息查询：

```java
@Data
public class User{
    int id;
    String username;
    String password;
}
```

```java
public interface UserMapper{
    @Select("select * from user where username = #{username} and password =#{password}")
    User getUser(@aram("username") String username,@Param("password")String password);
}
```

```xml
<mappers>
    <mapper class="com.example.mapper.UserMapper"
</mappers>
```

然后就可以测试了。

### 上传和下载文件

首先，我们来看比较简单的下载文件，首先将我们的icon.png放入到resource文件夹中，接着我们编写一个Servlet用于处理文件下载：

```java
@WebServlet("/file")
public class FileServlet extends HttpServlet{
    @Override
    protected void doGet(HttpServletRequest req,HttpServletResponse resp) throws ServletException,IOException{
        resp.setContentType("image/png");
        OutputStream os=resp.getOutputStream();
        InputStream is=Resources.getResourceAsStream("icon.png");
    }
}
```

为了更快速的编写一个IO代码，我们可以引入一个工具库：

```xml
<dependency>
    <groupId>commons-io</groupId>
    <artifactId>commons-io</artifactId>
    <version>2.20.0</version>
</dependency>
```

由此，我们可以快速完成IO操作：

```java
@WebServlet("/file")
public class FileServlet extends HttpServlet{
    @Override
    protected void doGet(HttpServletRequest req,HttpServletResponse resp) throws ServletException,IOException{
        resp.setContentType("image/png");
        OutputStream os=resp.getOutputStream();
        InputStream is=Resources.getResourceAsStream("icon.png");
        IOUtils.copy(is,os);  //直接copy完成转换
    }
}
```

在前端页面添加一个链接，用于下载此文件：

```html
<hr>
<a href="icon.png" download="icon.png">点我下载高清资源</a>
```

href指定下载路径或者url，download指定下载文件的默认名称。

现在，我们学习上传文件。

首先编写前端部分：

```html
<form method="post" action="file" enctype="multipart/form-data">
     <div>
        <input type="file" name="test-file">
    </div>
    <div>
        <button>上传文件</button>
    </div>
</form>
```

注意必须添加enctype="multipart/form-data"，来表示此表单用于文件传输。

现在，我们修改一些Servlet代码：

```java
@MultipartConfig
@WebServlet("/file")
public class FileServlet extends HttpServlet{
    @Override
    protected void doPost(HttpServletRequest req,HttpServletResponse resp) throws ServletException,IOException{
        try(FileOutputStream stream = new FileOutputStream("/Users/nagocoler/Documents/test.png")){
            Part part = req.getPart("test-file");  //Part用于表示上传的文件，name属性填前端标签中的属性值
            IOUtils.copy(part.getInputStream(), stream);
            resp.setContentType("text/html;charset=UTF-8");
            resp.getWriter().write("文件上传成功，);
    }
  }
```

注意，必须添加`@MultipartConfig`注解来表示此Servlet用于处理文件上传的请求。

### 使用XHR请求数据

xhr本质上是XMLHttpRequest的缩写。

现在，我们希望网页中的部分内容可以动态显示，比如网页上有个时间，旁边有个按钮，点击按钮可以刷新当前时间。

这个时候就需要我们在页面展示时向后端发起请求了，并根据后端相应的结果，动态地更新页面中的内容，要实现此功能，就需要用到JS来帮助我们，首先，在js中编写我们的XHR请求，并在请求中完成动态更新：

```js
function updateTime(){
    let xhr=new XMLHttpRequest();  //专门用于在不刷新页面的情况下，向服务器发送请求并获取数据
    xhr.onreadystatechange=function(){
        if(xhr.readyState===4&&xhr.status===200){  //已经把数据返回&请求成功
            document.getElementById("time").innerText=xhr.responseTest  //根据time找到元素，然后显示文本内容，即显示内容就是responseTest
        }
    };
    xhr.open('GET','time',true);//true代表异步请求，即发送请求时浏览器不会卡住，可以滚动之类的操作；GET表示发送请求，time表示发送请求的地址
    xhr.send();
}
```

onreadystatechange表示一旦状态发生变化，立刻执行；为什么状态会发生变化呢，因为从浏览器发请求到服务器返回数据是需要时间的，当请求状态变化为数据已经发送成功时，自动执行后续操作。

`xhr.readyState`是请求的 "状态码"，有 5 种可能的值：

- 0：请求还没初始化（刚创建对象，还没调用`open()`）
- 1：请求已建立（调用了`open()`，但还没`send()`）
- 2：请求已发送（调用了`send()`，服务器开始接收）
- 3：服务器正在返回数据（部分数据已收到）
- 4：服务器已返回全部数据（请求完成）

`xhr.status`是服务器返回的"结果码"，类似生活中的"状态提示码"

- 200：成功（服务器正常返回数据）
- 404：找不到（请求的地址错了，服务器没有这个资源）
- 500：服务器出错（服务器自己出问题了）

接着，修改前端页面，添加一个时间显示区域：

```html
<hr>
<div id="time"></div>
<br>
<button onclick="updateTime()">  //按钮点击事件，点击后执行函数
    更新数据
</button>
<script>
    updatetTime()  //当页面加载完成后，自动执行一次updateTime()函数，这样页面一打开就会显示时间，而不需要用户先点击按钮。
</script>
```

最后，创建一个Servlet用于处理时间更新请求：

```java
@WebServlet("/time")
public class TimeServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy年MM月dd日HH:mm:ss");
        String date = dateFormat.format(new Date());
        resp.setContentType("text/html;charset=UTF-8");
        resp.getWriter().write(date);
    }
}
```

### 重定向与请求转发

当我们希望用户登录完成后，自动跳转到网站首页，这个时候，需要重定向来完成。当浏览器收到一个重定向的响应时，会按照重定向响应给出的地址，再次向此地址发出请求。

实现重定向，只需要调用一个方法即可，我们修改一下登录成功后执行的代码：

```java
resp.sendRedirect("https://www.baidu.com");
```

调用后，响应的状态码会被设置为302，并且响应头中添加了一个Location属性，此属性表示，需要重定向到哪一个网址。

现在，如果我们成功登录，那么服务器会发送给我们一个重定向响应，这时，我们的浏览器会去请重新请求另一个网址，这样，就可以实现跳转了。

那么我们接着看请求转发，请求转发是一种服务器内部的跳转机制，我们知道，重定向会使得浏览器去重新请求一个页面，而请求转发则是服务器内部进行跳转，它的目的是，直接将本次请求转发给其他Servlet进行处理，并由其他Servlet来返回结果，因此它是在进行内部的转发。（也就是说，你去政务大厅办业务（发送请求），窗口 A 的工作人员看了你的材料后说：" 这个业务不归我管，我直接把你的材料转给窗口 B（`/time`），你在这等着就行，不用重新排队，最后由窗口 B 直接给你结果 "。）

```java
req.getRequestDispatcher("/time").forward(req,resp);
```

只发送了一次请求，不跳转到其他网址或者其他Web应用程序。

接着，我们看看下面这个例子。

当进行登录操作时，我们发现，返回一个405界面，表示我们的请求被另一个Servlet处理，并且请求的信息全部被转交给另一个Servlet，由于此Servlet不支持POST请求，因此返回405。

那么也就是说，该请求包括请求参数一起被传递了，那么我们可以尝试给Servlet B添加POST请求：

```java
@Override
protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    this.doGet(req, resp);  // 把POST请求交给GET处理
}
```

那么，请求转发有什么好处呢？它可以携带数据：

```java
req.setAttribute("test", "我是请求转发前的数据");
req.getRequestDispatcher("/time").forward(req, resp);
```

```java
System.out.println(req.getAttribute("test"));
```

通过`setAttribute`方法来给当前请求添加一个附加数据，在请求转发后，我们可以直接获取到该数据。

重定向属于二次请求，因此无法使用这种方式来传递数据，那么，如何在重定向之间传递数据呢？我们可以使用即将要介绍的ServletContext对象。

最后总结，两者的区别为：

- 请求转发是一次请求，重定向是两次请求
- 请求转发地址栏不会发生改变， 重定向地址栏会发生改变
- 请求转发可以共享请求参数 ，重定向之后，就获取不了共享参数。
- 请求转发只能转发给内部的Servlet

### ServletContext对象

ServletContext全局唯一，它是属于整个Web程序的，我们可以通过getServletContext()来获取此对象。

此对象也能设置附加值：

```java
ServletContext context = getServletContext();
context.setAttribute("test", "我是全局共享的数据");
//不管是重定向还是转发，其他地方都能拿到
resp.sendRedirect("time");
```

```java
System.out.println(getServletContext().getAttribute("test"));
```

因为无论如何，获取到的ServletContext始终是一个对象，因此我们可以随时随地获取我们添加的属性。

它不仅仅可以用来进行数据传递，还可以做一些其他的事情，比如请求转发：

```java
context.getRequestDispatcher("/time").forward(req, resp);
```

它还可以获取根目录下的资源文件（注意是webapp根目录下的，不是resource中的资源）

### 初始化参数

初始化参数类似于初始化配置需要的一些值，比如我们的数据库连接相关信息，就可以通过初始化参数来给予Servlet，或是一些其他的配置项。

我们先给Servlet添加一些初始化参数：

```java
@WebServlet(value="/login" initParams={
    @WebInitParam(name="test",value="我是一个默认的初始化参数);
})
```

它是以键值对形式保存的，我们可以直接通过Servlet的getInitParameter方法获取：

```java
System.out.println(getInitPatameter("test"));
```

但是，这里的初始化参数仅仅是针对于Servlet，我们也可以定义全局初始化参数，只需要在web.xml编写即可：

```xml
<context-param>
    <param-name>lbwnb</param-name>
    <param-value>我是全局初始化参数</param-value>
</context-param>
```

我们需要使用ServletContext来读取全局初始化参数：

```java
ServletContext context = getServletContext();
System.out.println(context.getInitParameter("lbwnb"));
```

有关ServletContext其他的内容，我们需要完成后面内容的学习才能理解。
