# jUnit单元测试

随着我们项目的逐渐变大，我们都是一边写一边测试，而测试的主要方法，就是启动main直接测试。但是，在很多情况下，我们的项目可能会很庞大，不可能每次都去完整的启动一个项目来测试某一个功能，这样显然会降低我们的开发效率，因此，我们需要使用的那远测试，帮助我们针对某一个功能单独运行代码进行测试，而不是启动整个项目，比如：
```java
public class Main{
    public static void main(String[] args){
        System.out.println("Hello World");
        func1();
        func2();
        func3();
    }
    
    private static void func1(){
        System.out.println("我是第一个功能);
    }
    private static void func1(){
        System.out.println("我是第二个功能);
    }
    private static void func1(){
        System.out.println("我是第三个功能);
    }
}
```

单元测试，可以针对某一个方法进行测试运行，而不需要让整个项目跑起来。

## 初次使用JUnit

使用很简单，在导入JUnit依赖以后，我们只需要添加一个`@Test`注解就可快速创建测试用例：

```java
@Test
public void test1(){
    Main.func1();
}
```

此时，IDEA会在最左边放置一个启动按钮，![QQ_1724828793159](https://oss.itbaima.cn/internal/markdown/2024/08/28/Q6uP3yz1NTVIqDF.png)

接着，点击运行，那就可以直接执行我们的测试方法了：

![QQ_1724834749820](https://oss.itbaima.cn/internal/markdown/2024/08/28/WQoIXkt1iBjmO89.png)

一个测试类种可以同时存在很多个测试案例：

```java
public class MainTest {

    @Test
    public void test1(){
        Main.func1();
    }

    @Test
    public void test2(){
        Main.func2();
    }

    @Test
    public void test3(){
        Main.func3();
    }
}
```

我们可以点击类旁边的运行按钮，可以执行当前类种所有的测试案例：

![QQ_1724839789746](https://oss.itbaima.cn/internal/markdown/2024/08/28/X1Anuvgohb6OyF2.png)

有些时候，如果不想开启三个中的某一个测试案例，我们可以使用`@Disable`来关闭：

```java
@Test
@Disable
public void test2(){
}
```

此时，将忽略二号测试案例：

![QQ_1725176910092](https://oss.itbaima.cn/internal/markdown/2024/09/01/oYsG2yTtpEXknA1.png)

我们同样可以为测试案例添加一个自定义名称，使用`@DisplayName`注解来为其命名：

```java
@Test
@DisaplayName("这是一个快乐的测试案例")
public void test1(){}
```

![QQ_1724839198905](https://oss.itbaima.cn/internal/markdown/2024/08/28/GKXxyd9AQSMeHOE.png)

除此之外，JUnit还提供了一些预设的名称生成器，可以通过`@DisplayNameGeneration`注解来配置使用：

- `Standard`-方法名称作为测试名称
- `Simple`-同上，但是会删除无参数方法的尾随括号
- `ReplaceUnderscores`-同上，但是会用空格替代下划线
- `IndicativeSentences`-包含类名和方法名称连接之后的名称

## 断言工具类

当然，对于一个测试案例来说，我们肯定希望测试的结果是我们所期望的一个值，因此，如果测试的结果并不是我们所期望的结果，那么这个测试就应该没有成功，我们可以通过断言工具类`Assertions`来对结果进行判定：

```java
@Test
public void test1(){
    Random radom=new Random();
    int value=random.nextInt()%2;  //生成一个随机数，进行对2取余操作
    Assertions.assertEquals(1,value);  //如果是单数则匹配成功，否则匹配失败
}
```

当测试案例失败时：

![QQ_1724838573199](https://oss.itbaima.cn/internal/markdown/2024/08/28/8usXgxHIePUZVAk.png)

JUnit为我们提供了非常多的断言操作，这些断言操作基本上是用于判断某个测试结果是否符合我们的预期状况，其中最简单的就是判断某个结果是否符合某个值：

```java
@Test
public void test1(){
    int a=10,b=5;
    int c=a+b;
      //判断结果是否相等，前面是预期结果，后面是实际结果
    Assertions.assertEquals(15,c);
}
```

我们同样也可以为本次断言添加一个message来助于我们快速了解是什么类型的测试结果出现了问题：

```java
Assertions.assertEquals(14,c,"计算机结果验证);
```

![QQ_1725178634235](https://oss.itbaima.cn/internal/markdown/2024/09/01/MlftC67rANvuGao.png)

除了使用值进行比较之外，我们也可以直接对某个boolean类型的结果快速判断，使用`assertTrue`方法：

```java
Assertions.assertTrue(14==c,"计算机结果验证);
```

还有一个是两个相同对象的判断：

```java
Assertions.asserSame(999,999);  //判断两个值是否为同一个对象
```

注意：在Java中，对于-128到127之间的整数，Integer类中有一个缓存机制，会预先创建这些数值的Integer对象并缓存起来，当使用自动装箱或者Integer.valueOf()方法创建这个范围内的整数对象时，会自动返回缓存中的对象，而不是创建新的对象。

因此，999会返回false，123则会返回true。

如果判断流程比较复杂，我们可以使用Lambda来编写结果：

```java
Assertions.assertTrue(()->{
    if(c<10) return true;
    if(c>20) return false;
    return c==15;
},"计算机结果验证");
```

对于更加复杂的组合结果判断，我们使用`assertAll`来包含多个判断操作：

```java
Assertions.assertAll("整体测试",
                    ()->Assertions.assertTrue(c==14),
                    ()->Assertions.assertTrue(c<10),
                    ()->Assertions.assertTrue(c>20)
);
```

除了我们上面提到的真假判断外，还有很多不同类型的结果判断，比如异常判断，我们希望这个案例抛出指定的异常：

```java
Assertions.assertThrows(IOException.class,()->{
    System.out.println(1/0);  //空指针异常
},"此测试案例并未抛出指定异常)：
```

![image-20241115174848264](https://oss.itbaima.cn/internal/markdown/2024/11/15/VwkAoeGIzChBtq2.png)

JUnit还提供了包括上述断言但不限于，这里不一一介绍了。

除了断言工具外，对于一些不影响结果的测试，我们可以使用假设工具来实现对结果的判断但不作为测试结果的判断依据，它通常在执行给定测试没有意义时才使用。

```java
public void test1(){
    Assumption.assumeTrue(1==3);
}
```

测试结果会将其显示已忽略，而不是失败：

![image-20241115222449539](https://oss.itbaima.cn/internal/markdown/2024/11/15/urBZYCMxmNGKP8v.png)

## 条件测试和执行

有些时候，我们可能需要配置各种条件来执行某些测试案例，比如某些测试案例必须指定JDK版本执行，或是某些案例只需要在某个特性的操作系统执行，JUnit为我们提供了这些条件。

比如，限制在Windows或者Mac上执行下进行，我们可以使用`EnabledOnOs`来指定：

```java
@Test
@EnabledOnOs(OS.MAC)
public void test1(){
    System.out.println("我只在MAC上执行);
}

@Test
@EnabledOnOs(OS.WINDOWS)
//@DisabledOnOs(OS.MAC)与上一行同上
public void test2(){
    System.out.println("我只在WINDOWS下执行);
}
```

同样的，如果我们要指定在某个JDK下执行，我们可以使用`@EnableOnJre`来指定：

```java
@Test
@EnabledOnJre(JRE.JAVA_8)
//@DisabledOnJre(JRE.JAVA_8)指定关闭java8的JDK
public void test1(){
    System.out.println("我是只在Java8下执行的测试案例");
}

@Test
@EnabledOnJre(JRE.JAVA_17)
public void test2(){
    System.out.println("我是只在Java17下执行的测试案例");
}
```

或者一个指定的JDK范围：

```java
@Test
@EnabledForJreRange(min=JRE.JAVA_8,max=JRE.JAVA_17)
public void test1(){
    System.out.println("我只在Java8-17下成功执行");
}
```

初次之外，我们可以直接从系统属性中获取我们需要的参数来判断。

> 使用System.getProperties()来获取所有的系统属性，包括系统的架构，版本，名称等信息。

使用`@EnabledIfSystemProperty`来对系统属性进行判断：

```java
@Test
@EnabledIfSystemProperty(named="os.arch",matches="aarch64");
//其中matches参数支持正则表达式
public void test1(){
    System.out.println("我只在arm64架构下测试);
}
```

当然，为了方便，我们可以直接读取环境变量：

```java
@Test
@EnabledIfEnvironmentVariable(named="TEST_STR",matches="666")
public void test1(){
    System.out.println("我是只在环境变量: TEST_STR = 666");
}
```

如果你认为还不够灵活，我们可以直接声明一个自定义方法来进行判断：

```java
@Test
@EnabledIf("testCondition")
public void test1(){
    System.out.println("我是自定义的测试条件");
}

public boolean testCondition(){
    return 1>0;
}
```

>条件方法可以位于测试类之外。在这种情况下，他必须用其完全限定的名称来引用。（就是放在两个不同的java文件下）
>
>```java
>@EnabledIf("example.ExternalCondition#customCondition")
>```
>
>```java
>xclass ExternalCondition{
>    //在这几种情况下，条件方法要使用static：
>    //当@EnabledIf在类上使用时
>    //当@EnabledIf用于@ParameterizedTest或@TestTemplate方法上
>    //当条件方法位于外部类上
>    static boolean customCondition(){
>        return true;
>    }
>}
>```
>
>

## 生命周期、顺序控制和嵌套测试

我们可以自由设定某些操作在测试之前执行还是测试之后：

```java
@Test
public void test1(){
    Systen.out.println("我是测试方法1");
}

@BeforeAll  //使用BeforeAll必须为static方法
public static void start(){
    System.out.println("我是测试前必须要执行的工作);
}
```

其中，`@BeforeAll`表示此准备工作在所有测试用例执行之前执行，这样，当测试开始前，会优先进行指定的准备工作，相反的，`AfterAll`表示所有测试用例完成之后执行。

除了在所有方法前后插入准备工作，还可以为所有的方法单个插入准备工作：

```java
@BeforeEach  //使用BeforeEach不能为static方法
public void start(){
    System.out.println("我是测试前必须要执行的准备工作);
}
```

这样，每个测试案例执行之前，都会执行一次准备工作：

![image-20241116004216666](https://oss.itbaima.cn/internal/markdown/2024/11/16/Kw2S1lxy3AbOI5n.png)

我们接着来了解一下测试类的生命周期。默认情况下，执行测试实际上也会对类进行实例化，并通过实例化对象来调用其中的测试方法，并且，每一个测试用例执行之前，都会创建一个新的对象，而不是直接执行：

```java
public class MainTest{
    
    public MainTest(){
        System.out.println("AAA");
    }
}
```

![image-20241116004839643](https://oss.itbaima.cn/internal/markdown/2024/11/16/yGfK7EvemLFwpCt.png)

每次执行测试用例都会创建一个新的对象来执行，在某些场景下可能不太方便，比如初始化类需要大量时间执行非常费时间的IO操作，这会导致我们要花费大量时间来而等待每次测试用例的初始化操作。我们也可以手动更改测试类的初始化行为，默认情况下`PER_METHOD`模式：

```java
@TestInstance(TestInstance.Liftcycle.PER_CLASS)
public class MainTest{
}
```

将其修改为`PER_CLASS`模式后，初始化操作只会执行一次，因为现在是以类为单位：

![image-20241116005150384](https://oss.itbaima.cn/internal/markdown/2024/11/16/8SyYQUWC2lLeEnB.png)

有时候，我们可能需要控制某些测试案例的顺序，默认情况下，所有的测试案例都是按照方法的名称顺序来进行的：

```java
@Test
public void test3() {  //按照名称顺序，虽然这里是第一个定义的，但是它是第三个
    System.out.println("我是测试用例3");
}

@Test
public void test1() {
    System.out.println("我是测试用例1");
}

@Test
public void test2() {
    System.out.println("我是测试用例2");
}
```

除了默认的名称顺序之外，JUnit提供了以下顺序：

- `MethodOrderer.DisplayName`：根据显示名称对测试方法进行*字母数字*排序（请参阅[显示名称生成优先级规则](https://junit.org/junit5/docs/current/user-guide/#writing-tests-display-name-generator-precedence-rules)）
- `MethodOrderer.MethodName`：根据测试方法的名称和形式参数列表，*以字母数字排序
- `MethodOrderer.OrderAnnotation`：根据通过`@Order`注释指定的值对测试方法*进行数字排序
- `MethodOrderer.Random`，伪随机排序测试方法，并支持自定义种子*的配置

其中，注解顺序可以由我们自己通过注解来手动定义执行顺序：

```java
@Test
@Order(1)
void nullValues(){
    //perform assertions against null values
}
```

有些时候我们可能需要对测试用例进行进一步的分层，比如用户相关的测试全部归为一个组，而管理相关的测试全部归为一个组，此时我们可以嵌套测试，通过在类中定义多个内部类来完成：

```java
public class MainTest {

    @Test
    public void test() {
        System.out.println("我是外部测试类型");
    }

    @Nested
    class Test1 {

        @Test
        public void test1_1() {
            System.out.println("我是内部测试类型1-1");
        }

        @Test
        public void test1_2() {
            System.out.println("我是内部测试类型1-2");
        }
    }

    @Nested
    class Test2 {
        @Test
        public void test2_1() {
            System.out.println("我是内部测试类型2-1");
        }

        @Test
        public void test2_2() {
            System.out.println("我是内部测试类型2-2");
        }
    }
}
```

此时测试的结果也是嵌套类型的样式：

![image-20241116001214709](https://oss.itbaima.cn/internal/markdown/2024/11/16/35vkn4qQzlbVrif.png)

## 重复和参数化测试

对于某些存在随机性的测试案例，我们可能需要多次执行才能确定其是否存在某些问题，比如某些案例存在一个BUG，导致其10次里面有1次出现错误，现在我们想要保证10次都不会出现问题才算通过，此时我们就可以使用重复测试案例来使其多次执行：

```java
@RepeatedTest(10)
public void test1(){
    Random random=new Random();
    if(random.nextInt(10)==0){
        throw new IllegalStateException();
    }
}
```

此时，会重复执行10次此案例，并且当每一次执行都没有出现问题时，才会正常通过：

![image-20241116010355502](https://oss.itbaima.cn/internal/markdown/2024/11/16/iLSas1TzdHtOgUI.png)

某些测试可能并不是固定单个输入参数，有时我们可能会需要对多个输入参数进行测试，来做到全方面的问题排查。它与重复测试必将类似，但是参数可以由我们自己决定：

```java
@ParameterizedTest  //使用此注解来表示此测试是一个参数化测试
@ValueSource(String ={"aa","bb","ccc"})
public void test1(String str){  //需要添加一个参数
    if(str.length()==3){
        throw new IllegalStateException();
    }
}
```

这里我们使用`@ValueSource`来进行参数来源设定，也就是需要测试的参数列表，接着下面会根据参数挨个执行测试用例，保证每一种情况正常执行：

![image-20241116021604397](https://oss.itbaima.cn/internal/markdown/2024/11/16/iT3UvfHc2Ns4koS.png)

 这里的`@ValueSource`是最简单的一种参数设定，我们可以直接设置一系列值，支持以下类型：short,byte,int ,long,float,double,char,boolean,java.lang.String,java.lang.Class

除了直接设定指定类型常量值，我们也可以传入空值或是一些为空的字符串，数组等：

```java
@ParameterizedTest
@NullSource  //将设置为null进行测试,包括空字符串，空数组，空集合
public void test1(String str){
    
}
```

> @NullAndEmptySource:结合了@NullSource和@EmptySource两个注解的功能。

我们也可以使用枚举值来进行测试，比如我们希望测试某个枚举类型下所有的枚举作为参数进行测试：

```java
enum Type{
    SWALL,MEDIUM,LARGE
}
@parameterizedTest
@EnumSource(Type.class)
public void test1(Type type){
    System.out.println(type);
}
```

或是指定某些枚举常量：

```java
@ParameterizedTest
//模式默认为INCLUDE，即使用指定的枚举常量进行测试
@EnumSource(mode==EnumSource.Mode.INCLUDE,names={"SWALL","LARGE"})
public void test1(Type type){
    System.out.println(type);
}
```

```java
@ParameterizedTest
@MethodSource("stringProvider")
public void test1(String str) {
    System.out.println(str);
}

static List<String> stringProvider() {
    return List.of("apple", "banana");
}
```

方法的返回值是任何可迭代的内容，对于其他类中的方法，需要和之前一样使用完全限定的方法名称来引用。

和方法一样，字段也可以作为参数的来源，但他必须是静态的：

```java
static List(String)list=List.of("AAA","BBB");

@ParameterizedTest
@FiledSource("list")
public void test1(String str){
    System.out.println(str);
}
```

不仅仅是一个普通的集合或是数组可以作为字段参数来源，如Supplier这种懒加载的数据，也可以作为参数来源：

```java
static Supplier<List<String>> list = () -> List.of("AAA", "BBB");

@ParameterizedTest
@FieldSource("list")
public void test1(String str) {
    System.out.println(str);
}
```

当然，JUnit还支持从CSV表格中导入或自定义参数提供器等，这里就不做详细介绍了，官方文档：https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests-sources-ArgumentsSource
