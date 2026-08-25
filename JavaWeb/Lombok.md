# Lombok

本次知识点讲解基于Java17。

我们不难发现，在以往编写项目时，尤其是在类内部成员字段封装时，需要编写大量get/set方法，之不竭使我们类定义中充满了get和set方法，同样如果字段名称发生了改变，都要进行挨个修改，甚至如果字段变多，编写会十分麻烦。

此时，通过记录类型可以快速得到一个带有自带构造方法，getter以及重写toString等方法的类：

```java
public record Account(int id,String name,int age,String gender,String password){}
```

此时，虽然不用手写一部分代码了，但是它依然不够灵活，尤其是最关键的Setter也并未生成。

那么，此时可以通过Lombok（小辣椒），他就是专门用于简化Java中的样板代码的，通过注解的方式，能够自动生成常见的代码。官网地址：https://projectlombok.org

使用了Lombok以后，你的代码变成了这样：

```java
@Getter
@Setter
@AllArgsConstructor
```

使用Lombok提供的注解，即可一步到位，直接生成对应的Getter，Setter包括构造方法，toString都可以全包。

那么Lombok是如何做到一个注解就包揽了代码生成工作的呢？这里又要说到我们Java的编译过程，它可以分成三个阶段：

![img](https://oss.itbaima.cn/internal/markdown/2024/08/05/6HwkaOh9SJ7XCRm.png)



1. 所有源文件会被解析成语法树。
2. 调用注解处理器。如果注解处理器产生了新的源文件，新文件也要进行编译。
3. 最后，语法树会被分析并转化成类文件。

Lombok会在上述的第二阶段，执行*[lombok.core.AnnotationProcessor](https://github.com/rzwitserloot/lombok/blob/master/src/core/lombok/core/AnnotationProcessor.java)*，它所做的工作就是我们上面所说的，修改语法树，并将注解对应需要生成的内容全部添加到类文件中，这样，我们即使没有在源代码中编写的内容，也会存在于生成出来的class文件中。

## 类属性相关

我们首先从类属性相关注解开始介绍，首先`@Getter`，他用于自动生成Getter，定义如下：

```java
@Target({ElementType.FIELD, ElementType.TYPE})   //此注解可以添加在字段或是类型上
@Retention(RetentionPolicy.SOURCE)
public @interface Getter {
    AccessLevel value() default AccessLevel.PUBLIC;  //自动生成的Getter的访问权限级别
    AnyAnnotation[] onMethod() default {};  //用于添加额外的注解
    boolean lazy() default false;   //懒加载功能
    ...
}
```

它最简单的用法，就是直接添加到类或者字段上：

```java
@Getter  //添加到类上时，将为类中所有字段添加Getter方法
public class Account{
    private int id;
    @Getter  //当添加到字段上时，仅对此字段生效
    private String name;
    pirvate int age;
}
```

此时，我们打开.class为后缀的编译文件：

```java
import lombok.Generated;

public class Account {
    private int id;
    private String name;
    private int age;

    public Account() {}

    @Generated
    public int getId() {   //自动为所有字段生成了对应的Getter方法
        return this.id;
    }

   // ...省略
}
```

是不是感觉很方便，注意：它存在一定的命名规则，如果该字段为foo，那么将其直接按照字段名称命名为getFoo，但是注意，如果字段是boolean，那么命名为isFoo。

我们接下来看看Getter注解的其他属性，首先是访问权限，默认下为public，但是有时候我们希望生成的权限为private，此时我们可以对其进行修改：

- PUBLIC - public
- PACKAGE- 相当于不添加任何访问权限关键字
- PRIVATE-private
- PROTECTED-protected
- MODULE-仅限模块内使用，于package相同
- NONE-表示不生成对应的方法，这很适合对类中不需要生成的字段进行排除

```java
@Getter(AccessLevel.PRIVATE) //为所有属性生成为private的getter方法
public class Account{
    private int id;
    @Getter(AccessLevel.NONE)  //不为name生成Getter方法
    private String name;
    private int age;
}
```

生成的结果是：

```java
public class Account {
    private int id;
    private String name;
    private int age;

    public Account() {
    }

    private int getId() {   //得到的就是private的Getter方法
        return this.id;
    }

    ...
}
```

我们接下来看看onMethod属性，这个属性用于添加一些额外的注解到生成的方法上，比如说，我们要为Getter方法添加一个额外的@Deprecated，表示它不推荐使用：

```java
@Getter
public class Account{
    private int id;
    @Getter(onMethod_={@Deprecated})  //onMethod不推荐直接被使用，要求加一个字符，一般来说加_就可以。
    private String name;
    private int age;
}
```

此时得到的代码是：

```java
public class Account {
    ...

    /** @deprecated */
    @Deprecated   //由Lombok额外添加的注解
    public String getName() {
        return this.name;
    }
}
```

最后，我们再来看看lazy属性，这是用于控制懒加载。

> 懒加载就是在一开始此字段没有值，当我们需要的时候才将值添加到此处。

只不过，它有一些要求，我们的属性必须是private且final：

```java
public class Account{
    @Getter(lazy=true){
        private final String name="你干嘛";
    }
}
```

生成的代码如下：

```java
public class Account {
  	//这里会自动将我们的字段修改为AtomicReference原子类型，以防止多线程环境下出现的问题
    private final AtomicReference<Object> name = new AtomicReference();

    ...

    //当我们调用getName才会去初始化字段的值，为了保证初始化只进行一次，整个过程与懒汉式单例模式一样
    public String getName() {
        Object $value = this.name.get();
        if ($value == null) {   //判断值是否为null，如果是则需要进行懒初始化
            synchronized(this.name) {    //对我们的字段加锁，保证同时只能进一次
                $value = this.name.get();
                if ($value == null) {    //再次进行一次判断，因为有可能其他线程后进入
                    String actualValue = "你干嘛";
                    $value = actualValue == null ? this.name : actualValue;
                    this.name.set($value);
                }
            }
        }
				//返回得到的结果
        return (String)($value == this.name ? null : $value);
    }
}
```

原子类知识点在JUC中，单例模式知识点在Java设计模式中，这里不多赘述（因为现在的我也不会，交给未来的我），我们作为使用者来说，只需要知道，懒加载只是将字段的值延迟赋值，比如下面的场景：

```java
public class Account{
    @Getter(lazy=true)
    private final String name=initValue();
    
    private String initValue(){
        System.out.printlin("我不希望在对象创建时就执行);
        return "666";
    }
}
```

至此，有关@Getter注解相关的内容就介绍完毕了，那么我们接着来看看@Setter：

```java
public class Account{
    @Setter
    private String name;
}
```

得到的结果：

```java
public class Account {
    private String name;

   	...
      
    public void setName(String name) {  //自动生成一个setter方法
        this.name = name;
    }
}
```

大部分与@Getter一致，唯一一个不一样的参数是onParam，它可以在形参上额外添加的自定义注解。

最后，需要注意的是，如果我们手动编写了getter与setter的方法（按照命名规则来判断），那么Lambok提供的注解将不会生效，也不会覆盖我们自己编写的方法。

如果出现同名不同参的情况误判，我们也可以使用@Tolerate注解使得Lombok忽略它的存在，继续生成。

## 构造方法相关

Lombok也可以为我们自动生成相应的构造方法，它提供了三个用于处理构造方法的注解，我们来依次学习。

首先是`@AllArgsConstructor`,它用于为类中所有属性生成一个构造方法：

```java
@AllArgsConstructor
public class Account{
    private int id;
    private String name;
    private int age;
}
```

它只能添加到类上：

```java
public class Account {
    private int id;
    private String name;
    private int age;

    public Account(int id, String name, int age) {   //自动生成一个携带所有参数的构造方法
        this.id = id;
        this.name = name;
        this.age = age;
    }
}
```

我们来看看它的其他属性：

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.SOURCE)
public @interface AllArgsConstructor {
    //用于生成一个静态构造方法
    String staticName() default "";
    
    //用于在构造方法上添加额外的注解
    AnyAnnotation[] onConstructor() default {};
    
  	//设置构造方法的访问权限级别
  	AccessLevel access() default lombok.AccessLevel.PUBLIC;
    ...
}
```

其中onConstructor和access与上一节中的类似，这里我们就不多说了，我们直接来看看他的staticName属性，它用于生成静态构造方法，现在很多类中都包含静态构造方法，比如：

```java
List<String>strings =List.of("A","B","C","D");
```

这里的List.of其实就是一种静态构造方法，通常用于快速构造对应的类对象，我们同样也可以像这样去编写，只需要将staticName设置一个名字即可：

```java
@AllArgsConstructor(staticName="with")
public class Account{
    ...
}
```

此时得到的结果：

```java
public class Account {
    ...

    //强制生成一个带全部参数的private方法，不可修改
    private Account(int id, String name, int age) {
        this.id = id;
        this.name = name;
        this.age = age;
    }

    public static Account with(int id, String name, int age) {  //生成一个以函数名为类型的静态函数
        return new Account(id, name, age);
    }
}
```

我们在使用的时候，需要调用此静态构造方法来创建对象：

```java
Account account=Account.with(1,"小明",18);
```

官方说这种方式非常适合用于泛型的类型判断，简化代码，比如MapEntry.of(“foo”,5)而不是更长的new MapEntry<String,Integer>(“foo”,5)。

现在有了全参构造，但是如果我们想要无参构造，Lombok同样也准备好了，只需要添加一个`@NoArgsConstructor`即可：

```java
@NoArgsConstructor
@AllArgsConstructor
public class Account{
    ...
}
```

此时，我们的到了一个既有全参构造，又有无参构造的类：

```java
public class Account {
    ...

    public Account() {}

    public Account(int id, String name, int age) {
        this.id = id;
        this.name = name;
        this.age = age;
    }
}
```

但是注意了，当我们使用无参构造的注解时，类中不允许出现存在final类型的字段，否则会出现错误：

![QQ_1722937534148](https://oss.itbaima.cn/internal/markdown/2024/08/06/PiYOwgRElzM2yb1.png)

只不过，@NoArgsConstructor有一个force属性，它可以在创建无参构造时，为final字段添加一个默认值，这样就可以同时存在了：

```java
@NoArgsConstructor(force=true)
@AllArgsConstructor
public class Account{
    private final int id;
    private String name;
    private int age;
}
```

得到的结果：

```java
public class Account {
    ...

    public Account() {
        this.id = 0;   //强行生成一个无参构造，但是这里也会为属性设置一个默认值，不然编译会报错
    }

    ...
}
```

我们来看最后一个构造相关的注解，`@RequiredArgsConstructor`用于生成那些需要初始化的参数的构造方法，也就是说，类中哪些属性为final，他就只针对这些属性生成对应的构造方法：

```java
@RequiredArgsConstructor
public class Account{
    private final int id;
    private String name;
    private final int age;
}
```

生成的结果为:

```java
public class Account {
    ...

    public Account(int id, int age) {   //只为fianl字段id和age生成了对应的构造方法
        this.id = id;
        this.age = age;
    }
}
```

## 打印对象

我们也可以使用Lombok为类生成toString，equals以及hashCode等方法，我们首先来看看最简单的toString方法，是需要在类中添加一个`@ToString`即可：

```java
@ToString
@AllArgsConstructor
public class Account{
    private int id;
    private String name;
    private int age;
}
```

```java
public static void main(String[] args) {
    Account account = new Account(1, "小明", 18);
    System.out.println(account);   //尝试直接打印
}
```

结果如下：

![QQ_1722938247064](https://oss.itbaima.cn/internal/markdown/2024/08/06/12yk6qGSsIM5B7p.png)

我们来看看生成的内容：

```java
public class Account {
    ...

    public String toString() {   //自动为每个字段都生成打印
        return "Account(id=" + this.id + ", name=" + this.name + ", age=" + this.age + ")";
    }
  
    ...
}
```

我们来看看它有哪些参数：

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.SOURCE)
public @interface ToString {
    //是否在打印的内容中带上对应字段的名字
    boolean includeFieldNames() default true;
    
    //用于排除不需要打印的字段（这种用法很快会被移除，不建议使用）
    String[] exclude() default {};
    
    //和上面相反，设置哪些字段需要打印，默认打印所有（这种用法很快会被移除，不建议使用）
    String[] of() default {};
    
    //不仅为当前类中所有字段生成，同时还调用父类toString进行拼接
    boolean callSuper() default false;
    
    //默认情况下生成的toString会尽可能使用get方法获取字段值，我们也可以手段关闭这个功能
    boolean doNotUseGetters() default false;
    
    //开启后将只为字段或get方法上添加了@ToString.Includ注解的内容生成toString方法，白名单模式
    boolean onlyExplicitlyIncluded() default false;
    
    /**
     * 用于排除toString中的字段
     */
    @Target(ElementType.FIELD)
    @Retention(RetentionPolicy.SOURCE)
    public @interface Exclude {}
    
    /**
     * 用于手动包含toString中的字段
     */
    @Target({ElementType.FIELD, ElementType.METHOD})
    @Retention(RetentionPolicy.SOURCE)
    public @interface Include {
			 //配置字段打印顺序的优先级
       int rank() default 0;
       
       //配置一个自定义的字段名称进行打印
       String name() default "";
    }
}
```

我们首先来看看@ToString对于get方法的特殊机制，它会尽可能的使用我们自定义的get方法获取字段的值，命名规则判定和之前一样：

```java
@ToString
@AllArgsConstructor
public class Account{
    ...
        
        public String getName(){
        return name+"同学";  //编写了一个自定义的getName方法
    }
}
```

打印结果如下：

![QQ_1722939058554](https://oss.itbaima.cn/internal/markdown/2024/08/06/tZrsA52R3pyWbqc.png)

但是，如果我们想要跳过这个getter的情况，直接输出，那么我们可以手动配置@ToString中doNotUseGetters属性：

```java
@ToString(doNotUseGetters=true)
@AllArgsConstructor
public class Account{}
```

这样，就跳过了getter的定义。

我们接着来看字段的包含和排除，首先，当我们在类中添加@ToString，默认会为所有字段生成对应的toString操作，但是如果我们需要排除某些字段，我们可以使用`@ToString.Exclude`注解，将其添加到对应的属性上，就不会打印了：

```java
@ToString
@AllArgsConstructor
public class Account{
    @ToString.Exclude
    private int id;
    private String name;
    private int age;
}
```

![QQ_1722939596344](https://oss.itbaima.cn/internal/markdown/2024/08/06/dGH7vLc5IgsbZP4.png)

同理，既然有黑名单模式，那么同样也有白名单模式，要开启白名单模式，需要将onlyExplicitlyIncluded，接着，为我们需要打印的字段添加`@ToString.Include`注解：

```java
@ToString(onlyExplicitlyIncluted=true)
@AllArgsConstructor
public class Account{
    @ToString.Include
        private int id;
    @ToString.Include
        private String name;
    private int age;
}
```

![QQ_1722940029901](https://oss.itbaima.cn/internal/markdown/2024/08/06/3qT52QNPhtiRyg4.png)

不过值得注意的是，`@ToString.Include`不仅可以对字段生效，还可以对方法生效：

```java
@ToString(onlyExplicitlyIncluted=true)
@AllArgsConstructor
public class Account{
    ...
    @ToString.Include
        public String test(){
        return "你干嘛";
    }
}
```

![QQ_1722940194659](https://oss.itbaima.cn/internal/markdown/2024/08/06/WaQtwJXVbPHSoT4.png)

@ToString同样也可以设置一些参数，比如我们手动为字段起一个用于打印的名字：

```java
@ToString.Include(name="编号")
    private int id;
@ToString.Include(name="名字")
    private String name;
```

![QQ_1722940310376](https://oss.itbaima.cn/internal/markdown/2024/08/06/tPcuIzwgUW8kOmN.png)

默认情况下，toString打印的结果都是按照编写顺序进行的，我们也可以手动指定顺序：

```java
@ToString.Include(name="编号")
    private int id;
@ToString.Include(name="名字",rank=1)  //rank越大，越靠前，默认为1
    private String name;
```

![QQ_1722940433118](https://oss.itbaima.cn/internal/markdown/2024/08/06/W48mcTetgYGZlFs.png)

## 比较相关

Lombok可以为我们自动生成类属性的比较方法以及相对的HashCode计算。我们只需要为类添加@EqualsAndHashCode注解，即可开启：

```java
@EqualsAndHashCode
@AllArgsConstructor
public class Account{
    private int id;
    private String name;
    private int age;
}
```

此时，自动生成的类为：

```java
public class Account {
    ...

    public boolean equals(Object o) {   //自动生成的equals重写方法，包含所有参数的比较
        ... 
    }

    protected boolean canEqual(Object other) {
        return other instanceof Account;
    }

    public int hashCode() {   //自动生成的hashCode重写方法
        ...
    }

    ...
}
```

他自动为我们所有的参数生成了对应的比较方法，我们可以来测试一下生成的代码能否正常运行：

```java
public static void main(String[] args){
    Account a1=new Account(1,"小明",18);
    Account a2=new Account(1,"小明",18);
    System.out.println(a1.equals(a2));
}
```

`@EqualsAndHashCode`注解的参数大部分与我们上节讲解的`@ToString`类似，比如`exclude`、`of`、`callSuper`（默认关闭，开启后调用equals比较前先调用父类的equals进行一次比较）、`doNotUseGetters`以及生成的方法中需要额外携带的注解`onParam`属性等。

它同样可以使用`onlyExplicitlyIncluded`属性来开启白名单模式，我们可以使用以下注解来自由控制哪些属性会作为比较的目标，哪些需要排除：

- `@EqualsAndHashCode.Exclude` - 用于排除不需要参与比较的字段。
- `@EqualsAndHashCode.Include` - 开启白名单模式后，用于标明哪些字段需要参与比较。

和@ToString一样，我们同样可以将其添加到一个方法上，使其结果也参与其中：

```java
@EqualsAndHashCode.Include
    public int test(){
    return 1;
}
```

不过，@EqualsAndHashCode.Include有一个replace属性，它可以用于将当前方法的结果替代目标字段进行比较，比如：

```java
@EqualsAndHashCode.Include(replaces="id")  //此时，id的比较不会直接比较其本身，而是改用此方法获取对应的结果进行比较
    public int test(){
    return 1;
}
```

最后，让我们来看看它独特的hashCode缓存机制，我们可以通过设置cacheStrategy属性来控制hashCode结果的缓存，这有助于优化程序的性能，默认情况下缓存为NEVER，也就是不启用，我们可以开启LAZY模式：

```java
@EqualsAndHashCode(cacheStrategy = EqualsAndHashCode.CacheStrategy.LAZY)
@AllArgsConstructor
public class Account{
    private int id;
    private String name;
    private int age;
}
```

此时，生成的hashCode方法在第一次生成结果之后，后续将一致使用同样的结果直接返回，避免二次计算：

```java
public int hashCode() {
    if (this.$hashCodeCache != 0) {  //判断是否生成过hashCode，直接使用缓存
        return this.$hashCodeCache;
    } else {
        ...
        this.$hashCodeCache = result;  //设置缓存
        return result;
    }
}
```

这对于哪些属性值不会发生变化的实体类来说，是一个很好的选择，但是后续使用中，值发生变化从而影响hashCode的结果，则不建议使用此功能。

此时，如果我们大量的需要这些注解，我们可以使用`@Data`，这包含了：`@Getter` `@Setter` `@RequiredArgsConstructor` `@ToString` `@EqualsAndHashCode`。

只读版本`@Value`，它等价于添加注解：`@Getter` `@FieldDefaults(makeFinal=true, level=AccessLevel.PRIVATE)` `@AllArgsConstructor` `@ToString` `@EqualsAndHashCode`

```java
@Value
public class Account {  //类会自动变成final类型
    int id;   //在`@FieldDefaults`配置下，会自动将类属性变为private和final的状态，这里我们无需手动编写
    String name;
    int age;
}
```

只不过在Java17之后，这种类完全可以被记录类型平替，因此使用时IDEA会提示我们直接使用记录类型。

## 建模

该知识点，在学习了设计模式后再进行学习。

## 变量相关

很多语言都有var关键字，它用于声明一个变量，但是我们无需手动设置。在Java10之后，同样支持了var关键字，它可以自动判断类型，而不需要像之前那样手动指明变量的类型。

```java
var a=" ";  //自动推断变量a的类型为String
```

而在Lombok中，也为我们提供了对应的注解类型，使得我们可以像其他语言那样使用：

- var——java10之前可用，java10之后存在无法导入的问题，功能完全一样。
- val——与var类似，但是它是不可变的，等价于final变量。

```java
public static void main(String[] args){
    val a="Hello World";  //等价于final变量
    System.out.println(a);
}
```

## 资源释放与异常处理

有些时候，我们可能会用到一些需要释放资源的对象，比如Stream这类，在Java7的时候推出了try-with-resource语法，它大大减少了我们编写资源释放语句的成本：

```java
public static void main(String[] args)throws IOException{
    //使用try-with-resource会自动生成close相关操作的代码
    try(FileInputStream in=new FileInputStream("test.exe")){
        byte[] bytes=in.readAllBytes();
        System.out.println(new String(bytes));
    }
}
```

即便如此，但是他依然不够灵活，Lombok为我们提供了一个更加方便的注解，只需要在我们需要释放资源的变量前添加`@Cleanup`即可：

```java
public static void main(String[] args)throw IOException{
    @Cleanup FileInputStream in=new FileInputStream("test.py");
    byte[] bytes=in.readAllBytes();
    System.out.println(new String(bytes));
}
```

生成的代码为：

```java
public static void main(String[] args) throws IOException {
    FileInputStream in = new FileInputStream("test.py");
    try {
        byte[] bytes = in.readAllBytes();   //自动将后续操作添加到try语句块中
        System.out.println(new String(bytes));
    } finally {   //在finally中对资源进行释放
        if (Collections.singletonList(in).get(0) != null) {
            in.close();
        }
    }
}
```

当然，我们同样可以自定义操作关闭资源：

```java
static class Test{
    public void end(){
        System.out.println("关闭资源");
    }
}

public static void main(String[] args)throw IOException{
    @Cleanup("end") Test test=new Test();
}
```

我们在使用Stream时多多少少的遇到了手动处理IOException的问题，这就导致我们很多地方都要去写`throws`来抛出异常，此时，Lombok为我们提供了一个`@SneakyThrows`注解，不需要我们手动指定，就可以抛出注解。

```java
@SneakyThrows
public static void main(String[] args){
    @Cleanup FileInputStream in=new FileInputStream("test.py");
    byte[] bytes=in.readAllBytes();
    System.out.println(new String(bytes));
}
```

实际上在编译完成时：

```java
public static void main(String[] args) {
    try {   //自动使用trycatch包裹内部，出现问题直接原样抛出
        ...
    } catch (Throwable var7) {
        Throwable $ex = var7;
        throw $ex;
    }
}
```

官方解释这个注解为了避免javac的异常捕获检查，减少手动编写异常抛出的代码。

## 非空判断

由于java除了基本类型之外其他类型都有可能存在`null`的情况，因此空指针问题一直困扰着所有人，很多情况下我们不得不在传递参数时进行检验，以确保传入的参数不是`null`才能安全的进行困扰操作。最简单的方法就是在最开始的时候直接对其进行判定：

```java
/***
 * 测试方法
 * @param text 要求不为null的情况下打印
 */
public static void test(String text){
    if(text == null) return;
    System.out.println(text);
}
```

在Java8之后我们也可以利用Optional将其写的更方便：

```java
//利用Optional和Lambda表达式一行搞定
public static void main(String[] args){
    Optional.ofNullable(text).ifPresent(System.out::println);
}
```

不过，虽然我们可以像这样进行一次预先判断，但是它依旧不够方便，如果我们需要对所有参数都进行校验，这是不可能的，那么，Lombok为我们提供了一种更好的方式，我们只需要在参数前面添加`@NonNull`则会自动为其生成对应的判空代码：

```java
public static void test(@NonNull Sting text){
    System.out.println(text);
}
```

生成结果为：

```java
public static void test(@NonNull String text) {
    if (text == null) {
        throw new NullPointerException("text is marked non-null but is null");
    } else {
        System.out.println(text);
    }
}
```

除了方法的形参外，也可以添加到局部变量上，但是只会有一个警告效果。

## 锁处理

同样，本节涉及到了JUC的课程，以后在进行学习补充。

## 日志相关

我们在项目中可能需要使用各种日志，Lombok为不同的日志框架提供了一个快速注解。我们在项目中常常需要将日志对象创建在类中：

```java
private static Logger log=Logger.getLogger(Main.class.getName());
public static void main(String[] args){
    log.info("我是日志");
}
```

而有了Lombok之后，我们可以直接在类上添加`@Log`注解：

```java
@Log
public class Main{
    public static void main(String[] args){
        log.info("我是日志");  //自动生成一个log对象，我们可以直接使用
    }
}
```

针对于不同的日志框架，我们可以使用不同的注解来创建：

```
@CommonsLog
```

创造`private static final org.apache.commons.logging.Log log = org.apache.commons.logging.LogFactory.getLog(LogExample.class);`

```
@Flogger
```

创造`private static final com.google.common.flogger.FluentLogger log = com.google.common.flogger.FluentLogger.forEnclosingClass();`

```
@JBossLog
```

创造`private static final org.jboss.logging.Logger log = org.jboss.logging.Logger.getLogger(LogExample.class);`

```
@Log
```

创造`private static final java.util.logging.Logger log = java.util.logging.Logger.getLogger(LogExample.class.getName());`

```
@Log4j
```

创造`private static final org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(LogExample.class);`

```
@Log4j2
```

创造`private static final org.apache.logging.log4j.Logger log = org.apache.logging.log4j.LogManager.getLogger(LogExample.class);`

```
@Slf4j
```

创造`private static final org.slf4j.Logger log = org.slf4j.LoggerFactory.getLogger(LogExample.class);`

```
@XSlf4j
```

创造`private static final org.slf4j.ext.XLogger log = org.slf4j.ext.XLoggerFactory.getXLogger(LogExample.class);`
