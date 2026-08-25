# JUL日志系统

我们之前一直使用System.out.println来打印信息，但是，如果项目中存在大量的控制台输出语句，会显得很凌乱，而且日志不够细致，假如我们现在希望，项目只在debug的情况下打印某些日志，采用直接输出的方式就很难实现了，因此我们需要使用日志框架来规范化日志输出。

而且JDK为我们提供了一个自带的日志框架，位于java.util.logging包下，我们可以使用此框架实现日志的规范化打印，使用起来很简单：

```java
public class Main{
    public static void main(String[] args){
        //首先获取日志打印器
        Logger logger=Logger.getLogger("test");
        //调用info来输出一个普通的信息，直接填写字符串即可
        logger.info("我是日志");
    }
}
```

我们可以在主类中实现日志打印，得到的结果：

```
8月10, 2025 10:36:49 上午 Main main
信息: 我是日志
```

我们发现，通过日志输出的结果更规范。

## JUL基本使用

日志的打印并不是简单的输出，有些时候我们可以会打印一些比较重要的日志信息，或者非常紧急的日志信息，根据不同类型的信息进行划分，日志一般分为7个级别，详细信息我们在Level类中查看：

```java
public class Level implements java.io.Serializable {
	...
  
    //出现严重故障的消息级别，值为1000，也是可用的日志级别中最大的
    public static final Level SEVERE = new Level("SEVERE",1000, defaultBundle);
    //存在潜在问题的消息级别，比如边充电边打电话就是个危险操作，虽然手机爆炸的概率很小，但是还是会有人警告你最好别这样做，这是日志级别中倒数第二大的
    public static final Level WARNING = new Level("WARNING", 900, defaultBundle);
    //所有常规提示日志信息都以INFO级别进行打印
    public static final Level INFO = new Level("INFO", 800, defaultBundle);
  	//以下日志级别依次降低，不太常用
    public static final Level CONFIG = new Level("CONFIG", 700, defaultBundle);
    public static final Level FINE = new Level("FINE", 500, defaultBundle);
    public static final Level FINER = new Level("FINER", 400, defaultBundle);
    public static final Level FINEST = new Level("FINEST", 300, defaultBundle);
 
  ...
}
```

之前通过info方法直接输出的结果就是使用的默认级别的日志，实际上每个级别都有一个对应的方法用于打印：

```java
public static void main(String[] args){
    Logger logger = Logger.getLogger(Main.class.getName());
    logger.severe("severe");  //最高日志级别
    logger.warning("warning");
    logger.info("info"); //默认日志级别
    logger.config("config");
    logger.fine("fine");
    logger.finer("finer");
    logger.finest("finest");   //最低日志级别
}
```

当然，如果需要更加灵活地控制日志级别，我们也可以通过log方法来主动设定该条日志的输出级别：

```java
Logger logger=Logger.getLogger(Main.class.getName());
logger.log(Level.SEVERE,"严重的错误);
logger.log(Level.WARNING,"警告的内容);
logger.log(Level.INFO, "普通的信息");
logger.log(Level.CONFIG, "级别低于普通信息);
```

打印后会发现，某些级别的日志，并没用在控制台打印。这其实是因为Logger默认情况下只会打印INFO级别以上的日志，而下面的日志会直接省略，我们可以通过配置进行调整。

## 日志核心内容

我们接下来看日志打印的核心部分：Handler，它用于处理我们的日志打印，JDK为我们提供了很多种类的Handler用于多种不同类型的日志打印，比较常见的就是打印到控制台，当然我们也可以打印到一个日志文件中，名字是xxx.log(类似于xxx.txt)。常见的Handler有：

- ConsoleHandler - 将日志通过System.err打印到控制台，默认是这个。
- FileHandler - 将日志直接写入指定文件中。
- SocketHandler - 将日志通过Socket发送到另一个主机。

当然，一个Logger可以包含多个Handler同时用于向不同的地方打印日志，我么们通过getHandlers方法来获取Logger中已经配置的Handler对象：

```java
Logger logger=Logger.getLogger(Main.class.getName());
System.out.println(Arrays.toString(logger.getHandlers()));
```

此时是空的，可见，我们创建的Logger默认是不带任何Handler对象的，那么我们之前的日志是怎样打印的呢？这实际上是Logger的父级提供的，这里先不介绍继承关系。我们使用setUseParentHandlers方法来屏蔽所有父类提供的日志处理器：

```java
logger.setUseParentHandlers(false);
```

现在由于Logger没有配置任何Handler处理器，因此打印日志就没有任何效果了。

现在，我们自己尝试配置一个用于控制台打印的Handler处理器，这里我们自己搭建一个ConsoleHandler对象：

```java
ConsoleHandler handler=new ConsoleHandler();
logger.addHandler(handler);
logger.info("hello world");
```

现在我们获得了打印的结果了：

```
8月10, 2025 11:04:21 上午 Main main
信息: hello world
```

我们现在尝试将日志记录到本地的文件中，这里使用FileHandler类型：

```	java
FileHandler handler=new FileHandler("test.log",true);  //第二个参数开启后会续写已有的日志，如果不开启会直接覆盖重写
logger.addHandler(handler);
```

最后，我们得到一个日志文件了，默认以xml格式进行写入的：

![QQ_1724775618370](https://oss.itbaima.cn/internal/markdown/2024/08/28/4mZsxMOGDA8jTBn.png)

这种规格有助于程序的日志读取，但是对于我们人来说，难以阅读，那有没有什么办法将文件的日志打印成控制台那种格式的呢？实际上每一个Handler都有一个Formatter对象，它用于控制日志的格式，默认情况下，ConsoleHandler会配置一个SimpleFormatter对象，格式为：

```
时间 类名 方法
日志级别：日志内容
```

我们刚刚在FileHandler中见到的默认生成的XMLFormatter，它将日志以xml的形式打印，现在我们也可以手动修改：

```java
Handler handler=new FileHandler("test.log");
handler.setFormatter(new SimpleFormatter());
```

此时，日志文件中写入的内容就是简单的日志格式了：![QQ_1724776088333](https://oss.itbaima.cn/internal/markdown/2024/08/28/VJKTIlU51cBO6aS.png)

我们最后来看看上一节中遗留的日志级别问题，我们知道日志的默认打印级别为INFO，此时低于INFO的所有日志都是被屏蔽的，而要修改日志的默认打印级别，我们需要调整Handler和Logger的level属性：

```java
handler.setLevel(Level.FINEST);  //填写的日志级别什么，高于等级此级别的所有日志都会被打印
logger.setLevel(Level.FINEST);
logger.fine("Hello World");
```

现在我们再次打印低于INFO的日志就可以得到正确的结果了,Logger类还为我们提供了两个比较特殊的日志级别，他们专门用于配置特殊情况：

```java
//表示直接关闭所有日志信息，值为int的最大值
public static final Level OFF=new Level("OFF",Integer.MAX_VALUE,defaultBundle);
//表示开启所有日志信息，无论是什么级别都进行打印
public static final Level ALL=new Level("ALL",Integer.MIN_VALUE,defaultBundle);
```

因为这里OFF的值为int的最大值，也就是说没有任何日志级别的值大于它，因此，如果将打印等级配置为OFF，那么所有类型的日志信息都不会被打印了，而ALL则相反。

## 日志继承关系

JUL中Logger之间存在父子关系，这种父子关系类似于继承，我们可以通过Logger的getParent方法来获取其父Logger对象：

```java
Logger logger=Logger.getLogger(Main.class.getName());
System.out.println(logger.getParent());
```

这里我们得到一个：

```
java.util.logging.LogManager$RootLogger@4bf558aa
```

这个RootLogger对象为所有日志记录器的最顶层父级对象，它包含一个默认的ConsoleHandler处理器用于进行控制台打印，而日志在打印时，子Logger会继承父Logger提供的所有Handler进行日志处理，因此我们在默认情况下才能正常使用日志打印：

```java
Logger logger=Logger.getLogger("test");
Logger parent=logger.getParent();
System.out.println(Arrays.toString(parent.getHandlers()));
```

根据我们上节课的知识，在默认情况下如果我们需要修改日志打印等级，那么同时也需要将父级的Handler也进行日志等级配置：

```java
parent.getHandlers()[0].setLevel(Level.ALL);  //[0]表示默认是第一个，ALL表示所有级别都可以
logger.setLevel(Level.ALL);
logger.config("jdaiow");
```

当然，如果我们在不屏蔽父级Handler的情况下为子配置一个Handler，那么此时两个Handler都会生效：

```java
logger.addHandler(new ConsoleHandler());
logger.info("1dwsx");
```

日志中出现了两次：

```
8月10, 2025 9:46:36 下午 Main main
信息: Hello Word
8月10, 2025 9:46:36 下午 Main main
信息: Hello Word
```

不过，需要注意一下顺序，当子类和父类都配置时，那么子类的Handler会优先处理，接着才是父级。

除了默认的RootLogger作为父类，实际上Logger还会通过名称进行分级，自动构建一个继承关系，比如下面：

```java
Logger logger1 = Logger.getLogger("com");
Logger logger2 = Logger.getLogger("com.test");
Logger logger3 = Logger.getLogger("com.test.inner1");
Logger logger4 = Logger.getLogger("com.test.inner2");

System.out.println(logger4.getParent() == logger2);   //全true
System.out.println(logger3.getParent() == logger2);
System.out.println(logger2.getParent() == logger1);
```

就像包名，日志的名称会按照包的分级，进行自动继承，如图：

![QQ_1724778477259](https://oss.itbaima.cn/internal/markdown/2024/08/28/4X8PqesSAC7ijZW.png)

至于为啥要这样划分，下面我们来介绍。

## 日志默认配置

### Properties格式

在学习日志配置之前，我们先来学习Properties格式，Properties格式是java的一种配置文件，我们之前在Mybatis中学习了xml，但是xml的读取太过于麻烦，那么是否存在于一种简单的配置文件呢？此时使用Properties，格式如下：

```properties
name=Test
desc=Descrption
```

该文件配置很简单，类似于Java中Map键值对，中间使用等号进行连接。当然，键的名称我们也可以分多级进行配置，每一级用.进行划分，比如我们现在要配置数据库的连接信息，就可以编写为这种形式：

```properties
jdbc.datasource.driver=com.cj.mysql.Driver
jdbc.datasource.url=jdbc:mysql://localhost:3306/test
jdbc.datasource.username=root
jdbc.datasource.password=123456
```

那么文件配好了，该如何进行读取呢？JDK为我们提供了一个叫做Properties的类型，他继承自Hashtable类（是HashMap的同步加锁版）使用起来与HashMap类似：

```java
public class Properties extends Hashtable<Object,Object>{
```

现在，试着创建一下：

```java
Properties properties=new Properties();
properties.load(new FileReader("test.properties"));  //使用load方法读取本地文件的所有配置到Map中
System.out.println(properties);
```

实际上，我们可以通过这种方式来获取我们的一些系统属性，System类中有一个getProperties方法用于存储所有系统相关的属性值，这里我们打印一下系统名称和版本：

```java
Properties properties=System.getProperties();
System.out.println(properties.get("os.name"));
System.out.println(properties.get("os.version"));
```

当然，程序中的Properties对象也可以快速保存为一个对应的.Properties文件：

```java
Properties properties=System.getProperties();
properties.store(new FileWriter("test.properties","null"));
```

### Properties与JUL

接着，我们回到JUL中，实际上JUL也可以通过配置文件来规范日志打印器的一些默认值，比如我们现在向配置默认的日志打印级别：

```properties
# RootLogger 的默认处理器：
handlers=java.util.logging.ConsoleHandler
# RootLogger 的默认的日志级别
.level=ALL

# 配置ConsoleHandler的默认level
java.util.logging.ConsoleHandler.level=ALL
```

接着，我们要在程序开始之前加载这里的配置：

```java
LogManager manager=LogManager.getLogManager();
manager.readConfiguration(new FileInputStream("test.properties"));
Logger logger=Logger.getLogger("test");
logger.config("Hello World");
```

这样就可以通过配置文件的形式修改一些功能的默认属性了，而不需要我们再使用代码进行配置。实际上在JUL的这类内部也有着对应的配置处理操作，如果发现有默认配置优先使用配置里面的，比如Handler的构造方法：

```java
Handler(Level defaultLevel, Formatter defaultFormatter,
        Formatter specifiedFormatter) {

    LogManager manager = LogManager.getLogManager();
    String cname = getClass().getName();

    final Level level = manager.getLevelProperty(cname + ".level", defaultLevel);
    final Filter filter = manager.getFilterProperty(cname + ".filter", null);
    final Formatter formatter = specifiedFormatter == null
                                ? manager.getFormatterProperty(cname + ".formatter", defaultFormatter)
                                : specifiedFormatter;
    final String encoding = manager.getStringProperty(cname + ".encoding", null);
		...
}
```

关于使用配置文件的形式修改JUL部分内容的默认值就先讲解到这里。

## 自定义日志格式

前面我们提到了每一个Handler都可以配置一个对应的Formatter来决定日志打印的格式，除了官方默认提供的两种格式外，我们也可以自定义。

我们只需要继承Formatter类，就可以创建一个自定义的日志格式处理逻辑了：

```java
public class MyFormatter extends Formatter{
    @Override
    public String format(LogRecord record){
        return "我是自定义日志格式;
    }
}
```

接着，我们通过上节课的方式，直接把ConsoleHandler的默认Formatter配置为我们自己的类：

```properties
java.util.logging.ConsoleHandler.formatter=com.test.MyFomatter
```

因此，我们也可以利用这些属性来编写一个类似于的SimpleFormatter的日志格式，比如这里包含类名、时间等，类似于下面图中的日志格式：

![QQ_1724781560808](https://oss.itbaima.cn/internal/markdown/2024/08/28/FWTolmRGuX2J1cU.png)



我们来尝试编写一下：

```java
public String format(LogRecord record) {
    StringBuilder builder = new StringBuilder();
    //日期
    Date date = new Date(record.getMillis());
    SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS");
    builder.append(dateFormat.format(date));
    //级别
    builder.append("  ").append(record.getLevel());
    builder.append(" --- ");
    //线程名称
    builder.append('[').append(Thread.currentThread().getName()).append(']');
    //类名：
    builder.append(" ").append(String.format("%-15s", record.getSourceClassName()));
    //消息内容
    builder.append(" : ").append(record.getMessage());

    return builder.toString();
}
```

至此，有关JUL相关的基础内容我们就介绍到这里。
