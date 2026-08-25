# AOP面向切片

又是一个听起来很高大上的名词，AOP（Aspect Oriented Programming）思想实际上是：在运行代码时，动态的将代码切入到类的指定方法，或者指定位置上。也就是说，我们可以使用AOP来帮助我们在执行方法前后完成一些额外的指定操作，这就是代理。
通过AOP我们可以在保证原有业务不变的情况下，添加额外的动作，比如我们的某些方法执行完成之后，需要打印日志，那么这个时候，我们就可以使用AOP来帮助我们完成，它可以批量地为这些方法添加动作。可以说，它相当于将我们原有的方法，在不改变源代码的基础上进行了增强处理。
![image-20221130155358974](https://oss.itbaima.cn/internal/markdown/2022/11/30/sJbSrgiAxa8Vhcv.png)

相当于我们的整个业务流程，被直接斩断，并在断掉的位置添加了一个额外的操作，再连接起来，也就是在一个切点位置插入内容。它的原理实际上就是通过动态代理机制实现的。不过Spring底层并不是使用的JDK提供的动态代理，而是使用的第三方库实现，它能够以父类的形式代理，而不仅仅是接口。
## 使用配置实现AOP

在开始之前，我们先切换回XML配置文件模式，之后也会讲解AOP操作，现在我们需要了解相关XML配置：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
       http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop.xsd">
</beans>
```

Spring是支持AOP编程的框架之一，（实际上它整合了AspectJ框架的一部分），要使用AOP我们需要先导入一个依赖：

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-aspects</artifactId>
    <version>7.0.0-RC1</version>
</dependency>
```

那么，如何使用AOP呢？我们首先要明确要实现AOP操作，我们需要知道哪些内容：

1. 需要切入的类，类的哪个方法需要被切入，也就是说切入的位置。2. 切入之后需要执行哪个操作。3. 是在方法执行前被切入还是方法执行后。4. 如何告诉Spring需要被切入。
比如，我们需要对学生对象的study方法增强，在不修改源码的情况下，增加了一些额外操作：

```java
public class Student {
    public void study(){
        System.out.println("室友还在打游戏，我狠狠的学Java，太爽了"); 
      	//现在我们希望在这个方法执行完之后，打印一些其他的内容，在不修改原有代码的情况下，该怎么做呢，    }
}
```

我们先生成Bean：
```xml
<bean class="org.example.entity.Student"/>
```

首先需要解决的是，找到需要被切入的类，很显然，就是这个Student类，我们要切入的是这个study方法。
第二步，我们切入后需要做什么呢？在这里我们直接创建一个新的类，并将我们要执行的操作写成一个方法：

```java
public class StudentAOP {
  	//这个方法就是我们打算对其进行的增强操作    public void afterStudy() {
        System.out.println("为什么毕业了他们都继承家产，我还倒给他们打工，我努力的意义在哪里...");
    }
}
```

注意这个类也需要生成Bean：
```xml
<bean id="studentAOP" class="org.example.entity.StudentAOP"/>
```

第三步，我们要明确这个方法执行前切入还是执行后切入，显而易见，我们需要在执行后切入。
第四步，关键的一步来了，我们怎么才能告诉Spring我们要进行切入操作呢？这里我们需要在配置文件中进行AOP文件配置：
```xml
<aop:config>

</aop:config>
```

接着，我们需要添加一个新的切点，首先填写ID，这个随便起都可以：

```xml
<aop:pointcut id="test" expression:""/>
```

 然后就是通过后面的expression表达式来选择我们需要切入的方法，这个方法支持很多种方式进行选择，Spring AOP支持以下AspectJ切点指示器（PCD）用于表达式：（最主要的还是第一种，其他的现在只做了解）

- `execution`：用于匹配方法执行连接点。这是使用Spring AOP时使用的主要点切割指示器。- `within`：限制匹配到某些类型的连接点（使用Spring AOP时在匹配类型中声明的方法的执行）。- `this`：限制与连接点匹配（使用Spring AOP时方法的执行），其中bean引用（Spring AOP代理）是给定类型的实例。- `target`：限制匹配连接点（使用Spring AOP时方法的执行），其中目标对象（正在代理的应用程序对象）是给定类型的实例。- `args`：限制与连接点匹配（使用Spring AOP时方法的执行），其中参数是给定类型的实例。- `@target`：限制匹配连接点（使用Spring AOP时方法的执行），其中执行对象的类具有给定类型的注释。- `@args`：限制匹配到连接点（使用Spring AOP时方法的执行），其中传递的实际参数的运行时类型具有给定类型的注释。- `@within`：限制与具有给定注释的类型中的连接点匹配（使用Spring AOP时在带有给定注释的类型中声明的方法的执行）。- `@annotation`：与连接点主体（在Spring AOP中运行的方法）具有给定注释的连接点匹配的限制。
更多详细内容请查阅：https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#aop-pointcuts-designators

其中，我们主要学习的execution填写格式如下：
```
修饰符包名.类名.方法名称(方法参数)
```

- 修饰符：public、protected、private、包括返回值类型、static等等（使用*代表任意修饰符）
- 包名：如com.test， 代表全部，比如com.*代表com包下的全部包，- 类名：使用*也可以代表包下的所有类
- 方法名称：可以使用*代表全部方法
- 方法参数：填写对应的参数即可，比如 String, String)，也可以使用*来代表任意一个参数，使用..代表所有参数。
比如说：

```xml
<aop:pointcut id="test" expression="execution(*org.example.entity.Student.study())"/>
```

这样，我们就指明了需要切入的方法，这就是将我们增强的方法，我们在里面添加aop:aspect标签，并使用ref属性将其指向我们刚刚注册的AOP类Bean：
```xml
<aop:config>
    <aop:pointcut id="test" expression="execution(*org.example.entity.Student.study())"/>
    <aop:aspect ref="studentAOP">
    </aop:aspect>
</aop:config>
```

接着，我们需要添加后续动作了，当然，官方支持多种多样的，比如执行前，执行后，抛出异常前，方法返回后等等：

![image-20221216155201849](https://oss.itbaima.cn/internal/markdown/2022/12/16/uopJ9KyqMvQSwi4.png)

其中around方法为环绕方法，自由度更高，我们稍后介绍。这里我们按照上面要求直接添加后续动作，注意需要指明生效的切点：
```xml
<aop:config>
    <aop:pointcut id="test" expression="execution(*org.example.entity.Student.study())"/>
    <aop:aspect ref="studentAOP">
        <aop:after method="afterStudy" pointcut-ref="test"/>
    </aop:aspect>
</aop:config>
```

这样，我们就成功配置好了，配置正确会在旁边出现图标：

![image-20221216155551779](https://oss.itbaima.cn/internal/markdown/2022/12/16/hBaSmuovMzp5iIn.png)

我们来试试看吧：

```java
public static void main(String[] args) {
    ApplicationContext context = new ClassPathXmlApplicationContext("application.xml");
    Student bean = context.getBean(Student.class);
    bean.study();
}
```

结果如下：
![image-20221216155616952](https://oss.itbaima.cn/internal/markdown/2022/12/16/JlvLe9rgQw2pbXo.png)

可以看到在执行完结果后，仍然执行了我们的插入操作，这实际上就是动态代理做到的，实现在不修改原有代码的基础上，对方法的调用进行了各种增强，在之后的SpringMVC学习中，我们甚至可以使用它来快速配置访问日志打印。
前面说了，AOP是基于动态代理实现的，所以说我们直接获取Bean的类型，会发现不是原有类型了：
```java
Student bean=context.getBean(Student.class);
System.out.println(bean.getClass());
```

![image-20221216172042146](https://oss.itbaima.cn/internal/markdown/2022/12/16/8lsiRj6Q9eTLhSI.png)

这里其实是Spring通过CGLib为我们生成的动态代理类，，也就不难理解为什么调用方法会直接得到增强之后的结果了。包括我们前面讲解Spring的异步任务调度时，为什么能够直接实现异步，其实就是利用了AOP机制实现的方法增强。
虽然这个功能已经很强大了，但是仅仅能简单的切入还是不能满足一些需求，在某些情况下，我们可以寻找方法执行的一些参数，比如方法执行后返回了什么，或是方法开始之前传入了什么参数，现在我们修改一下Student：
```java
public class Student {
    public void study(String str){  //现在方法有一个String类型的参数        System.out.println("都别学Java了，根本找不到工作，快去"+str);
    }
}
```

我们希望在增强的方法中也能拿到这个参数，然后进行处理：
```java
public class StudentAOP {
    public void afterStudy() {
      	//这个str参数我们该从哪里拿呢，        System.out.println("学什么"+str+"，Rust天下第一，");
    }
}
```

这个时候，我们可以为我们切入的方法添加一个JoinPoint参数，通过这个参数就可以快速获取切点位置的一些信息：

```java
public void afterStudy(JoinPoint point) {   //JoinPoint实例会被自动传入
    //这里我们直接通过getArgs()返回的参数数组获取第1个参数    System.out.println("学什么"+point.getArgs()[0]+"，Rust天下第一，");
}
```

接着，我们修改一下刚才的AOP配置：
```xml
<aop:pointcut id="test" expression="execution(* org.example.entity.Student.study(String))"/>
```

现在我们来测试一下：

```java
public static void main(String[] args) {
    ApplicationContext context = new ClassPathXmlApplicationContext("application.xml");
    Student bean = context.getBean(Student.class);
    bean.study("PHP");
}
```

![image-20221216160501469](https://oss.itbaima.cn/internal/markdown/2022/12/16/NrZA49JvpgEyL2O.png)



是不是感觉大部分功能都可以通过AOP来完成了：
我们接着来看自定义度更高的环绕方法，我们希望在方法执行前和执行后都加入各种各样的动作，但是这样执行太慢了，能不能直接写在一起呢？此时我们可以使用环绕方法。
环绕方法相当于完全代理了此方法，它完全将方法包含到最中间，需要我们手动调用才可以执行此方法，并且我们可以直接获取更多的参数：

```java
public Object around(ProceedingJoinPoint joinPoint)throws Throwable{
    System.out.println("方法开始之前);
    Object value = joinPoint.proceed();   //调用process方法来执行被代理的原方法，如果有返回值，可以使用value接收
    System.out.println("方法执行完成，结果为，+value);
  	return value;
}
```

注意：如果原方法存在返回值，那么环绕方法也需要一个返回值。
通过proceed方法执行被代理的方法，也可以修改参数之后调用proceed(Object[])，使用我们给定的参数再去执行：
```java
public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
    System.out.println("方法开始之前);
    String arg = joinPoint.getArgs()[0] + "伞兵一个;
    Object value = joinPoint.proceed(new Object[]{arg});  //使用修改后的arg来重新执行    System.out.println("方法执行完成，结果为，+value);
    return value;
}
```

这时我们还是以study方法为例，现在我们希望在调用前修改这个方法的传入值，然后在调用之后对返回值结果进行处理：

```java
public String study(String str){
    if(str.equals("Java"))
        System.out.println("我的梦想是学Java");
    else {
        System.out.println("我就要学Java，不要修改我的梦想！");
        str = "Java";
    }
    return str;
}
```

现在我们编写一个环绕方法，对其进行处理：
```java
public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
    System.out.println("我是她的家长，他不能学Java，必须学Rust，这是为他好");
    Object value = joinPoint.proceed(new Object[]{"Rust"});
    if(value.equals("Java")) {
        System.out.println("听话，学Rust以后进大厂！");
        value = "Rust";
    }
    return value;
}
```

同样的，因为方法变动了，现在我们去修改一下我们的AOP配置：
```xml
<aop:pointcut id="test" expression="execution(* org.example.entity.Student.study(String))"/>
<aop:aspect ref="studentAOP">
    <aop:around method="around" pointcut-ref="test"/>
</aop:aspect>
```

![image-20221216162003675](https://oss.itbaima.cn/internal/markdown/2022/12/16/FPwQjRvsDgTnoWx.png)

现在我们来试试看吧：

```java
public static void main(String[] args) {
    ApplicationContext context = new ClassPathXmlApplicationContext("application.xml");
    Student bean = context.getBean(Student.class);
    System.out.println("已报名："+bean.study("Java"));
}
```

![image-20221216161855358](https://oss.itbaima.cn/internal/markdown/2022/12/16/pGl7n8qboe4tuJf.png)

这样，我们就实现了环绕方法，通过合理利用AOP带来的便捷，可以使得我们的代码更加清爽和优美。这里介绍一下 AOP 领域中的特性术语，防止自己下来看不懂文章：

- 通知（Advice） AOP 框架中的增强处理，通知描述了切面何时执行以及如何执行增强处理，也就是我们上面编写的方法实现。- 连接点（join point） 连接点表示应用执行过程中能够插入切面的一个点，这个点可以是方法的调用、异常的抛出，实际上就是我们在方法执行前或是执行后需要做的内容。- 切点（PointCut） 可以插入增强处理的连接点，可以是方法执行之前也可以方法执行之后，还可以是抛出异常之类的。- 切面（Aspect） 切面是通知和切点的结合，我们之前在xml中定义的就是切面，包括很多信息。- 引入（Introduction）：引入允许我们向现有的类添加新的方法或者属性。- 织入（Weaving） 将增强处理添加到目标对象中，并创建一个被增强的对象，我们之前都是在将我们的增强处理添加到目标对象，也就是织入（这名字挺有文艺范的）
## 利用接口实现AOP

前面我们介绍了如何使用xml配置AOP操作，这章我们学习如何使用Advice实现AOP。
它与我们之前学习的动态代理更接近一些，比如在方法开始执行之前或是执行之后调用我们实现的接口，首先我们需要一个类实现Advice接口，只有实现此接口，才可以被通知，比如这里我们使用MethodBeforeAdvice表示是一个方法执行之前的动作：
```java
public class StudentAOP implements MethodBeforeAdvice{
    @Override
    public void before(Method method,Object[] args,Object target) throws Throwable{
        System.out.println("通过Advice实现AOP");
    }
}
```

我们发现，方法中包含了很多参数，其中args代表的方法执行前得到的实参列表，target表示的是执行此方法的实例对象，运行之后，效果和之前是一样的，但是在这里我们可以快速获得更多信息，以study为例：
```java
public class Student {
    public void study(){
        System.out.println("我是学习方法，);
    }
}
```

```xml
<bean id="student" class="org.example.entity.Student"/>
<bean id="studentAOP" class="org.example.entity.StudentAOP"/>
<aop:config>
    <aop:pointcut id="test" expression="execution(* org.example.entity.Student.study())"/>
  	<!--  这里只需要添加我们刚刚写好的advisor就可以了，注意是Bean的名称 -->
    <aop:advisor advice-ref="studentAOP" pointcut-ref="test"/>
</aop:config>
```

我们来测试一下：

![image-20221216164110367](https://oss.itbaima.cn/internal/markdown/2022/12/16/ofducpb2mLh9XHi.png)

除了此接口以外，还有其他的接口，比如`AfterReturningAdvice`就需要实现一个方法执行之后的操作：
```java
public class StudentAOP implements MethodBeforeAdvice, AfterReturningAdvice {
    @Override
    public void before(Method method, Object[] args, Object target) throws Throwable {
        System.out.println("通过Advice实现AOP");
    }

    @Override
    public void afterReturning(Object returnValue, Method method, Object[] args, Object target) throws Throwable {
        System.out.println("我是方法执行之后的结果，方法返回值为，+returnValue);
    }
}
```

因为使用的是接口，就非常方便，直接写一起，配置文件都不需要改了：

![image-20221216164242506](https://oss.itbaima.cn/internal/markdown/2022/12/16/DUZzqaBSiJKNv8j.png)

我们也可以使用MethodInterceptor（同样也是Advice的子接口）进行环绕增强，它用起来就真的像代理一样，例子如下：
```java
public class Student {
    public String study(){
        System.out.println("我是学习方法，);
        return "lbwnb";
    }
}
```

```java
public class StudentAOP implements MethodInterceptor {   //实现MethodInterceptor接口
    @Override
    public Object invoke(MethodInvocation invocation) throws Throwable {  //invoke方法就是代理方法
        Object value = invocation.proceed();   //跟之前一样，需要手动proceed()才能调用原方法        return value+"增强";
    }
}
```

我们来看看结果吧：
![image-20221216173211310](https://oss.itbaima.cn/internal/markdown/2022/12/16/ARcUW2mJrn7Y6f9.png)



使用起来还是挺简单的。
## 使用注解实现AOP

现在我们来看看注解开发AOP，首先，我们在主类添加@EnableAspectJAutoProxy注解，来开启AOP注解支持：
```java
@EnableAspectJAutoProxy
@ComponentScan("org.example.entity")
@Configuration
public class MainConfiguration{
}
```

还是熟悉的用法，类上加上@Component快速注册Bean：
```java
@Component
public class Student{
    public void Study(){
        System.out.println("我是学习方法");
    }
}
```

接着，我们需要在定义AOP增强操作的类上添加@Aspect注解和@Component将其注册为Bean即可：
```java
@Aspect
@Component
public class StudentAOP{
    
}
```

接着，我们可以直接在里面编写增强方法，并将此方法添加到一个切点中，比如我们希望在Student的study方法中执行我们的before方法：
```java
public void before(){
    System.out.println("我是之前执行的内容！");
}
```

那么只需要添加@Before注解即可：
```java
@Before("execution(* org.example.entity.Student.study())")  //execution写法跟之前一样 public void before(){
    System.out.println("我是之前执行的内容！");
}
```

这样，这个方法就会在指定方法执行之前执行了，是不是感觉比XML配置方便多了。我们来测试一下：

```java
public static void main(String[] args) {
    ApplicationContext context = new AnnotationConfigApplicationContext(MainConfiguration.class);
    Student bean = context.getBean(Student.class);
    bean.study();
}
```

![image-20221216165625372](https://oss.itbaima.cn/internal/markdown/2022/12/16/KpiXcdNt7BglYQh.png)

同样的，我们可以为其添加JoinPoint参数来获取切点信息，使用方法和之前一样：

```java
@Before("execution(* org.example.entity.Student.study())")
public void before(JoinPoint point){
    System.out.println("参数列表，+ Arrays.toString(point.getArgs()));
    System.out.println("我是之前执行的内容！");
}
```

为了更方便，我们可以将参数直接放入：

```java
public void study(String str){
    System.out.println("我是学习方法，);
}
```

使用命名绑定模式，可以快速获得原方法的参数：

```java
@Before(value="execution(* org.example.entity.Student.study(..)) && args(str)",argNames="str")
//这是一个传声筒
// args(str)表示上面传入的str，要求传入类型相同（String）//argNames="str"表示传给下面的方法public void before(String str){
    System.out.println(str);   //可以快速得到传入的参数
    System.out.println("我是之前执行的内容！");
}
```

除了@Before，还有很多可以直接使用的注解，比如@AfterReturning、@AfterThrowing等，比如@AfterReturning：
```java
public String study(){
    System.out.println("我是学习方法，);
    return "lbwnb";
}
```

```java
@AfterReturning(value = "execution(* org.example.entity.Student.study())", argNames = "returnVal", returning = "returnVal")   //使用returning指定接收方法返回值的参数returnVal
public void afterReturn(Object returnVal){
    System.out.println("返回值是，+returnVal);
}
```

同样的，环绕也可以直接通过注解声明：
```java
@Around("execution(* com.test.bean.Student.test(..))")
public Object around(ProceedingJoinPoint point) throws Throwable {
    System.out.println("方法执行之前，);
    Object val = point.proceed();
    System.out.println("方法执行之后，);
    return val;
}
```

实际上，无论是使用注解或是XML配置，我们要做的流程都是一样的，在之后的学习中，我们还会遇到更多需要使用AOP的地方。
