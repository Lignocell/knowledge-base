# Cookie

什么是Cookie？它可以在浏览器中保存一些信息（即，保存账号密码（记住我）），并且在下一次请求时，请求头中会携带这些信息。

我们可以编写一个测试用例：

```java
Cookie cookie=new Cookie("test","yyds");  //name与value
resp.addCookie(cookie);   //服务器发送给浏览器
resp.sendRedirect("time");  //重定向跳转页面
```

```java
for(Cookie:req.getCookies()){
    System.out.println(cookie.getName()+":"+cookie.getValue());
}
```

我们观察一下，在HttpServletResponse中添加Cookie之后，浏览器的响应头中会包含一个Set-Cookie属性，同时，在重定向之后，我们请求头中，会携带此Cookie作为一个属性，同时，我们可以直接通过HttpServletRequest来快速获得有哪些Cookie信息。

![点击查看源网页](https://oss.itbaima.cn/internal/markdown/2023/03/06/3JcLpr9GYMnbBHw.jpg)

接着，我们来看看Cookie包含哪些信息：

- name-Cookie的名称，Cookie一旦创建，名称不可更改。
- value-Cookie的值，新版本支持汉字。
- maxAge-Cookie失效的时间，单位秒。如果为正数，则该Cookie会在maxAge秒后失效。如果为负数，该Cookie为临时Cookie，关闭浏览器即失效，浏览器不会以任何形式保存该Cookie。如果为0，表示删除该Cookie，默认为-1.
- secure-该Cookie是否仅被使用安全协议传输。安全协议由HTTPS，SSL等，在网络上传输数据之前先将数据加密，默认为false。

- path-Cookie的使用路径。如果设置为/sessionWeb/”，则只有contextPath为/sessionWeb”的程序可以访问该Cookie。如果设置为/”，则本域名下contextPach都可以访问该Cookie。注意最后一个字符必须为/”。
- domain-可以访问该Cookie的域名。如果设置为“.google.com”，则所有以google.com结尾的域名都可以访问该Cookie。注意第一个字符必须为“.”。
- comment-该Cookie的用处说明，浏览器显示Cookie信息的时候显示该说明。
- version-Cookie使用的版本号0表示遵循Netscape的Cookie规范1表示遵循W3C的RFC2109规范。

我们发现，最关键的是name、value、maxAge、domains属性。

那么，我们来看看修改maxAge失效时间：

```java
cookie.setMaxAge(20);
```

设定为0秒，我们可以看到，响应头为我们设定了20秒的过期时间，0秒内访问都会携带此Cookie，而超过0秒，Cookie消失。

既然了解了Cookie的作用，我们就可以通过使用Cookie来实现记住我的功能，我们可以将用户名和密码全部保存在Cookie中，如果访问我们的首页时携带了这些Cookie，那么我们就可以直接为用户进行登录，如果登录成功则直接跳转至首页，如果登录失败，则清理浏览器中的Cookie。

那么首先，我们现在前端页面的表单中添加一个勾选框：

```html
<div>
    <label>
        <input type="checkbox" name="remember-me">
        记住我
    </label>
</div>
```

接着，我们在登录成功时进行判断，如果用户勾选了记住我，那么就将Cookie存储到本地：

```java
if(map.containsKey("remeber-me")){
    Cookie co_username=new Cookie("username",username);
    co_username.setMaxAge(30);
    Cookie co_password=new Cookie("password",password);
    co_password.setMaxAge(30);
    resp.addCookie(co_username);  //从服务器发送到浏览器
    resp.addCookie(co_password);
}
```

然后，我们修改一下默认的请求地址，一律通过http://localhost:8080/yyds/login进行登录，我们需要添加GET请求的相关处理：

```java
@Override
protected void doGet(HttpServletRequest req,HttpServletResponse resp) throws ServletException,IOException{
    Cookie[] cookies=req.getCookies();
    if(cookies !=null){
        String username=null;
        String password=null;
       for (Cookie cookie : cookies) {
            if(cookie.getName().equals("username")) 
                username = cookie.getValue();
            if(cookie.getName().equals("password"))
                password = cookie.getValue();
        }
        if(username != null && password != null){
            //登陆校验
            try (SqlSession sqlSession = factory.openSession(true)){
                UserMapper mapper = sqlSession.getMapper(UserMapper.class);
                User user = mapper.getUser(username, password);
                if(user != null){
                    resp.sendRedirect("time");
                    return;   //直接返回
                }
            }
        }
    }
    req.getRequestDispatcher("/").forward(req, resp);   //正常情况还是转发给默认的Servlet帮我们返回静态页面
    //forward(req, resp) 表示服务端内部把 req（请求对象）和 resp（响应对象）“转发给根路径对应的资源

}
```

现在，0s内都不需要重新登录，访问登录页面后，会直接跳转到time页面。

现在还有一个问题，无论是否登录，所有人都可以访问主页，那么如何实现只有登录后才能访问呢？这里要用到Session对象。
