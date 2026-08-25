# IoC容器技术
在学习了JavaSE与JavaWeb之后，我们接着来学习Spring框架来进一步搭建我们的知识体系，来简化和规范我们的Java开发。
Spring就是这样一个框架：

（文档：https://docs.spring.io/spring-framework/docs/6.0.10/reference/html/core.html#spring-core）
它就是为了简化开发而生，它是轻量级的*IoC**和*AOP**的容器框架，主要是针对*Bean**的生命周期进行管理的轻量级容器，并且它的生态已经发展得极为庞大。
那么，首先一问，什么是**IoC**和*AOP**，什么又是*Bean**呢？不要害怕，这些概念只是听起来满满的高级感，实际上没有多高级（很多东西都是这样，名字听起来很牛，实际上只是一个很容易理解的东西）

## IoC容器基础

Spring框架的最核心就是IoC容器，它是我们开启Spring学习的第一站。
## IoC理论介绍

在我们之前的Web应用程序中，整个程序其实是依靠各个部分相互协作，共同构成了一个系统；比如，图书管理系统中要展示借阅信息列表，那么首先要使用Servlet进行请求和响应的数据处理，然后请求的数据全部交给Service来处理，当Service需要在数据库中获取数据时，需要向对应的Mapper来发起请求。
它们之间就像是一个齿轮：
![img](https://oss.itbaima.cn/internal/markdown/2022/10/08/YQRP2idIS5skHJ4.png)

像一个团队，每个部件都离不开谁，形成一个高度耦合的体系。
虽然整个体系非常清晰，但是存在一个非常严重的问题，在当下日新月异的时代，所有的技术发展都十分快速，比如由于抖音推出的短视频模式大放异彩，那么几乎所有的软件全部跟进，包括但不限于b站，爱奇艺，甚至美团都有这玩意，虽然十分令人不齿，但是也为我们程序员形成了一个问题，之前写好的代码，都需要进行推翻来重新开发，但是由于这个耦合体系，我们需要进行大面积修改。
比如：
```java
class A{
    private List<B>list;
    public B test<B,b>{
        return null;
    }
    
}
class C{
    public C(A,B){}
    
}
class B{}
```

我们可以看到，A和C都在使用B，如果将来某一天，我们发现B过时了，需要重新更改成更好的D，那么，我们就出现了大面积修改的问题：
由点到面，当一个项目特别庞大时，我们就会消耗大量的时间。
因此，高度耦合带来的缺点也十分明显，想要改善这一情况，我们需要对模块之间进行解耦，让模块与模块之间的粘连不那么强，也就是说，Service的实现类，不再由我们决定，而是让程序自己决定，所有实现类的对象，全部由程序自管理，所有对象之间的关系，让程序动态决定，这样引入了IoC理论。
IoC翻译为：Inversion of Control，译为控制反转，把复杂系统分解成相互合作的对象，这样对象进行封装后，内部实现对外部是透明的，从而降低了解决问题的复杂度：
![img](https://oss.itbaima.cn/internal/markdown/2022/10/08/XsYQRk93CHewISB.png)

我们可以将对象给IoC容器进行管理，比如当我们需要一个接口的实现时，由它根据配置文件来决定到底给我们哪一个实现类，这样，我们就不需要关心我们要去使用哪一个实现类了，我们是需要关心，给到我的一定是一个可以正常使用的实现类。
还是之前的代码，但是有了IoC容器加持后：

```java
public static void main(String[] args){
     A a=new A();
    a.test(IoC.getBean(Service.class));
    //我们从Service中拿到了实现类}
class A{
    private List<Service> list;
    public Service test(Service b){
        return null;
    }
}

interface Service{}
class B implements Service{}
```

当具体的实现类发生修改时，我们同样只需要将新的实现类交给IoC容器管理，这样，我们无需修改前面的任何代码：

```java
interface Service{ }
class D implements Service{}
```

这样，即使我们的底层实现类发生了修改，也不会导致与其相关联的类出现错误，而进行大面积修改，通过定义抽象+容器管理的形式，我们就可以将原有的强关联解除。
高内聚，低耦合，是现代软件开发的设计目标，而Spring框架给我们提供了这样的一个IoC容器进行对象的管理，一个由Spring IoC容器实例化、组装和管理的对象，我们称其为 **Bean**。
## 第一个Spring项目

首先，一定要明确，使用Spring首要目的是对软件项目进行解耦，==不是为了简化代码==。通过它，就可以更好地对我们的Bean进行管理，这一部分我们体验一下Spring的基本使用。
Spring不是一个独立的框架，它实际上包含了很多模块：
![image-20221121233807593](https://oss.itbaima.cn/internal/markdown/2022/11/21/KT2XhuCNVmcSvi5.png)

我们首先学习它的核心内容模块（Core Container），只有了解了Spring的核心技术，我们才能认识到它的便捷之处。
Spring是一个非入侵式的框架，就像一个工具库一样，它可以很简单地加入到我们已有地项目中，因此，我们只需要直接导入其依赖就可以使用了：
```xml
<dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>7.0.0-M9</version>
</dependency>
```

注意，Spring 6要求Java17以上，这个依赖包含以下依赖：

![image-20221122133820198](https://oss.itbaima.cn/internal/markdown/2022/11/22/HszTflPavUdQKGJ.png)

> 如果在使用Spring框架的过程中出现如下警告，>
> ```
> 12月17, 2022 3:26:26 下午 org.springframework.core.LocalVariableTableParameterNameDiscoverer inspectClass
> 警告: Using deprecated '-debug' fallback for parameter name resolution. Compile the affected code with '-parameters' instead or avoid its introspection: XXXX
> ```
>
> 这是因为LocalVariableTableParameterNameDiscoverer在Spring 6.0.1版本已经被标记为过时，并且即将移除，请在Maven配置文件中为编译插件添加`-parameters`编译参数，>
> ```xml
> <build>
>     <pluginManagement>
>         <plugins>
>             <plugin>
>                 <artifactId>maven-compiler-plugin</artifactId>
>                 <version>3.10.1</version>
>                 <configuration>
>                     <compilerArgs>
>                         <arg>-parameters</arg>
>                     </compilerArgs>
>                 </configuration>
>             </plugin>
>         </plugins>
>     </pluginManagement>
> </build>
> ```
>
> 没有此问题请无视这部分。
这里，我们尝试编写一个最简单地Spring项目，我们在前面已经讲过了，Spring会给我们提供IoC容器来管理Bean，但是我们需要先给这个容器编辑一个配置文件，我们可以通过配置文件告诉容器需要管理哪些Bean以及Bean的属性、依赖关系等等。
首先，我们需要在Resource下创建一个Spring配置文件，命名为applicationContext.xml：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd">
</beans>
```

Spring为我们提供了一个IoC容器，用于去存放我们使用的对象，我们可以将对象交给IoC容器进行管理；当我们使用对象时，就可以向IoC容器去索要，并由它决定给我们哪一个对象；而我们如果需要使用Spring为我们提供的对象，那么就需要创建一个应用程序上下文，它代表的就是IoC容器，它会负责实例化、配置和组装Bean：
```java
public class void main(String[] args){
    //ApplicationContext是应用程序上下文的顶层接口，有很多实现，这里我们介绍第一种    //因为这里使用的是XML配置文件（后面还有一种方式），所以用 ClassPathXml...
    ApplicationContext context=new ClassPathXmlApplicationContext("applicationContext.xml");
}
```

这里，我们就在配置文件中编写好了对应的Bean信息，之后容器会根据这里的配置进行处理。
现在，这个对象不需要我们再去创建了，而是由IoC容器自动进行创建并提供，我们可以直接从上下文中获取到它为我们创建的对象：

```java
public static void main(String[] args){
    ApplicationContext context=new ClassPathXmlApplicationContext("applicationContext.xml");
    Student ss=(Student)context.getBean("student");  //使用getBean方法来获取对应的对象。    student.hello();
}
```

getBean中的参数我们在下面讲解。
实际上，这里得到的Student对象是由Spring通过反射机制帮助我们创建的，初学者会非常疑惑，为什么要这样来创建对象，我们直接new一个它不香吗？为什么要交给IoC容器管理呢？在后面的学习中，我们再慢慢进行体会。
![image-20221122153946251](https://oss.itbaima.cn/internal/markdown/2022/11/22/sjLiFokU1f3CvH5.png)

## Bean的注册与配置

前面我们简单的学习了一下如何使用Spring来管理我们的对象，并向IoC容器索要。现在我们学习一下如何向Spring注册Bean以及Bean的配置。
首先，我们还是从简单的配置文件开始，首先，我们需要知道如何配置Bean并注册。
要配置一个Bean，要添加：
```xml
<bean/>
```

然后，我们需要指定一个类：
```xml
<bean class="com.test.bean.Student"/>
```

![image-20221122164149924](https://oss.itbaima.cn/internal/markdown/2022/11/22/SRV3znQJH4A7vDl.png)

可以看到类旁边出现了Bean的图标，表示Bean已经注册成功了，这样，我们可以根据类型内容向Bean来索要对象了：
```java
public static void main(String[] args){
    ApplicationContext context=new ClassPathXmlApplicationContext("applicationContext.xml");
    //getBean有很多种形式，其中一种是根据类型来获取对应的Bean
    Student student=context.getBean(Student.class);
    student.hello();
}
```

不过在有些时候，Bean的获取可能会出现歧义，我们先来注册两个子类：

```java
public class ArtStudent extends Student{
    public void art(){
        System.out.println("我爱画画");
    }
}
```

```java
public class SportStudent extends Student{
		public void sport(){
        System.out.println("我爱运动");
    }
}
```

然后注册子类的Bean：
```xml
<bean class="com.test.bean.ArtStudent"/>
<bean class="com.test.bean.SportStudent"/>
```

但是，此时我们获取Bean时却索要它们的父类：

```java
Student student=context.getBean(Student.class);
student.hello();
```

会出现报错：

![image-20221122164100561](https://oss.itbaima.cn/internal/markdown/2022/11/22/vliWJ4SZdx5E6yX.png)

这里出现了异常：Bean的定义不唯一，很明显，因为我们需要的类型是Student，但是此时有两个Bean定义都满足这个类型，它们都是Student的子类，此时IoC容器不知道给我们返回哪一个Bean，所以就只能抛出异常了。
因此，如果我们需要一个Bean并且使用类型进行获取，那么必须要指明类型并且不能出现歧义：
```java
ArtStudent student = context.getBean(ArtStudent.class);
student.art();
```

要是两个Bean都一样呢，比如说：
```xml
<bean class="com.test.bean.Student"/>
<bean class="com.test.bean.Student"/>
```

或许你会怀疑会出现这种情况吗，但在这里，我们不需要纠结这个，我们需要学习的是，我们可以在这样的情况下给Bean定义名称来区分：

```xml
<bean name="ArtStudent" class="com.test.bean.Student"/>
<bean name="SportStudent" class="com.test.bean.Student"/>
```

name属性就是Bean设定中独一无二的名称（id同样适用，与name不一样的是，id会检查命名规范，不规范会出现黄标）。
不同的Bean名字不能相同，否则报错：

```xml
<bean name="a" class="com.test.bean.Student"/>
<bean name="b" class="com.test.bean.Student"/>
```

这样，这两个Bean我们就可以区分出来了：
```java
Student student = (Student) context.getBean("a");  //强转，还要加双引号student.hello();
```

虽然这两个Bean是一模一样的，但是我们如果后续给两个相同的Bean添加不同的属性，那么二者就不一样了，只能代表二者引用了相同的类型。
我们可以起名字，也可以起小名，正如人类一样：

```xml
<bean name="a" class="com.test.bean.Student"/>
<bean name="a" alias="test"/>
```

这样，我们可以使用别名拿到对应的Bean：
```java
Student student=(Student)context.getBean("test");
student.hello();
```

那么现在，我们又有一个新的问题了：IoC容器创建的Bean是只有一个还是每次索要都会给我们一个新的呢？现在，我们在主方法中连续获取两次Bean对象：
```java
Student student1=context.getBean(Student.class);
Student student2=context.getBean(Student.class);
System.out.println(student1==student2);
```

结果为true，那么显而易见，我们每次从IoC容器中获取到的对象，始终是同一个，默认情况下，通过IoC容器进行管理的Bean都是单例模式，这个对象只会被创建一次。
如果我们希望每次拿到的都是一个新的对象，我们可以将scope属性进行修改：

![image-20221122175719997](https://oss.itbaima.cn/internal/markdown/2022/11/22/hDGo7m9uBlgVn5A.png)

这里一共有两种，第一种是singleton，默认情况下就是这种（单例模式），prototype是原型模式（多例模式），这种模式每次得到的对象都是一个新的。
实际上，当Bean处于单例模式下，那么它会在一开始（容器加载配置时）创建，我们之后拿到的都是这个对象，而处于原型模式下，只有在被获取时才会被创建，也就是说，单例模式下，Bean会被IoC容器存储，只要容器没有被销毁，那么此对象将一直存在，而原型模式才是相当于在要用的时候直接new了一个对象，并不会被保存。
当然，这同样也可以关闭，如果我们不希望一开始就加载，而是等到被需要时才开始加载，（加载后依然会被容器存储，之后一直使用这个对象了，不会再创建新的）我们也可以开启懒加载：
```xml
<bean class="com.test.bean.Student" lazy-init="true"/>
```

开启懒加载后，只有在真正第一次使用时才会创建对象。
由于单例模式下Bean是由IoC容器加载，加载顺序我们并不清楚，如果我们需要维护Bean的加载顺序（比如某个Bean必须要在另一个Bean之前创建）那么我们可以使用`depends-on`来设定前置加载Bean，这样被依赖的Bean一定会在之前加载，比如Teacher应该在Student之前加载：
```xml
<bean name="teacher" class="com.test.bean.Teacher"/>
<bean name="student" class="com.test.bean.Student" depends-on="teacher"/>
```

这样就可以保证Bean的加载顺序了。
## 依赖注入

依赖注入是一种设计模式，也是Spring框架的核心概念之一，现在我们已经了解了如何注册和使用一个Bean，但是这样还不够，还记得我们之前怎么说的吗，消除类之间的强关联吗：
比如说，现在有一个教师接口：

```java
public interface Teacher{
    void teach();
}
```

具体实现有两个：

```java
public class ArtTeacher implements Teacher{
    @Override
    public void teach() {
        System.out.println("我是美术老师，我教你画画，);
    }
}
```

```java
public class ProgramTeacher implements Teacher{
    @Override
    public void teach() {
        System.out.println("我是编程老师，我教你学Golang，);
    }
}
```

我们的学生一开始有一个老师教他，比如美术老师：
```java
public class Student {
    private Teacher teacher = new ArtTeacher();   
  	//在以前，如果我们需要制定哪个老师教我们，直接new创建对应的对象就可以了    public void study(){
        teacher.teach();
    }
}
```

但是我们发现，如果美术老师不教了，现在来了一个其他的老师教学生，那么就需要去修改Student类的定义：
```java
public class Student {
    private Teacher teacher = new ProgramTeacher();
  	...
```

可以想象一下，如果现在冒出很多个这样的类去使用Teacher，一旦Teacher的实现发生变化，会导致所有的类都需要发生改变，这就造成了大量的时间消耗。
而有了依赖注入以后，Student中的Teacher成员变量，可以由IoC容器来选择一个合适的Teacher对象进行赋值，也就是说，IoC容器在创建对象时，需要将我们预设的属性注入到对象中，非常简单，我们可以使用property标签来实现：

```xml
<bean name="teacher" class="com.test.bean.ProgramTeacher"/>
<!--
1. property是student的属性2. property中的name表示给student类中的teacher成员变量进行赋值3. ref引用的是xml配置中的ProgramTeacher，也就是第一行的name
-->
<bean name="student" class="com.test.bean.Student">
    <property name="teacher" ref="teacher"/>
</bean>
```

然后，我们需要修改一下Student的类：
```java
public class Student{
    private Teacher teacher;
    //要使用依赖注入，那就必须提供一个set方法（无论成员变量的访问权限是什么）
    public void setTeacher(Teacher teacher){
        this.teacher=teacher;
    }
}
```

![image-20221122191025279](https://oss.itbaima.cn/internal/markdown/2022/11/22/wu2EYC8HToJbsva.png)

使用property指定（ref）或注入的Bean是ProgramTeacher，那么使用时也是这个对象：
```java
Student student=context.getBean(Teacher.class);
student.study();
```

![image-20221122191109690](https://oss.itbaima.cn/internal/markdown/2022/11/22/n3zYWvIoE8CrRDT.png)

可以看到，在我们的Java代码中，没有出现任何实体类的信息，而是一堆xml配置，现在，就算我们切换老师的实现为另一个类，也不用去调整代码，而是去变动Bean的类型：

```xml
<!--  只需要修改这里的class即可，现在改为ArtTeacher  -->
<bean name="teacher1" class="com.test.bean.ArtTeacher"/>
<bean name="student" class="com.test.bean.Student">
    <property name="teacher" ref="teacher1"/>
</bean>
```

![image-20221122191427776](https://oss.itbaima.cn/internal/markdown/2022/11/22/evKArqDYcIQPCXT.png)

当然，依赖注入也并不一定是其他的Bean，也可以是其他的值：

```xml
<bean name="student" class="com.test.bean.Student">
    <property name="name" value="卢本伟"/>
</bean>
```

直接使用value可以传入一个具体值。
实际上，在很多情况下，类中的某些参数是在构造方法中就已经完成的初始化（也就是说，它变成了有参构造），而不是创建之后，比如说：

```java
public class Student{
    private final Teacher teacher;
    
    public Student(Teacher teacher){  //teacher属性是在构造方法中完成了初始化
        this.teacher=teacher;
    }
}
```

我们前面说了，Bean是由IoC容器来创建的，但是现在我们修改了默认的无参构造，可以看到文件报错：
![image-20221122174328107](https://oss.itbaima.cn/internal/markdown/2022/11/22/5HN8GKQywWaYvrF.png)

很明显，因为我们修改了构造方法，IoC容器默认调用无参构造，但是现在是有参构造，所以，我们需要指定一个可以明确使用的构造方法，我们展开Bean标签，添加一个constructor-arg标签：
```xml
<bean name="teacher" class="com.test.bean.ArtTeacher"/>
<bean name="student" class="com.test.bean.Student">
    <constructor-arg name="teacher" ref="teacher"/>
</bean>
```

这里的constructor-arg就是构造方法的一个参数，这个参数可以写很多个，会自动匹配符合里面参数数量的构造方法，这里匹配的就是我们刚刚写的有参构造。
通过这种方式，我们也能实现依赖注入，只不过我们将依赖注入的时机提前到了对象构造时。
那要是出现这种情况呢，现在我们这样定义一个Student：
```java
public class Student {
    private final String name;
    public Student(String name){
        System.out.println("我是一号构造方法);
        this.name = name;
    }

    public Student(int age){
        System.out.println("我是二号构造方法);
        this.name = String.valueOf(age);
    }
}
```

此时，我们希望使用的是二号构造方法，那么我们如何指定呢？有两种方式，我们可以给标签添加类型：

```xml
<constructor-arg value="1" type="int"/>
```

也可以指定对应的参数名称：
```xml
<constructor-arg value="1" name="age"/>
```

只要能够保证我们指定的参数匹配到目标构造方法中就可以。
现在我们的类中出现了一个比较特殊的类型，它是一个集合类型：

```java
public class Student {
    private List<String> list;

    public void setList(List<String> list) {
        this.list = list;
    }
}
```

对于这种集合类型，有着特殊的支持：

```xml
<bean name="student" class="com.test.bean.Student">
    <property name="list">
        <list>
            <value>AAA</value>
            <value>BBB</value>
            <value>CCC</value>
        </list>
    </property>
</bean>
```

不仅仅是list，Map，Set这类集合，数组也可以，都是支持这样编写的，比如Map类型，我们也可以使用`entry`来注入：

```xml
<bean name="student" class="com.test.bean.Student">
    <property name="map">
        <map>
            <entry key="语文" value="100.0"/>
            <entry key="数学" value="80.0"/>
            <entry key="英语" value="92.5"/>
        </map>
    </property>
</bean>
```

至此，我们就已经完成了两种依赖注入的学习：
- Setter依赖注入：通过成员属性对应的set方法完成注入。- 构造方法依赖注入：通过构造方法完成注入。
## 自动装配 

在之前的学习中，如果我们想使用依赖注入的话，我们需要property参数进行配置：
但是有些时候为了方便，我们也可以开启自动装配，自动装配就是让IoC容器自己去寻找需要填入的值，我们只需要将set方法提供好就可以了，这里需要autowire属性：

```xml
<bean name="student" class="com.test.bean.Student" autowire="byType"/>
```

autowire属性有两个值，一个是byName，一个是byType，顾名思义，一个是根据类型去寻找合适的Bean自动装配，还有一个是根据名字去找，这样我们就不需要显式指定property了。
![image-20221122221936559](https://oss.itbaima.cn/internal/markdown/2022/11/22/QIBRwScq6fu4XDm.png)

此时set方法旁边会显示一个自动装配的图标，效果和上面一样。
对于使用构造方法依赖注入，也支持自动装配：

```xml
<bean name="student" class="com.test.bean.Student" autowire="constructor"/>
```

这个时候，我们只需要提供一个构造方法就可以了，默认也是用byType查找的。
自动化的东西虽然省事，但是太过于机械，有些时候，自动装配可能会遇到以下问题，比如出现下面这种情况：
![image-20221122223048820](https://oss.itbaima.cn/internal/markdown/2022/11/22/SQTchJBq4G8NWyC.png)

此时，由于autowire的规则是byType，存在两个候选Bean，此时我们希望的是ProgramTeacher这个Bean不参与装配中，此时我们需要将它的自动装配候选给关掉：
```xml
<bean name="teacher" class="com.test.bean.ArtTeacher"/>
<bean name="teacher2" class="com.test.bean.ProgramTeacher" autowire-candidate="false"/>
<bean name="student" class="com.test.bean.Student" autowire="byType"/>
```

此时报错消失，正常运行。
除了这种方式，我们也可以设定primary属性，表示这个Bean作为主要的Bean，当出现歧义时，优先选择：
```xml
<bean name="teacher" class="com.test.bean.ArtTeacher" primary="true"/>
<bean name="teacher2" class="com.test.bean.ProgramTeacher" />
<bean name="student" class="com.test.bean.Student" autowire="byType"/>
```

## 生命周期与继承
除了修改构造方法，我们也可以为Bean指定初始化方法和销毁方法，以便在对象创建和销毁时执行一些其他的任务：
```java
public void init(){
    System.out.println("我是对象初始化时要做的事情！");    
}

public void destroy(){
    System.out.println("我是对象销毁时要做的事情！");
}
```

我们可以通过init-method和destroy-method来指定：

```xml
<bean name="student" class="com.test.bean.Student" init-method="init" destroy-method="destroy"/>
```

那么什么时候初始化，什么时候销毁呢：
```java
//当容器被创建时，默认情况下是单例的，那么都会在一开始就加载好，对象构造完成后，会执行init-method
ClassPathXmlApplicationContext context=new ClassPathXmlApplicaitonContext("applicationContext.xml");
//我们可以调用close方法关闭容器，此时容器内存放的Bean也会被一起销毁，会执行destroy-method
context.close();
```

注意，如果Bean是原型模式，那么只会在获取时才创建，并调用init-method，而对应的销毁方法不会被调用，（因此，对于原型模式下的Bean，Spring无法顾及其完整生命周期，而在单例模式下，Spring能够从Bean对象的创建一直管理到对象的销毁）官方文档原文如下：
> In contrast to the other scopes, Spring does not manage the complete lifecycle of a prototype bean. The container instantiates, configures, and otherwise assembles a prototype object and hands it to the client, with no further record of that prototype instance. Thus, although initialization lifecycle callback methods are called on all objects regardless of scope, in the case of prototypes, configured destruction lifecycle callbacks are not called. The client code must clean up prototype-scoped objects and release expensive resources that the prototype beans hold. To get the Spring container to release resources held by prototype-scoped beans, try using a custom [bean post-processor](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-factory-extension-bpp), which holds a reference to beans that need to be cleaned up.

Bean之间也具备继承关系，只不过这里的继承不是类的继承，而是属性的继承，比如：

```java
public class SportStudent {
    private String name;

    public void setName(String name) {
        this.name = name;
    }
}
```

```java
public class ArtStudent {
    private String name;
   
    public void setName(String name) {
        this.name = name;
    }
}
```

此时，我们先将ArtStudent注册一个Bean：
```xml
<bean name="artStudent" class="com.test.bean.ArtStudent">
    <property name="name" value="小明"/>
</bean>
```

此时，我们希望artStudent的bean和sportStudent的bean的name属性一样：

```xml
<bean class="com.test.bean.SportStudent">
    <property name="name" value="小明"/>
</bean>
```

如果属性增多，会变得更加麻烦，这种情况下，我们便可以配置Bean之间的继承关系了，我们可以让SportStudent这个Bean直接继承ArtStudent这个Bean配置的属性：

```xml
<bean class="com.test.bean.SportStudent" parent="artStudent"/>
```

注意：所有配置的属性，在子类中也必须存在，并且可以注入，否则发生错误，当然，如果子类中某些属性比较特殊，也可以在继承的基础上单独配置：

```xml
<bean name="artStudent" class="com.test.bean.ArtStudent" abstract="true">
    <!-- abstract表示不能单独实例化，只能用来继承 -->
    <property name="name" value="小明"/>
    <property name="id" value="1"/>
</bean>
<bean class="com.test.bean.SportStudent" parent="artStudent">
    <property name="id" value="2"/>
    <!-- id被覆盖为2，name保持不变，被继承 -->
</bean>
```

如果，我们希望配置一个Bean作为其他Bean继承的模板来使用，那么我们将其配置为abstract（抽象），这样，容器就不会创建这个Bean对象了：

```xml
<bean name="artStudent" class="com.test.bean.ArtStudent" abstract="true">
    <property name="name" value="小明"/>
</bean>
<bean class="com.test.bean.SportStudent" parent="artStudent"/>
```

注意：一旦声明了这个抽象Bean，就无法通过容器获取其实例化对象了。
![image-20221123140409416](https://oss.itbaima.cn/internal/markdown/2022/11/23/SyDkvOldB7ETW4z.png)

不过Bean的继承使用频率不是很高，了解就行。
这里最后再提一下，我们前面已经学习了各种各样的Bean配置属性，如果我们希望整个上下文中所有的Bean都采用某种配置，我们可以在最外层的beans标签中进行默认配置：

![image-20221123141221259](https://oss.itbaima.cn/internal/markdown/2022/11/23/KzSUJXa4jBfO9rd.png)



这样，即使Bean没有配置某项属性，但是只要在最外层编写了默认配置，那么同样会生效，除非Bean自己进行配置覆盖掉默认配置。
## 工厂模式与工厂Bean

前面我们介绍了IoC容器的Bean的创建机制。默认情况下，容器会调用默认情况下的构造方法进行创建，但是在有些时候，我们可能不希望外界使用类的构造方法完成对象创建，比如在工厂方法设计模式（JAVA设计模式）中我们更希望Spring不要直接利用反射机制通过构造方法创建Bean对象，而是利用反射机制先找到对应的工厂类，然后利用工厂类生成需要的Bean对象：（换个说法来讲，工厂类 Bean 是“被 Spring 管理的、专门用来生产其他Bean 的对象”。）

```java
public class Student {
    Student() {
        System.out.println("我被构造了");
    }
}
```

```java
public class StudentFactory {
    public static Student getStudent(){
      	System.out.println("欢迎光临电子科技大学");
        return new Student();
    }
}
```

```xml
<bean class="com.test.bean.StudentFactory" factory-method="getStudent"/>
```

此时Student有一个工厂，我们正常情况下需要使用工厂才可以得到Student对象，现在我们需要Spring也这样做，不要直接去反射搞构造方法创建，我们可以通过factory-method进行指定。
注意，这里的Bean类型需要填写为Student类的工厂类，并且添加factory-method指定对应的工厂方法，但是最后注册的是工厂方法的返回类型，所以说依然是Student的Bean：
![image-20221123143302785](https://oss.itbaima.cn/internal/markdown/2022/11/23/5Id43xPneJiWfZs.png)

此时我们再去进行获取，拿到的也是通过工厂方法得到的对象：

![image-20221123143347376](https://oss.itbaima.cn/internal/markdown/2022/11/23/l8HzN7Rwthqrim5.png)



这里有一个误区，千万不要认为是我们注册了StudentFactory这个Bean，class填写这个类只是为了告诉Spring我们的工厂方法在哪个位置，真正注册的是工厂方法提供的东西。
可以发现，当我们采用工厂模式后，我们就无法再通过配置文件对Bean进行依赖注入等操作了，而是只能在工厂方法中完成，这似乎与Spring的设计理念背道而驰：
当然，可能某些工厂类需要构造出对象之后才能使用，我们也可以将某个工厂类直接注册为工厂Bean：
```java
public class StudentFactory {
    public Student getStudent(){
        System.out.println("欢迎光临电子科技大学");
        return new Student();
    }
}
```

现在需要StudentFactory对象才可以获取到Student，此时我们就只能先将其注册为Bean了：

```xml
<bean name="studentFactory" class="com.test.bean.StudentFactory"/>
```

像这样将工厂类注册为Bean，我们称其为工厂Bean，然后再使用`factory-bean`来指定Bean的工厂Bean：
```xml
<bean factory-bean="studentFactory" factory-method="getStudent"/>
```

注意，使用factory-bean之后，不再要求指定class，我们可以直接使用了：
![image-20221123164134470](https://oss.itbaima.cn/internal/markdown/2022/11/23/ih1Af7xBdX3ebaG.png)



此时可以看到，工厂方法上同样有了图标，这种方式，由于工厂类被注册为Bean，此时我们就可以在配置文件中为工厂Bean配置依赖注入等内容了。
这里还有一个很细节的操作，如果我们想获取工厂Bean为我们提供的Bean，可以直接输入工厂Bean的名称，这样不会得到工厂Bean的实例，而是工厂Bean生产的Bean的实例：

```java
Student bean = (Student) context.getBean("studentFactory");
```

当然，如果我们需要获取工厂类的实例，可以在名称前面添加`&`符号：
```java
StudentFactory bean = (StudentFactory) context.getBean("&studentFactory");
```

又是一个小细节。
## 使用注解
前面我们已经完成了大部分的配置学习，但是我们发现，使用配置文件进行配置，貌似有点累了，因为当一个项目非常庞大时，需要配置大量的文件，我们能否有一种更加高效的方法省去配置呢？有的兄弟有的，就是注解。
那么，现在我们删除xml配置文件，看看如何使用注解。
```java
ApplicationContext context=new AnnotationConfigApplicationContext();
```

既然现在采用注解，我们需要使用类来编写配置文件，在之前的学习中，我们这样配置的：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd">
</beans>
```

现在，我们需要配置一个类：
```java
@Configuration
public class MainConfiguraiton{
}
```

这两者是等价的。
我们可以为AnnotationConfigApplicationContext指定一个默认的配置类：

```java
ApplicationContext context = new AnnotationConfigApplicationContext(MainConfiguration.class);
//这个构造方法可以接收多个配置类（更准确的说是多个组件）
```

那么，我们如何配置bean呢？

```java
@Configuration
public class MainConfiguration{
    @Bean("student")
    public class Student student{
        return new Student();
    }
}
```

这就相当于：

```xml
<bean name = "student" class="com.test.bean.Student"/>
```

通过@Import还可以引入其他配置类：
```java
@Import(LBWConfiguration.class)  //在讲解到Spring原理时，我们还会遇到它，目前只做了解即可。@Configuration
public class MainConfiguration {
```

只不过变成了由Java代码来为我们提供Bean配置，这样会更加灵活，也更加便于控制Bean对象的创建。
```java
ApplicationContext context=new AnnotationConfigApplicationContext(MainApplication.class);
Student student=context.getBean("student");
System.out.println(student);
```

使用方法是相同的。
那么肯定会有人好奇，我们之前那么多属性是在哪里配置呢？首先，初始方法、毁灭方法以及自动装配可以直接在@Bean注解中进行配置：

```java
@Configuration
public class MainConfiguration{
    @Bean(name="student",initMethod="",destroyMethod="",autowireCanditate=false)
    public class Student student{
        return new Student();
    }
}
```

其次，其他的属性需要我们在注解中进行开发：

```java
@Bean
@Lazy(true)     //对应lazy-init属性@Scope("prototype")    //对应scope属性@DependsOn("teacher")    //对应depends-on属性public Student student(){
    return new Student();
}
```

对于那些我们需要通过构造方法或是Setter完成依赖注入的Bean，比如：

```xml
<bean name="teacher" class="com.test.bean.ProgramTeacher"/>
<bean name="student" class="com.test.bean.Student">
    <property name="teacher" ref="teacher"/>
</bean>
```

像这种需要引入其他Bean进行的注入，我们可以直接将其作为形参放到方法中：

```java
@Configuration
public class MainConfiguration {
    @Bean
    public Teacher teacher(){
        return new Teacher();
    }

    @Bean
    public Student student(Teacher teacher){
        return new Student(teacher);
    }
}
```

运行正常。
只不过，除了这种基于构造器或者Setter方法的注入之外，我们可以直接到Bean对应的类中进行自动装配：

```java
public class Student {
    @Autowired   //使用此注解来进行自动装配，由IoC容器自动为其赋值    private Teacher teacher;
}
```

@Resource与@Autowired的区别：

1. 来源不同：@Resource 和 JDK 自带的注解（属于 javax.annotation 包），@Autowired 是Spring 提供的；
2. 匹配规则不同：@Resource 默认先按「名称」匹配（比如属性名 student，就是name/ID 就是 name/ID 为 student 的Bean），找不到再按「类型」匹配；而@Autowired 默认先按「类型」匹配。
现在，我们甚至连构造方法和Setter都不需要去编写了，就能直接完成自动装配，是不是感觉比那堆配置方便多了？

当然，@Autowired并不是只能用于字段，对于构造方法或是Setter，它同样可以：
```java
public class Student {
    private Teacher teacher;

    @Autowired
    public void setTeacher(Teacher teacher) {
        this.teacher = teacher;
    }
}
```

@Autowired默认采用byType进行自动装配，那么要是出现了许多相同的Bean，只用其中的一个该如何使用呢？

```java
@Bean("a")
public Teacher teacherA(){
    return new Teacher();
}

@Bean("b")
public Teacher teacherB(){
    return new Teacher();
}
```

此时，我们可以配合@Qualifier进行名称匹配：
```java
public class Student {
    @Autowired
    @Qualifier("a")   //匹配名称为a的Teacher类型的Bean
    private Teacher teacher;
}
```

有@PostConstruct和@PreDestroy，它们效果和init-method和destroy-method是一样的：
```java
@PostConstruct
public void init(){
    System.out.println("我是初始化方法);
}

@PreDestroy
public void destroy(){
    System.out.println("我是销毁方法);
}
```

我们只需要将其添加到对应的方法上即可：
```java
AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(MainConfiguration.class);
Student student = context.getBean(Student.class);
context.close();
```

![image-20221123225232979](https://oss.itbaima.cn/internal/markdown/2022/11/23/wXRuAjVF2ykCOJ4.png)



可以看到效果是完全一样的，这些注解都是jakarta.annotation提供的，有关Spring和JakartaEE的渊源，还请各位小伙伴自行了解。
前面我们介绍了使用@Bean来注册Bean，但是实际上我们发现，如果只是简单将一个类作为Bean的话，这样写还是不太方便，因为都是固定模式，就是单纯的new一个对象出来，能不能像之前一样，让容器自己反射获取构造方法去生成这个对象呢？

肯定是可以的，我们可以在需要注册为Bean的类上添加@Component注解来将一个类进行注册（现在最常用的方式），不过要实现这样的方式，我们需要添加一个自动扫描来告诉Spring，它需要在哪些包中查找我们提供的@Component声明的Bean。
```java
@Component("lbwnb")
public class Student{
}
```

要注册这个类的Bean，只需要添加@Component即可，然后配置一下包扫描：
```java
@Configuration
@Component("com.test.bean")  //包扫描，这样Spring就会去扫描对应包下的所有类
```

Spring在扫描对应包下的所有类时，会自动那些添加了@Component的类注册为Bean。只不过这种方式只适用于我们自己编写类的情况，如果是第三方包提供的类，只能使用前者完成注册，并且这种方式不太灵活。
不过，无论是通过@Bean还是@Component形式注册的Bean，Spring都会为其添加一个默认的name属性，比如：
```java
@Component
public class Student{
    
}
```

此时，他给Student这个类添加了name属性为student（小驼峰命名法）：
```java
Student student=(Student)context.getBean("student");
System.out.println(student);
```

同样的，如果通过@Bean注册，默认名称是对应的方法名称：

```java
@Bean
public Student artStudent(){
    return new Student();
}
```

```java
Student student=(Student)context.getBean("artStudent");
System.out.println(student);
```

相比于传统的XML配置方式，注解形式的配置确实能够减少我们很多工作量。并且，对于这种使用@Component注册的Bean，如果其构造方法不是默认无参构造，那么默认会对其每一个参数都进行自动注入：
```java
@Component
public class Student{
    Teacher teacher;
    public Student(Teacher teacher){  //如果由Teacher类型的Bean，那么这里的参数会被自动注入
        this.teacher=teacher;
    }
}
```

最后，对于我们之前使用的工厂模式，Spring也提供了接口，我们可以直接实现接口表示这个Bean是一个工厂Bean：
```java
@Component
public class StudentFactory implements FactoryBean<Student> {
    @Override
    public Student getObject() {   //生产的Bean对象
        return new Student();
    }

    @Override
    public Class<?> getObjectType() {   //生产的Bean类型
        return Student.class;
    }

    @Override
    public boolean isSingleton() {   //生产的Bean是否采用单例模式
        return false;
    }
}
```

实际上跟我们之前在配置文件中编写是一样的，这里就不多说了。
请注意，使用注解虽然可以省事很多，代码也能变得更简洁，但是这并不代表XML配置文件就是没有意义的，它们有着各自的优点，在不同的场景下合理使用，能够起到事半功倍的效果，官方原文：

> Are annotations better than XML for configuring Spring?
>
> The introduction of annotation-based configuration raised the question of whether this approach is “better” than XML. The short answer is “it depends.” The long answer is that each approach has its pros and cons, and, usually, it is up to the developer to decide which strategy suits them better. Due to the way they are defined, annotations provide a lot of context in their declaration, leading to shorter and more concise configuration. However, XML excels at wiring up components without touching their source code or recompiling them. Some developers prefer having the wiring close to the source while others argue that annotated classes are no longer POJOs and, furthermore, that the configuration becomes decentralized and harder to control.
>
> No matter the choice, Spring can accommodate both styles and even mix them together. It is worth pointing out that through its [JavaConfig](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-java) option, Spring lets annotations be used in a non-invasive way, without touching the target components source code and that, in terms of tooling, all configuration styles are supported by the [Spring Tools for Eclipse](https://spring.io/tools).

至此，关于Spring的IoC基础部分，我们就全部介绍完了。在最后，留给各位一个问题，现在有两个类：
```java
@Component
public class Student {
    @Resource
    private Teacher teacher;
    
}
```

```java
@Component
public class Teacher {
    @Resource
    private Student student;
}
```

这两个类互相需要注入对方的实例对象，这个时候Spring会怎么进行处理呢？如果Bean变成原型模式，Spring又会怎么处理呢？

这个问题我们会在实现原理探究部分进行学习。
