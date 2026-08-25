# 了解JSP页面与加载规则

前面我们已经完成了整个Web应用程序生命周期中所有内容的学习，我们已经完全了解，如何编写一个Web应用程序，并放到Tomcat上部署运行，以及如何控制浏览器发来的请求，通过Session+Filter实现用户的登录验证，通过Cookie实现自动登录等操作。到目前位置，我们已经具备了编写一个完整Web网站的能力。

在之前的教程中，我们的前端静态页面并没有和后端相结合，我们前端页面所需要的数据全部需要单独向后端发起请求获取，并动态进行内容填充，这是一种典型的前后端分离写法，前端只负责要数据和显示数据，后端只负责处理数据和提供数据，这也是更流行的一种写法，让前端开发者和后端开发者各尽其职，这才是我们希望的开发模式。

JSP并不是重点，它已经过时了，使用JSP会导致前后端更加耦合，因为*只做了解即可**。

JSP其实就是一种模板引擎，那么何为模板引擎呢？顾名思义，它就是一个模板，而模板需要我们填入数据，才会变成一个页面，也就是说，我们可以直接在前端中填写数据，填写后生成一个最终的HTML页面返回给前端。

首先创建新项目，删除Java目录下的内容，只留下默认创建的jsp文件。我们发现，在webapp目录下，存在一个index.jsp文件，我们直接运行项目，会直接访问这个JSP页面。

```jsp
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>JSP - Hello World</title>
</head>
<body>
<h1><%= "Hello World!" %>
</h1>
<br/>
<a href="hello-servlet">Hello Servlet</a>
</body>
</html>
```

但是，我们并没有编写对应的Servlet来解析呀？这个JSP是如何被加载的呢：

实际上，我们一开始提到的两个Tomcat默认的Servlet中，一个是用于请求静态资源，还有一个就是用于处理jsp的：

```xml
<!-- The mappings for the JSP servlet -->
    <servlet-mapping>
        <servlet-name>jsp</servlet-name>
        <url-pattern>*.jsp</url-pattern>
        <url-pattern>*.jspx</url-pattern>
    </servlet-mapping>
```

那么，JSP和普通的HTML页面有什么区别呢？其实没什么区别，但我们可以直接在JSP中编写java代码，并在页面加载的时候执行，我们随便找个地方插入：

```jsp
<%
    System.out.println("JSP页面被加载");
%>
```

我们发现，请求一次页面，页面就会加载一次，并执行我们填写的Java代码，也就是说，我们可以直接在此页面中执行Java代码来填充我们的数据，这样我们的页面就变成了一个动态页面：

```jsp
<h1>
    <% =new Date()%>
</h1>
```

现在，访问我们的网站，每次都会创建一个新的Date对象，因为每次访问获取的时间都不一样，我们的网站已经算是一个动态网站了。

虽然这样在一定程度上为我们提供了便利，但是这样的写法相当于整个页面既要编写前端代码，也要编写后端代码，随着项目的扩大，整个页面会显得难以阅读，造成不必要的开销。

那么我们来研究一下，为什么JSP页面能够在加载的时候执行Java代码呢？

首先我们将此项目打包，并在Tomcat服务端中运行，生成了一个文件夹并且可以正常访问。

我们现在看到`work`目录，我们发现这个里面多了一个`index_jsp.java`和`index_jsp.class`，那么这些东西是干嘛的呢，我们来反编译一下就啥都知道了：

```java
public final class index_jsp extends org.apache.jasper.runtime.HttpJspBase  //继承自HttpServlet
    implements org.apache.jasper.runtime.JspSourceDependent,
                 org.apache.jasper.runtime.JspSourceImports {

 ...

  public void _jspService(final jakarta.servlet.http.HttpServletRequest request, final jakarta.servlet.http.HttpServletResponse response)
      throws java.io.IOException, jakarta.servlet.ServletException {

    if (!jakarta.servlet.DispatcherType.ERROR.equals(request.getDispatcherType())) {
      final java.lang.String _jspx_method = request.getMethod();
      if ("OPTIONS".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        return;
      }
      if (!"GET".equals(_jspx_method) && !"POST".equals(_jspx_method) && !"HEAD".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        response.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, "JSP 只允许GET、POST和HEAD。Jasper 还允许OPTIONS");
        return;
      }
    }

    final jakarta.servlet.jsp.PageContext pageContext;
    jakarta.servlet.http.HttpSession session = null;
    final jakarta.servlet.ServletContext application;
    final jakarta.servlet.ServletConfig config;
    jakarta.servlet.jsp.JspWriter out = null;
    final java.lang.Object page = this;
    jakarta.servlet.jsp.JspWriter _jspx_out = null;
    jakarta.servlet.jsp.PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html; charset=UTF-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
             null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\n");
      out.write("\n");
      out.write("<!DOCTYPE html>\n");
      out.write("<html>\n");
      out.write("<head>\n");
      out.write("    <title>JSP - Hello World</title>\n");
      out.write("</head>\n");
      out.write("<body>\n");
      out.write("<h1>");
      out.print( new Date() );
      out.write("</h1>\n");

    System.out.println("JSP页面被加载");

      out.write("\n");
      out.write("<br/>\n");
      out.write("<a href=\"hello-servlet\">Hello Servlet</a>\n");
      out.write("</body>\n");
      out.write("</html>");
    } catch (java.lang.Throwable t) {
      if (!(t instanceof jakarta.servlet.jsp.SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try {
            if (response.isCommitted()) {
              out.flush();
            } else {
              out.clearBuffer();
            }
          } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
```

我们发现，它是继承自`HttpJspBase`类，我们可以反编译一下jasper.jar（它在tomcat的lib目录中）来看一下。

```java
package org.apache.jasper.runtime;

import jakarta.servlet.ServletConfig;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.jsp.HttpJspPage;
import java.io.IOException;
import org.apache.jasper.compiler.Localizer;

public abstract class HttpJspBase extends HttpServlet implements HttpJspPage {
    private static final long serialVersionUID = 1L;

    protected HttpJspBase() {
    }

    public final void init(ServletConfig config) throws ServletException {
        super.init(config);
        this.jspInit();
        this._jspInit();
    }

    public String getServletInfo() {
        return Localizer.getMessage("jsp.engine.info", new Object[]{"3.0"});
    }

    public final void destroy() {
        this.jspDestroy();
        this._jspDestroy();
    }

    public final void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this._jspService(request, response);
    }

    public void jspInit() {
    }

    public void _jspInit() {
    }

    public void jspDestroy() {
    }

    protected void _jspDestroy() {
    }

    public abstract void _jspService(HttpServletRequest var1, HttpServletResponse var2) throws ServletException, IOException;
}
```

实际上，Tomcat在加载JSP页面时，会将其动态转换为一个java类并编译为class进行加载，而生成的Java类，正是一个Servlet的子类，而页面的内容全部被编译为输出字符串，这便是JSP的加载原理，因此，JSP本质上依然是一个Servlet：

![image-20230306164106712](https://oss.itbaima.cn/internal/markdown/2023/03/06/UGJBqvOTDeX5SuM.png)
