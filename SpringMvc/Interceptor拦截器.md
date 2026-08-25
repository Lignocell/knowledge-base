# Interceptor拦截器

拦截器是整个MVC的重要内容，与之前学过的过滤器类似，都是用于拦截一些非法请求，但是我们之前学习的过滤器是作用于Servlet之前，只有经过层层过滤器才能到达Servlet，而拦截器处理位置不同，它是在Servlet和RequestMapping之间，相当于DispatcherServlet在将请求交给对应的Controller中的方法**之前**进行拦截处理，它只会拦截所有Controller中定义请求映射对应的请求（不会拦截静态资源），这里一定要区分两者的不同。

![image-20230630194651686](https://oss.itbaima.cn/internal/markdown/2023/06/30/6J3D98HdkawAOVK.png)

## 创建拦截器

创建一个拦截器我们需要实现HandlerInterceptor接口：

```java
public class MainInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        System.out.println("我是处理之前，);
        return true;   //只有返回true才会继续，否则直接结束
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println("我是处理之后，);
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
      	//在DispatcherServlet完全处理完请求后被调用
        System.out.println("我是完成之后，);
    }
}
```

接着，我们需要在配置类（@Configuration）中进行注册：

```java
@Override
public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(new MainInterceptor())
      .addPathPatterns("/**")    //添加拦截器的匹配路径，只要匹配一律拦截
      .excludePathPatterns("/home");   //拦截器不进行拦截的路径
}
```

现在我们在浏览器中访问index页面，拦截器已经生效。

得到整理拦截器的执行顺序：

```
我是处理之前：
我是处理：
我是处理之后：
我是完成之后：
```

也就是说，处理前和处理后，包含了真正的请求映射的处理，在整个流程结束后还执行了一次afterCompletion，其实整个流程与我们之前的Filter类似，不过在处理之前，我们需要返回true或者false，表示是否被拦截即可，而不是去使用FilterChain进行向下传递。

那么我们就来看看，如果处理前返回false，会怎么样：

```
我是处理之前：
```

通过结果发现一旦返回false，之后的所有流程全部取消。

那么如果是在处理中发生异常了呢？

```java
@RequestMapping("/index")
public String index(){
    System.out.println("我是处理，);
    if(true) throw new RuntimeException("");
    return "index";
}
```

结果为：

```
我是处理之前：
我是处理：
我是完成之后：
```

我们发现，如果在处理中抛出异常，那么就不会执行处理postHandle方法，但是会执行afterCompletion方法，我们可以在这个方法中获取到被抛出的异常。

## 多级拦截器

前面我们学习了只有一个拦截器的情况，那么如果存在多个拦截器呢，我们现在用同样的方法创建二号拦截器：

```java
public class SubInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        System.out.println("二号拦截器：我是处理之前，);
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println("二号拦截器：我是处理之后，);
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        System.out.println("二号拦截器：我是完成之后，);
    }
}
```

注册二号拦截器：

```java
@Override
public void addInterceptors(InterceptorRegistry registry) {
  	//一号拦截器
    registry.addInterceptor(new MainInterceptor()).addPathPatterns("/**").excludePathPatterns("/home");
  	//二号拦截器
    registry.addInterceptor(new SubInterceptor()).addPathPatterns("/**");
}
```

注意拦截顺序就是注册顺序：

```
一号拦截器：我是处理之前！
二号拦截器：我是处理之前：
我是处理：
二号拦截器：我是处理之后：
一号拦截器：我是处理之后！
二号拦截器：我是完成之后：
一号拦截器：我是完成之后！
```

和多级Filter相同，在处理之前，是按照顺序从前向后进行拦截的，但是处理完成之后，就按照倒序执行处理后方法，而完成后是在所有的`postHandle`执行之后再同样的以倒序方式执行。

那么如果这时一号拦截器在处理前就返回了false呢？

```java
@Override
public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
    System.out.println("一号拦截器：我是处理之前！");
    return false;
}
```

得到结果如下：

```
一号拦截器：我是处理之前！
```

我们发现，与单个拦截器的情况一样，一旦拦截器返回false，那么之后无论有无拦截器，都不再继续。

我们可以更改拦截器顺序：

```java
@Override
public void addInterceptors(InterceptorRegistry registry) {
  	//一号拦截器
    registry.addInterceptor(new MainInterceptor()).addPathPatterns("/**").order(2);
  	//二号拦截器
    registry.addInterceptor(new SubInterceptor()).addPathPatterns("/**").order(1);
}
```

此时结果如下：

```
二号拦截器：我是处理之前：
一号拦截器：我是处理之前！
我是处理：
一号拦截器：我是处理之后！
二号拦截器：我是处理之后：
一号拦截器：我是完成之后！
二号拦截器：我是完成之后：
```


