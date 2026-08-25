# MVC理论基础与环境配置

在Spring框架学习之后，我们将继续学习有关MVC给我们带来的便捷之处。

## MVC理论基础

在之前，我们了解了有关项目的三层架构：

![img](https://oss.itbaima.cn/internal/markdown/2023/02/18/2IiK8YrfhF4zyU1.jpg)

每一层都有着对应的职责，其中最重要的当属表示层，因为它是直接与用户打交道的，并且所有的请求都会经过它去解析，然后再告知业务层进行处理，任何页面的返回与数据填充也靠表示层来完成，在之前的学习中，我们编写了大量的Servlet（也就是表示层实现），来处理浏览器的各个请求，但是我们发现，仅仅是几个很小的功能以及很少的页面，都要编写近十个Servlet，如果是更大型的网站，难道我们要编写成千上百个Servlet吗。

因此，SpringMVC正是为了解决这种问题而生的，它是一个非常优秀的表示层框架，采用MVC思想设计实现。

MVC详细解释如下：

- M是指业务模型（Model）：通俗的讲就是我们之前用于封装数据传递的实体类。
- V是指用户界面（View）：一般指的是前端页面。
- C则是控制器（Controller）：控制器就相当于Servlet的基本功能，处理请求，返回响应。

![img](https://oss.itbaima.cn/internal/markdown/2023/02/18/voy7HYrIbJuw9R3.jpg)

SpringMVC正是将这三者进行解耦，实现各干各的，更加细分对应的职责。最后再将View与Model进行渲染，，得到最终的页面并返回给前端（就像之前使用Thymeleaf那样，把实体数据对象和前端页面都给到Thymeleaf，然后它会将其进行整合渲染得到最终有数据的页面，而本教程也会使用Thymeleaf作为视图解析器进行讲解）。

## 配置环境

这里我们继续使用之前的Tomcat10服务器，Spring6之后要求必须使用Tomcat10或更高版本，跟之前一样，我们直接创建一个新的JakartaEE项目。

![image-20230219162053172](https://oss.itbaima.cn/internal/markdown/2023/02/19/4IucyfBKsLzASNJ.png)



创建完成后会自动生成相关文件，但是还是请注意检查运行配置中的URL和应用程序上下文名称是否一致。

然后，我们导入依赖：

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>6.2.10</version>
</dependency>
```



### XML配置

接着，我们配置一下web.xml，用DispatcherServlet替换掉Tomcat自带的Servlet，这里的url-pattern需要写为`/`，即可完成替换：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee https://jakarta.ee/xml/ns/jakartaee/web-app_5_0.xsd"
         version="5.0">
    <servlet>
        <servlet-name>mvc</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>mvc</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

接着需要为整个Web应用程序配置一个Spring上下文环境（也就是容器），因为SpringMVC是基于Spring开发的，它直接利用Spring提供的容器来实现各种功能，那么第一步依然跟之前一样，需要编写一个配置文件，那么我们再创建一个spring.xml：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd">
</beans>
```

接着我们需要为DispatherServlet配置一些初始化参数来指定刚刚创建的配置文件：

```xml
<servlet>
    <servlet-name>mvc</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
      	<!--     指定我们刚刚创建在类路径下的XML配置文件       -->
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath:spring.xml</param-value>
    </init-param>
</servlet>
```

这样我们就完成了基本的配置，现在我们可以来测试一下是否配置正确，我们删除项目自带的Servlet类，创建一个Mvc中使用的Controller类，现在还没学没关系，跟着写就行了，这里我们只是测试一下：

```java
@Controller
public class HelloController {
    @ResponseBody
    @RequestMapping("/")
    public String hello(){
        return "HelloWorld!";
    }
}
```

接着我们需要将这个类注册为Bean才能正常使用，我们来编写一下Spring的配置文件，这里我们直接配置包扫描，XML下的包扫描需要这样开启：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd">
  	<!-- 需要先引入context命名空间，然后直接配置base-package属性就可以了-->
    <context:component-scan base-package="com.example"/>
</beans>
```

如果可以成功在浏览器中出现HelloWorld则说明配置成功：

![](https://oss.itbaima.cn/internal/markdown/2023/02/19/D1sAFePzj7d49VL.png)



### 注解配置

如果，你希望完完全全丢弃xml配置，只使用注解进行开发，可以直接添加一个类，Tomcat会在类路径下实现ServletContainerInitializer接口的类，如果Tomcat找到了，就会用他来配置Servlet容器，Spring提供了这个接口的实现类SpringServletContainerInitializer , 通过@HandlesTypes(WebApplicationInitializer.class)设置，这个类反过来会查找实现WebApplicationInitializer 的类，并将配置的任务交给他们来完成，说了这么一堆，其实直接实现接口即可：

```java
public class MainInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {

    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class[]{WebConfiguration.class};   //基本的Spring配置类，一般用于业务层配置
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class[0];  //配置DispatcherServlet的配置类、主要用于Controller等配置，这里为了学习简单，就不分这么详细了，只使用上面的基本配置类
    }

    @Override
    protected String[] getServletMappings() {
        return new String[]{"/"};    //匹配路径，与上面一样
    }
}
```

接着我们需要再配置类中添加一些必要的注解：

```java
@Configuration
@EnableWebMvc   //快速配置SpringMvc注解，如果不添加此注解会导致后续无法通过实现WebMvcConfigurer接口进行自定义配置
@ComponentScan("com.example.controller")
public class WebConfiguration {
}
```

这样我们同样可以正常访问：

![image-20230219170637540](https://oss.itbaima.cn/internal/markdown/2023/02/19/D1sAFePzj7d49VL.png)



之后为了方便，我们就统一使用全注解形式编写。

如果日志科技有报错无法显示Mvc相关的日志，请添加以下依赖：

```xml
<dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
      <version>1.7.33</version>
</dependency>
<dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-jdk14</artifactId>
      <version>1.7.33</version>
</dependency>
```

添加后就可以正常打印日志了：

![image-20230630162821105](https://oss.itbaima.cn/internal/markdown/2023/06/30/7eti1wuU8Bd4RqZ.png)

