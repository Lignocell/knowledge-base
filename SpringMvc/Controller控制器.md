# Controller控制器

有了SpringMvc之后，我们不必像之前那样一个请求地址创建一个Servlet了，它使用DispatcherServlet替代Tmocat为我们提供默认的静态资源Servlet，也就是说，现在所有的请求（除了jsp，因为Tomcat还提供了一个jsp的Servlet）都会经过DispatcherServlet进行处理。

那么，DispatcherServlet会帮我们做什么呢：

![img](https://oss.itbaima.cn/internal/markdown/2023/02/18/SQNnl3yFjhHbp1G.jpg)

根据图片我们可以了解，我们的请求到达Tomcat服务器之后，会交给当前的Web应用程序进行处理，而SpringMVC则使用DispathcherServlet来处理所有的请求，也就是说它被作为一个统一的访问点，所有的请求全部由它进行调度。

当一个请求经过DispathcerServlet之后，会先走过Handlermapping，它会将请求映射为HandlerExecutionChain，依次经过HandlerInterceptor（有点类似于我们之前学习到的过滤器），不过在SpringMVC中，我们使用的是拦截器，然后再交给HandlerAdapter，根据请求的路径选择合适的控制器进行处理，控制器处理完成之后，会返回一个ModelAndView对象，包括数据模型和视图，通俗的讲就是页面数据和页面本身。

返回ModelAndView之后，会交给ViewResolver（视图解析器）进行处理，视图解析器会对整个视图页面进行解析，SpringMVC自带了一些视图解析器，但是只适用于JSP页面，我们也可以像之前一样使用Thymeleaf作为视图解析器，这样我们就可以根据给定的视图名称，直接读取HTML编写的页面，解析为一个真正的View。

解析完成后，将需要将页面的数据全部渲染到View中，最后返回DispatcherServlet一个包含所有数据的成型页面，再响应给浏览器，完成全过程。

因此，实际上整个过程只需要我们编写对应的请求路径，Controller已经配置好我们需要的ViewResolver即可，之后还可以继续添加补充拦截器，而其他流程SpringMVC就已经全部帮我们完成了。

## 配置视图解析器和控制器

首先，我们需要实现最基本的页面解析并返回，第一步就是配置视图解析器，这里我们使用Thymeleaf:

```xml
<dependency>
    <groupId>org.thymeleaf</groupId>
    <artifactId>thymeleaf-spring6</artifactId>
    <version>3.1.3.RELEASE</version>
</dependency>
```

配置视图解析器非常简单，我们只需要将ViewResolver注册为Bean即可，这里我们直接在配置类中编写：

```java
@Configuration
@EnableWebMvc
@ComponentScan("com.example.controller")
public class WebConfiguration {
    //我们需要使用ThymeleafViewResolver作为视图解析器，并解析我们的HTML页面
    @Bean
    public ThymeleafViewResolver thymeleafViewResolver(SpringTemplateEngine springTemplateEngine){
        ThymeleafViewResolver resolver = new ThymeleafViewResolver();
        resolver.setOrder(1);   //可以存在多个视图解析器，并且可以为他们设定解析顺序
        resolver.setCharacterEncoding("UTF-8");   //编码格式是重中之重
        resolver.setTemplateEngine(springTemplateEngine);   //和之前JavaWeb阶段一样，需要使用模板引擎进行解析，所以这里也需要设定一下模板引擎
        return resolver;
    }

    //配置模板解析器
    @Bean
    public SpringResourceTemplateResolver templateResolver(){
        SpringResourceTemplateResolver resolver = new SpringResourceTemplateResolver();
        resolver.setSuffix(".html");   //需要解析的后缀名称
        resolver.setPrefix("/");   //需要解析的HTML页面文件存放的位置，默认是webapp目录下，如果是类路径下需要添加classpath:前缀
        return resolver;
    }

    //配置模板引擎Bean
    @Bean
    public SpringTemplateEngine springTemplateEngine(ITemplateResolver resolver){
        SpringTemplateEngine engine = new SpringTemplateEngine();
        engine.setTemplateResolver(resolver);   //模板解析器，默认即可
        return engine;
    }
}
```

现在，我们完成了视图解析器的配置，我们接着来创建一个Controller，非常简单，只需要在一个类上添加一个@Controller注解即可，它会被Spring扫描并注册为Controller类型的Bean，然后我们只需要在类中编写方法用于处理对应地址的需求即可：

```java
@Controller   //直接添加注解即可
public class HelloController {

    @RequestMapping("/index")   //直接填写访问路径
    public ModelAndView index(){
        return new ModelAndView("index");  //返回ModelAndView对象，这里填入了视图的名称
      	//返回后会经过视图解析器进行处理
    }
}
```

接着，我们在类路径根目录下创建一个简单的html文件：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>测试</title>
</head>
<body>
    <p>欢迎来到GayHub全球最大同性交友网站</p>
</body>
</html>
```

我们会发现，打开浏览器之后就可以直接访问我们的HTML页面了：

![image-20230220150905300](https://oss.itbaima.cn/internal/markdown/2023/02/20/ru4pBgI75JZxG6F.png)



我们在之前，使用Thymeleaf解析后端的一些数据时，需要通过Context进行传递，而使用SpringMVC之后，数据我们可以直接导向Model模型层进行提供：

```java
@RequsetMapping(value="/index")  //指请求路径
publc ModelAndView index(){
    ModelAndView model=new ModelAndView("index");
    	model.getModel().put("name","啊这");
    return model;
}
```

这样Thymeleaf就能收到我们传递的数据进行解析：

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="static/test.js"></script>
</head>
<body>
    HelloWorld：
    <div th:text="${name}"></div>
</body>
</html>
```

当然，为了简便，我们可以直接返回View名称，SpringMVC会将其自动包装为ModelAndView对象：

```java
@RequestMapping(value = "/index")
public String index(){
    return "index";
}
```

我们还可以单独添加一个Model作为形参设置，SpringMVC通过依赖注入会自动帮助我们传递实例对象：

```java
@RequestMapping(value = "/index")
public String index(Model model){  //这里不仅仅可以是Model，还可以是Map、ModelMap
    model.addAttribute("name", "yyds");
    return "index";
}
```

有了Spring框架的加持，相比我们之前编写的Web应用程序，简直方便了一个层次。

注意，一定要保证视图名称下面出现横线并且按住Ctrl可以跳转，配置才是正确的（最新版IDEA）。

我们的页面中可能也会包含静态资源，因此这里我们还需要配置一下，让静态资源通过Tomcat提供的默认Servlet进行解析，我们需要让配置类实现一下WebMvcConfigurer接口，这样在Web应用程序启动时，会根据我们重写方法里面的内容进行进一步的配置：

```java
@Override
public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
    configurer.enable();   //开启默认的Servlet
}

@Override
public void addResourceHandlers(ResourceHandlerRegistry registry) {
    registry.addResourceHandler("/static/**").addResourceLocations("/static/");
    //配置静态资源的访问路径
}
```

我们编写一下前端内容：

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>测试</title>
    <!-- 引用静态资源，这里使用Thymeleaf的网址链接表达式，Thymeleaf会自动添加web应用程序的名称到链接前面 -->
    <script th:src="@{/static/test.js}"></script>
</head>
<body>
    <p>欢迎来到GayHub全球最大同性交友网站</p>
</body>
</html>
```

创建`test.js`并编写如下内容：

```javascript
window.alert("欢迎来到GayHub全球最大同性交友网站
```

最后访问页面，页面在加载时就会显示一个弹窗，这样我们就完成了最基本的页面配置。相比之前的方式，这样就简单很多了，直接避免了编写大量的Servlet来处理请求。

##  @RequestMapping详解

前面我们已经了解到，如何创建一个控制器来处理我们的请求，接着我们只需要在控制器添加一个方法用于处理我们对应的请求即可，之前我们需要完整的编写一个Servlet来实现，而现在我们只需要添加一个@RequestMapping就可以实现，此注解就是将请求和处理请求的方法建立一个映射关系，当收到请求时，可以根据映射关系来调动对应的请求处理方法，注解定义如下：

```java
@Mapping
public @interface RequestMapping {
    String name() default "";

    @AliasFor("path")
    String[] value() default {};

    @AliasFor("value")
    String[] path() default {};

    RequestMethod[] method() default {};

    String[] params() default {};

    String[] headers() default {};

    String[] consumes() default {};

    String[] produces() default {};
}
```

#### path/value

其中最关键的就是path属性（相当于value），它决定了当前方法处理的请求路径，注意路径必须全局唯一，任何路径只能由一个方法进行处理，它是一个数组，也就是说此方法不仅可以用于处理某一个请求路径，我们可以使用此方法处理多个请求路径：

```java
@RequstMapping({"/index","/test"})
public ModelAndView index(){
    return new ModelAndView("index");
}
```

现在，我们无论访问index还是test都会经过此方法进行处理。

我们也可以将@RequstMapping添加到类名上，表示为此类中的所有请求映射添加一个路径前缀，比如：

```java
@Controller
@RequestMapping("/yyds")
public class MainController{
    @RequstMapping({"/index","/test"})
    public ModelAndView index(){
        return new ModelAndView("index");
    }
}
```

此时，我们需要访问 yyds/index或者 yyds/test才能访问到页面。我们可以直接在IDEA下方的端点板块中查看当前Web应用程序定义的所有请求映射，并且可以通过IDEA为我们提供的内置Web客户端直接访问某个路径。

路径还支持通配符进行匹配：

- ?：表示任意一个字符，比如`@RequestMapping("/index/x?")`可以匹配/index/xa。index/xb等等。
- *：表示任意-n个字符，比如`@RequestMapping("/index/*")`可以匹配/index/lbwnb。index/yyds等。
- **：表示当前目录或基于当前目录的多级目录，比如`@RequestMapping("/index/**")`可以匹配/index。index/xxx等。

#### method

我们接着来看下一个method属性，顾名思义，它就是请求的方法类型，我们可以限定请求方式，比如：

```java
@RequestMapping(value = "/index", method = RequestMethod.POST)
public ModelAndView index(){
    return new ModelAndView("index");
}
```

现在如果我们直接访问浏览器，大概会显示405方法不支持，因为浏览器默认是使用GET方法去获取界面，我们指定这里是POST方法，所以访问失败，我们现在再去端点中用POST方法，会成功获取。

我们可以使用衍生注解来直接指定请求映射（@PostMapping）：

```java
@PostMapping(value = "/index")
public ModelAndView index(){
    return new ModelAndView("index");
}
```

#### params

我们可以使用params属性来指定请求必须携带哪些指定参数，比如：

```java
@RequestMapping(value = "/index", params = {"username", "password"})
public ModelAndView index(){
    return new ModelAndView("index");
}
```

比如这里我们要求必须携带username和password属性，否则无法访问。它还支持表达式，比如我们可以这样写：

```java
@RequestMapping(value = "/index", params = {"!username", "password"})
public ModelAndView index(){
    return new ModelAndView("index");
}
```

在username之前添加一个感叹号表示请求的不允许携带此参数，否则无法访问，我们甚至可以直接设定一个固定值：

```java
@RequestMapping(value = "/index", params = {"username!=test", "password=123"})
public ModelAndView index(){
    return new ModelAndView("index");
}
```

这样，请求参数username不允许为test，并且password必须为123，否则无法访问。

#### header

header和params的用法一致，但是它要求的是请求头需要携带什么内容，比如：

```java
@RequestMapping(value = "/index", headers = "!Connection")
public ModelAndView index(){
    return new ModelAndView("index");
}
```

那么，如果请求头携带了Connnection属性，那么就无法访问。

#### consumes

指定处理请求的提交内容类型，例如application/json，test/html。

#### produces

指定返回的内容类型，仅当request请求头中包含 Accept)类型中包含该指定类型才返回。

## @RequestParam和@RequestHeader详解

我们接着来看，如何获取到请求中的参数。

我们只需要为方法添加一个形式参数，并在形式参数前面加上@RequestParam即可：

```java
@RequestMapping(value = "/index")
public ModelAndView index(@RequestParam("username") String username){
    System.out.println("接受到请求参数："+username);
    return new ModelAndView("index");
}
```

我们需要在@RequestParam中填写参数名称，参数的值会自动传递给形式参数，我们可以直接在方法中使用，注意，如果参数名称和形式参数名称相同，即使不添加@RequestParam也能获取到参数值。

一旦添加@RequestParam，那么此请求必须携带指定参数，我们也可以将require属性设定为false来将属性设定为非必须项：

```java
@RequestMapping(value = "/index")
public ModelAndView index(@RequestParam(value = "username", required = false) String username){
    System.out.println("接受到请求参数："+username);
    return new ModelAndView("index");
}
```

我们还可以直接设定一个默认值，当请求参数缺失时，可以直接使用默认值：

```java
@RequestMapping(value = "/index")
public ModelAndView index(@RequestParam(value = "username", required = false，defaultValue="你好") String username){
    System.out.println("接受到请求参数："+username);
    return new ModelAndView("index");
}
```

如果需要使用Servlet原本的一些类，比如：

```java
@RequestMapping(value = "/index")
public ModelAndView index(HttpServletRequest request){
    System.out.println("接受到请求参数："+request.getParameterMap().keySet());
    return new ModelAndView("index");
}
```

直接添加HttpServletRequest为形式参数即可，SpringMVC会自动传递该请求原本的HttpServletRequest对象，同理，我们也可以添加HttpServletResponse作为形式参数，甚至可以直接将HttpSession也作为参数传递：

```java
@RequestMapping(value = "/index")
public ModelAndView index(HttpSession session){
    System.out.println(session.getAttribute("test"));
    session.setAttribute("test", "鸡你太美");
    return new ModelAndView("index");
}
```

我们还可以直接将请求参数传递给实体类：

```java
@Data
public class User{
    String username;
    String password;
}
```

注意必须携带set方法或是构造方法中包含所有参数，请求参数会自动根据类中的字段名称进行匹配：

```java
@RequestMapping(value = "/index")
public ModelAndView index(User user){
    System.out.println("获取到cookie值为，+user);
    return new ModelAndView("index");
}
```

@RequestHeader与@RequestParam用法一致，但一个是获取请求头参数的。

## @CookieValue和@SessionAttrbutie

通过使用@CookieValue注解，我们也可以快速获取请求携带的Cookie信息：

```java
@RequestMapping("/index")
public ModelAndView index(HttpServletResponse response,@CookieValue(value="test",required=false) String test){
        System.out.println("获取到cookie值为，+test);
    response.addCookie(new Cookie("test", "lbwnb"));
    return new ModelAndView("index");
}
```

同样的，Session也能使用注解快速获取：

```java
@RequestMapping(value = "/index")
public ModelAndView index(@SessionAttribute(value = "test", required = false) String test,
                          HttpSession session){
    session.setAttribute("test", "xxxx");
    System.out.println(test);
    return new ModelAndView("index");
}
```

可以发现，通过使用SpringMVC框架，整个Web应用程序的开发变得非常简单，大部分功能只需要一个注解就可以搞定了，正是得益于Spring框架，SpringMVC才能大显身手。

## 重定向和请求转发

重定向和请求转发也非常简单，我们只需要在视图名称前面添加一个前缀即可，比如重定向：

```java
@RequestMapping("/index")
public String index(){
    return "redirect:home";
}

@RequestMapping("/home")
public String home(){
    return "home";
}
```

通过添加redirect：前缀，就可以很方便的使用重定向，那么请求转发呢，也一样，使用forward：前缀表示转发给其他请求映射：

```java
@RequestMapping("/index")
public String index(){
    return "forward:home";
}

@RequestMapping("/home")
public String home(){
    return "home";
}
```

## Bean的Web作用域

在学习Spring时我们讲解了Bean的作用域，包括singleton和prototype，Bean分别以单例模式和多例模式尽心那个创建，而在SpringMVC中，它会继续被细分：

- request：对于每次HTTP请求，使用request作用域定义的Bean都将产生一个新实例，请求结束后Bean也消失。
- session：对于每一个会话，使用session作用域定义的Bean都将产生一个新实例，会话过期后Bean也消失。
- global session：不常用，不做讲解。

这里我们创建一个测试类来试试看：

```java
public class TestBean {

}
```

接着将其注册为Bean，注意这里需要添加@RequestScope或是@SessionScope表示此Bean的Web作用域：

```java
@Bean
@RequestScope
public TestBean testBean(){
    return new TestBean();
}
```

我们将其自动注入到Controller中：

```java
@Controller
public class MainController {

    @Resource
    TestBean bean;

    @RequestMapping(value = "/index")
    public ModelAndView index(){
        System.out.println(bean);
        return new ModelAndView("index");
    }
}
```

我们发现，每次发起得到的Bean实例都不同，接着我们将其作用域修改为@SessionScope，这样作用域就上升到Session，只要清理浏览器的Cookie，那么都会被认为是同一个会话，只要是同一个会话，那么Bean实例始终不变。

实际上，它也是通过代理实现的，我们调用Bean中的方法会被转发到真正的Bean对象去执行。
