# Session

由于HTTP是无连接的（每次请求都是一锤子买卖，与下次无关），那么如何能辨别当前的请求是来自哪个用户发起的呢？Session就是用来处理这种问题的，每个用户的会话都会有一个自己的Session对象，来自浏览器的所有请求，就属于同一个会话。

但是HTTP协议是无连接的，那Session是如何做到辨别是否来自同一个浏览器呢？Session实际上是基于Cookie实现的，前面我们学习了Cookie，我们知道，服务端可以将Cookie保存到浏览器，当浏览器下次访问时，就会附带这些Cookie信息。

Session也利用了这一点，他给浏览器设定一个叫做JSESSIONID的Cookie，值是随机的排列组合的字母＋数字，而此Cookie就对应了你属于哪个对话，只要浏览器携带这个Cookie访问服务器，服务器就会通过Cookie的值进行辨别，得到对应Session对象，因此，这样就可以追踪到底是哪一个浏览器在访问服务器。

那么现在，我们在用户登录成功之后，将用户对象添加到Session中，只要此用户发起的请求，我们都可以从HttpSession中读取到存储在会话中的数据：

```java
HttpSession session=req.getSession();
session.setAttribute("user",user);  //存储到Session对象
```

同时，如果用户没有登录就去访问首页，那么我们将发送一个重定向请求，告诉用户，需要先进行登录才可以访问：

```java
HttpSession session=req.getSession();
User user=(User) sesson.getAttribute("user");
if(user==null){
    resp.sendRedirect("login");
    return;
}
```

在访问过程中，注意观察Cookie变化。

Session并不是永久都存在的，它有着自己的过期时间，默认30min，若超过此时间，Session将丢失，我们可以在配置文件中修改过去时间：

```xml
<session-config>
    <session-timeout>1</session-timeout>
</session-config>
```

我们也可以在代码中使用invalidate方法使Session立刻失效：

```java
session.invalidate();
```

现在，只有完成登录的用户才有资格访问首页。
