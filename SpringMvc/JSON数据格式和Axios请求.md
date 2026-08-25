# JSON数据格式和Axios请求

JSON (JavaScript Object Notation, JS 对象简称 是一种轻量级的数据交换格式。

我们现在推崇的是前后端分离的开发模式，而不是所有内容全部交给后端渲染再交给浏览器，也就是说，整个Web页面的内容在一开始就编写完成了，而其中的数据由前端执行JS代码向服务器动态获取，再到前端进行渲染（填充），这样可以大幅度减少后端压力，后端只需要传输关键数据即可（在即将到来的SpringBoot阶段，我们将完全采用前后端分离的开发模式）。

## JSON数据格式

既然要实现前后端分离，那么我们就必须约定一种更高效的数据传输模式，来向前端页面传输后端提供的数据。因此JSON横空出世，它非常容易理解，并且前端的兼容性更好，因此现在主流的数据传输方式都是通过JSON格式承载的。

一个JSON格式长这样，以学生对象为例：

```json
{"name":"小明","age":18}
```

多个学生可以用数组进行表示：

```json
[{"name": "杰哥", "age": 18}, {"name": "阿伟", "age": 18}]
```

嵌套关系可以表示为：

```json
{"studentList":[{"name": "杰哥", "age": 18}, {"name": "阿伟", "age": 18}],"count":2}
```

它直接包含了属性的名称和属性的值，它与JS的对象结尾相似，它到达前端后，可以直接转化为对象，以对象的形式进行操作和内容的读取，相当于以字符串形式表示了一个JS对象，我们可以直接在控制台窗口进行测试：

```js
let obj = JSON.parse('{"studentList": [{"name": "杰哥", "age": 18}, {"name": "阿伟", "age": 18}], "count": 2}')
//将JSON格式字符串转换为JS对象
obj.studentList[0].name   //直接访问第一个学生的名称
```

我们同样可以将JS转化为JSON字符串：

```js
JSON.stringify(obj)
```

我们后端就可以以JSON字符串的形式向前端传送数据，这样前端拿到数据以后，就可以快速获取，非常方便。

那么我们如何在后端快速创建一个JSON格式的数据呢？我们导入以下依赖：

```xml
<dependency>
      <groupId>com.alibaba.fastjson2</groupId>
      <artifactId>fastjson2</artifactId>
      <version>2.0.34</version>
</dependency>
```

JSON解析框架有很多种，比较常用的是Jackson和FastJSON，这里我们使用阿里巴巴的FastJSON进行解析，这是目前号称最快的JSON解析框架，并且现在已经强势推出FastJSON 2版本。

首先我们介绍的是JSONObject，它和Map的使用方法一样，并且是有序的（实现了LinkedHashMap接口），比如我们向其中存放几个数据：

```java
@RequsetMapping(value="/index")
public Srting index(){
    JSONObject object=new JSONObject();
    object.put("name", "杰哥");
    object.put("age", 18);
    Sytem.out.println(object.toJSONString());   //以JSON格式输出JSONObject字符串
    return "index";
}
```

最后我们得到的结果为：

```json
{"name": "杰哥", "age": 18}
```

实际上JSONObject就是对JSON数据的一种对象表示。同样还有JSONArray，它表示一种数组，用法和List一样，数组中可以嵌套其他的JSONObject和JSONArray：

```java
@RequestMapping(value = "/index")
public String index(){
    JSONObject object = new JSONObject();
    object.put("name", "杰哥");
    object.put("age", 18);
    JSONArray array = new JSONArray();
    array.add(object);
    System.out.println(array.toJSONString());
    return "index";
}
```

结果如下：

```json
[{"name": "杰哥", "age": 18}]
```

当出现循环引用时，会按照以下语法来解析：

![img](https://oss.itbaima.cn/internal/markdown/2023/08/14/MjO4awH3X1YnlmR.png)



我们可以也直接创建一个实体类，将实体类转换为JSON格式的数据：

```java
@RequestMapping(value = "/index", produces = "application/json")
@ResponseBody
public String data(){
    Student student = new Student();
    student.setName("杰哥");
    student.setAge(18);
    return JSON.toJSONString(student);
}
```

这里我们修改了produce的值，将返回的内容设定为application/json，表示服务端返回了一个JSON格式的数据（当然不设置也行，也能展示，这样是为了规范）然后我们在方法上添加了@ResponseBody表示方法返回（也可以在类上添加@RestController表示此Controller默认返回的是字符串数据）的结果不是视图名称而是直接返回一个字符串作为页面数据，这样，返回给浏览器的就是我们直接返回的字符串内容。

@RestController = @Controller + @ResponseBody

接着，我们使用JSON工具类将其转换为JSON格式的字符串，打开浏览器，得到JSON数据。

SpringMVC非常智能，我们可以直接返回一个对象类型，他会自动转换为JSON字符串格式：

```java
@RequestMapping(value = "/data", produces = "application/json")
@ResponseBody
public Student data(){
    Student student = new Student();
    student.setName("杰哥");
    student.setAge(18);
    return student;
}
```

注意需要在配置类中添加一下FastJSON转换器，这里需要先添加一个依赖：

```xml
<dependency>
    <groupId>com.alibaba.fastjson2</groupId>
    <artifactId>fastjson2-extension-spring6</artifactId>
    <version>2.0.34</version>
</dependency>
```

然后编写配置：

```java
@Override
public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
    converters.add(new FastJsonHttpMessageConverter());
}
```

再次尝试，内容就会自动转换为JSON格式响应给客户端了。

## Axios异步请求

前面我们已经讲解了如何向浏览器发送一个JSON格式的数据，那么我们现在来看看如何向浏览器请求数据。

![img](https://oss.itbaima.cn/internal/markdown/2023/08/14/faYcVC6dpIOuJyA.png)

这一部分，我们又要回到前端的相关内容介绍，当然，我们仅仅作为了解，并不需要详细学习前端项目开发知识。

前端为什么要用到异步请求，这是因为我们的网页是动态的（这里的动态不是指有动画效果，而是能够实时更新数据）比如我们点击一个按钮会弹出新的内容、或是跳转到新的页面、更新页面中的数据等等，这些都需要通过JS完成异步请求来实现。

> 前端异步请求指的是在前端中发送请求至服务器或其他资源，并且不阻塞用户界面或其他操作。在传统的同步请求中，当发送请求时，浏览器会等待服务器响应，期间用户无法进行其他操作。而异步请求通过将请求发送到后台，在等待响应的同时，允许用户继续进行其他操作。这种机制能够提升用户体验，并且允许页面进行实时更新。常见的前端异步请求方式包括使用XMLHttpRequest对象、Fetch API、以及使用jQuery库中的AJAX方法，以及目前最常用的Axios框架等。

假如我们后端有一个实时刷新的数据（随时间的变化）现在需要在前端实时更新展示，这里我们以Axios框架的简单使用作为例子，来体验如何发起异步请求并更新我们页面的数据。

首先是前端页面，直接抄作业就行：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>测试</title>
    <script src="https://unpkg.com/axios@1.1.2/dist/axios.min.js"></script>
</head>
<body>
  <p>欢迎来到GayHub全球最大同性交友网站</p>
  <p>用户名 <span id="username"></span></p>
  <p>密码: <span id="password"></span></p>
</body>
</html>
```

接着我们使用axios框架直接对后端请求JSON数据：

```html
<script>
    function getInfo() {
        axios.get('/mvc/test').then(({data}) => {
            document.getElementById('username').innerText = data.username
            document.getElementById('password').innerText = data.password
        })
    }
</script>
```

这样，我们就实现了从服务端获取数据并更新到页面中，前端开发者利用JS发起异步请求，可以实现各种各样的效果，而我们后端开发者只需要关心接口返回正确的数据即可，这就已经有前后端分离开发的雏形了（实际上之前，我们在JavaWeb阶段使用XHR请求也演示过，不过当时是纯粹的数据）

那么，我们接着来看，如何向服务端发起一个JS对象数据并进行解析，这里以简单的登录为例：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>测试</title>
    <script src="https://unpkg.com/axios@1.1.2/dist/axios.min.js"></script>
</head>
<body>
  <p>欢迎来到GayHub全球最大同性交友网站</p>
  <button onclick="login()">立即登录</button>
</body>
</html>
```

这里我们依然使用axios发起POST请求：

```html
<script>
    function login() {
        axios.post('/mvc/test', {
            username: 'test',
            password: '123456'
        }, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(({data}) => {
            if(data.success) {
                alert('登录成功')
            } else {
                alert('登录失败')
            }
        })
    }
</script>
```

服务器端只需要在请求参数的位置添加一个对象接收即可（和前面一样，因为这里也是提交的表单数据）：

```java
@ResponseBody
@PostMapping(value = "/test", produces = "application/json")
public String hello(String username, String password){
    boolean success = "test".equals(user.getUsername()) && "123456".equals(user.getPassword());
    JSONObject object = new JSONObject();
    object.put("success", success);
    return object.toString();
}
```

我们也可以将js对象转换为JSON字符串的形式进行传输，这里需要使用ajax方法来处理：

```html
<script>
    function login() {
        axios.post('/mvc/test', {
            username: 'test',
            password: '123456'
        }).then(({data}) => {
            if(data.success) {
                alert('登录成功')
            } else {
                alert('登录失败')
            }
        })
    }
</script>
```

如果我们需要读取前端发送给我们的JSON格式数据，那么这个时候就需要添加`@RequestBody`注解：

```java
@ResponseBody
@PostMapping(value = "/test", produces = "application/json")
public String hello(@RequestBody User user){
    boolean success = "test".equals(user.getUsername()) && "123456".equals(user.getPassword());
    JSONObject object = new JSONObject();
    object.put("success", success);
    return object.toString();
}
```

这样，我们就实现了前后端使用JSON字符串进行通信。
