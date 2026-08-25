# Filter

有了Session之后，我们就可以很好的控制用户的登录验证了，只有授权的用户，才可以访问一些页面，但是我们需要一个个去配置，太过于复杂，能否一次性地过滤掉没有登录验证的用户呢？

过滤器相当于在所有访问前加了一堵墙，来自浏览器的所有访问请求都会首先经过过滤器，只有过滤器允许通过的请求，才可以顺利地到达对应的Servlet，而过滤器不允许通过的请求，我们可以自由地进行控制是否进行重定向或是请求转发。并且过滤器可以添加很多个，就相当于添加很多堵墙。

添加过滤器很简单，只要实现Filter接口，并添加@WebFilter注解即可：

```java
@WebFilter("/*")  //路径的匹配规则和Servlet一致，这里表示匹配所有请求
public class TestFilter implements Filter{
    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException{
        
    }
}
```

这样，我们成功添加了一个过滤器。

我们发现，现在我们发起的所有请求，一律都要经过过滤器，但是所有请求都没有发出任何响应内容。

那么，如何让请求顺利到达对应的Servlet呢，我们只需要在后面添加一句：

```java
filterChain.doFilter(servletRequest,servletResponse);
```

这是什么意思呢：

由于我们整个应用程序可能存在多个过滤器，那么这行代码的意思实际上是将此请求传递给下一个过滤器，当没有下一个过滤器时，才会到达对应的Servlet进行处理，我们再来创建一个过滤器看看效果。

```java
@WebFilter("/*")
public class TestFilter2 implements Filter {
    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        System.out.println("我是2号过滤器");
        filterChain.doFilter(servletRequest, servletResponse);
    }
}
```

由于过滤器的过滤顺序是按照类名的自然排序进行的，因此我们将第一个过滤器命名进行调整。

![点击查看源网页](https://oss.itbaima.cn/internal/markdown/2023/03/06/LaDmPMWEtAB1HVF.jpg)

实际上，当doFilter方法调用时，就会一直向下直到Servlet，在Servlet处理完成之后，又依次返回到最前面的Filter，类似于递归的结果。

同Servlet一样，Filter也有对应的HttpFilter专用类，他针对HTTP请求进行了专门处理，因此我们可以直接使用HttpFilter来编写以下是HTTP反编译的方法)：

```java
public abstract class HttpFilter extends GenericFilter {
    private static final long serialVersionUID = 7478463438252262094L;

    public HttpFilter() {
    }

    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) throws IOException, ServletException {
        if (req instanceof HttpServletRequest && res instanceof HttpServletResponse) {
            this.doFilter((HttpServletRequest)req, (HttpServletResponse)res, chain);
        } else {
            throw new ServletException("non-HTTP request or response");
        }
    }

    protected void doFilter(HttpServletRequest req, HttpServletResponse res, FilterChain chain) throws IOException, ServletException {
        chain.doFilter(req, res);
    }
}
```

那么现在，我们就可以给我们的应用程序添加一个过滤器，用户在未登录情况下，只允许静态资源和登录页面请求通过，登录之后便可畅通无阻：

```java
@WebFilter("/*")
public class MainFilter extends HttpFilter{
    @Override
    protected void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        String url=req.getRequestURL().toString();  //获取用户访问的完整url
        //判断是否为静态资源静态资源不用拦截
        if(!url.endsWith(".js") && !url.endsWith(".css") && !url.endsWith(".png")){
            HttpSession session=req.getSession();
            User user=(User)session.getAttribute("user");
            //判断是否未登录并且访问的不是登录界面
            if(url==null&&!url.endsWith("login")){
                res.sendRedirect("login");
                return;
            }
        }
        //交给过滤链处理，让当前请求和响应传递给像一个过滤器，如果没有，就会传递给最终目标资源
        chain.doFilter(req,resp);
    }
}
```

`endsWith` 是 Java 中String类的一个方法，作用是*判断当前字符串是否以某个指定的子字符串结尾*，是boolean类型。
