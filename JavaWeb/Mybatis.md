# Mybatis

接下来，让我们学习Mybatis，该框架其实是基于JDBC，并且更加高效简洁的方式来和数据库进行交互。

在正式学习Mybatis之前，我们需要先学习xml语言。

## xml语言

xml语言放最初是用于数据库的存储和传输，它是由一个个标签嵌套而成，一般长这样：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<outer>
  <name>阿伟</name>
  <desc>怎么又在玩电动啊</desc>
	<inner type="1">
    <age>10</age>
    <sex></sex>
  </inner>
</outer>
```

xml文件本质上是一个配置文件。

一个xml文件存在以下的格式规范：

- 必须存在一个根节点，将所有的子标签包含。
- 可以但不必须包含一个头部声明（主要用于设定编码格式）。
- 所以标签必须成对出现，有些可以单独。
- 区分大小写。
- 标签中存在属性，属性的==值=由单引号或者双引号包括。

xml文件也可以使用注释：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!-- 注释内容 -->
```

当内容中出现<或>字符，我们会使用xml的转义字符来代替：

![img](https://oss.itbaima.cn/internal/markdown/2024/08/12/bYBle7VIq6DNang.jpg)

那么，我们现在了解了xml文件的定义，现在该如何解析一个xml文件呢？比如，我们希望将定义好的xml文件读取到Java程序中，该如何做呢？

JDK为我们内置了一个叫org.w3c的xml解析库，让我们来解析内容：

```java
// 创建DocumentBuilderFactory对象
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
// 创建DocumentBuilder对象
try {
    DocumentBuilder builder = factory.newDocumentBuilder();
    Document d = builder.parse("file:mappers/test.xml");
    // 每一个标签都作为一个节点
    NodeList nodeList = d.getElementsByTagName("test");  // 可能有很多个名字为test的标签
    Node rootNode = nodeList.item(0); // 获取首个

    NodeList childNodes = rootNode.getChildNodes(); // 一个节点下可能会有很多个节点，比如根节点下就囊括了所有的节点
    //节点可以是一个带有内容的标签（它内部就还有子节点），也可以是一段文本内容

    for (int i = 0; i < childNodes.getLength(); i++) {
        Node child = childNodes.item(i);
        if(child.getNodeType() == Node.ELEMENT_NODE)  //过滤换行符之类的内容，因为它们都被认为是一个文本节点
            System.out.println(child.getNodeName() + "， +child.getFirstChild().getNodeValue());
        // 输出节点名称，也就是标签名称，以及标签内部的文本（内部的内容都是子节点，所以要获取内部的节点）
    }
} catch (Exception e) {
    e.printStackTrace();
}
```

当然，学习和使用xml只是为了更好的认识Mybatis的工作原理，以及如何使用xml来作为Mybatis的配置文件，使用Java读取xml文件不要求掌握，要了解。

不仅仅是Mybatis，包括后面的Spring等众多框架都会用到xml来作为框架配置文件。

## 初次使用Mybatis

首先，先搭建环境。

https://mybatis.org/mybatis-3/zh_CN/getting-started.html，还是老规矩，我们直接先下载好Mybatis的依赖Jar包：https://github.com/mybatis/mybatis-3/releases

如果使用Maven可以直接引入：

```xml
<dependency>
  <groupId>org.mybatis</groupId>
  <artifactId>mybatis</artifactId>
  <version>3.5.16</version>
</dependency>
```

依赖变多之后，我们可以将其放到一个单独的文件夹，不然会很繁杂：

![QQ_1723452238551](https://oss.itbaima.cn/internal/markdown/2024/08/12/Y7ykK3idxSvUT1r.png)



依赖导入完成后，我们就可以编写Mybatis的配置文件了（现在不是在Java代码中配置了，而是通过一个XML文件去配置，这样就使得硬编码的部分大大减少，项目后期打包成Jar运行不方便修复，但是通过配置文件，我们随时都可以去修改，就变得很方便了，同时代码量也大幅度减少，配置文件填写完成后，我们只需要关心项目的业务逻辑而不是如何去读取配置文件）我们按照官方文档给定的提示，在项目根目录下新建名为`mybatis-config.xml`的文件，并填写以下内容：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
```

我们发现，在最上方还引入了一个叫做DTD（文档类型定义）的东西，它提前帮助我们规定了一些标签以及这些标签应该具有哪些属性，这些标签是Mybatis专属的配置标签，我们也必须要按照对应的方式来进行配置。

接着我们就可以使用DTD中声明的各种标签进行配置的编写了，最外层需要使用`configuration`标签进行囊括，内部首先需要编写环境配置，我们的项目可能会分多个环境进行编写，比如我们在开发的时候可能连接的是自己本地的数据库，但是项目部署到服务器上之后，可能会连接其他的数据库，所以我们可以提供多个环境配置，只不过这里我们只是做开发，只需要配置一个`environment`即可：

```xml
<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://localhost:3306/web_study"/>
                <property name="username" value="test"/>
                <property name="password" value="123456"/>
            </dataSource>
        </environment>
    </environments>
</configuration>
```

在`environment`中我们可以配置两个部分，一个是事务管理器，还有一个是数据源，事务管理器我们这里直接使用JDBC即可，有关其他事务管理器我们会在后续Spring课程中为大家介绍。数据源中配置就是驱动、连接地址、用户名和密码，按照之前JDBC的方式进行配置即可，最后还有一个数据源类型配置我们也会放在后续Spring阶段再进行介绍。

配置文件完成后，接着我们就可以通过Java来使用Mybatis了，首先我们要介绍的是`SqlSessionFactoryBuilder`它用于构建`SqlSessionFactory`对象，每个基于MyBatis 的应用都是以一个 SqlSessionFactory 的实例为核心的，使用也很简单，这里我们使用的是XML的形式进行配置的：

```java
public static void main(String[] args) throw FileNotFoundException{
    //使用build方法来创建SqlSessionFactory，这里我们通过文件输入流传入来配置文件
    SqlSessionFactory ssf=new SqlSessionFactoryBuilder().build(new FileInputStream("mybatis-config.xml"));
}
```

既然有了SqlSessionFactory，顾名思义，我们可以从中获取SqlSession的实例，每一个SqlSession都有一个会话，也就是相当于我们之前通过命令行访问MySql的一个窗口，不同的会话之间相互隔离，不受影响：

```java
try(SqlSession session=SqlSessionFactory.openSession(true)){
    //由于SqlSession需要在结束后关闭，这里我们使用try with resource来编写
    //这里的参数设置为自动提交，和之前的JDBC一样
}
```

![QQ_1723455145061](https://oss.itbaima.cn/internal/markdown/2024/08/12/eq3LwI1paXucYNl.png)

SqlSession接口为我们预设了非常多的增删改查操作：

```java
public interface SqlSession extends Closeable {
    <T> T selectOne(String statement);
    <T> T selectOne(String statement, Object parameter);
    <E> List<E> selectList(String statement);
    ...
    int insert(String statement);
    int insert(String statement, Object parameter);
    int update(String statement);
    int update(String statement, Object parameter);
    int delete(String statement);
    int delete(String statement, Object parameter);
```

我们该如何使用这些方法呢？由于Mybatis并不知道我们需要执行的SQL语句以及返回哪些数据作为结果，我们需要编写配置文件来告诉Mybatis我们需要做什么？

我们可以在项目目录中创建一个新的mapper目录，然后创建一个新文件TestMapper.xml作为我们SQL语句的映射配置，并添加以下内容：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="testMapper">
  
</mapper>
```

这里我们添加了映射器（Mapper）的DTD来方便我们后续配置，其中mapper标签用于囊括后续编写的所有SQL映射，namespace属性用于区分不同的映射器（一个项目可以有多个Mapper配置文件，用于分类存放不同的SQL映射）以及我们后续介绍的接口绑定，接着，我们需要尝试编写了。

假设我们要查询user表中的所有数据，我们需要先构建一个实体类：

```java
@Data
public class User{  //属性名称和数据库字段名称要一一对应，不然会赋值失败。
    int id;
    String name;
    int age;
}
```

接着我们在配置文件中添加一个新的映射，由于我们需要使用select语句，这里使用select标签：

```java
<select id="selectAllUser" resultType="com.test.User">
    select * from user
</select>
```

由于一个mapper文件中可以存在多个SQL语句映射，这里的id用于区分其他sql语句映射的，后面的resultType代表通过sql语句查询到结果后转换为实体类（比如这里的User），其他未使用的参数我们后续介绍。

接着，我们需要将其添加到一开始的Mybatiss配置文件中，使得Mybatis可以一开始正常加载：

```xml
<configuration>
    ...
    <mappers>
        <mapper url="file:mappers/TestMapper.xml"/>
    </mappers>
</configuration>
```

最后，我们在主函数中编写：

```java
try(SqlSession session=sqlSessionFactory.openSession(true)){
    List<User>users=session.selectList("selectAllUser");  //直接填写我们刚刚写的映射id
    users.forEach(System.out::println);
}
```

## Mybatis详解

### 查询操作

前面我们大致熟悉了一下配置流程，现在我们详细介绍如何配置查询操作。

由于SqlSessionFactory一般只需要创建一次，因此我们可以创建一个工具类来集中创建SqlSession，这样会更加方便一些：

```java
public class MybatisUtil{
    private static SqlSessionFactory ssf;
    static{
        try{
            ssf=new SqlSessionFactoryBuilder().build(new FileInputStream("mybatis-congfig.xml"));
        }catch(FileNotFoundException e){
            e.printStackTrace();
        }
    }
    
     /**
     * 获取一个新的会话
     * @param autoCommit 是否开启自动提交（跟JDBC是一样的，如果不自动提交，则会变成事务操作）
     * @return SqlSession对象
     */
    //SqlSession session = MybatisUtil.openSession(true);这是下面方法的用法
    public static SqlSession openSession(boolean autoCommit){
        return sqlSessionFactory.openSession(autoCommit);
    }
}
```

现在，我们只需要在main方法中使用工具类就能快速创建一个新会话：

```java
try(SqlSession ss=MybatisUtil.openSession(true)){
    List<User>users=ss.selectList("selectUser");
    users.forEach(System.out::println);
}
```

查询操作在xml配置中是以select标签囊括，我们首先来介绍需要配置的参数，假设，我们需要编写一个根据id查询用户的操作，首先我们需要指定id：

```xml
<select id="selectUserById">
</select>
```

接着我们需要配置查询的参数，由于要根据用户ID查询：

1. 如果是基本类型，需要在前面加入下划线，比如_int。
2. 如果是包装类或者其他类型，可以直接使用。
3. 如果是自己编写的类型，需要完整的包名加类名才可以i。

当然如果嫌麻烦，可以直接不填，Mybatis自动判断。

接下来，我们需要通过一个参数来查询，所以需要填入一个占位符，通过#{xxx}或${xxx}来填写：

```xml
<select id="selectUserById" >
select * from user where id=#{id}
</select>
```

实际上，Mybatis也是通过preparedStatement首先进行一次预编译，来有效防止sql注入问题，但如果使用的是占位符，那么就不通过预编译，而是直接传值，因此对于常见的一些查询参数，我们一般通过占位符来保证安全性。

最后，我们查询到结果后，一般将其转化为对应的实体类对象，所以我们使用resultTpye指定：

```xml
<select id="sekectUserById" resultType="com.test.User">
select * from user where id =#{id}
</select>
```

当然，如果嫌太累的话，我们可以设置一个别名：

```xml
<typeAliases>
<typeAlias type="com.test.User" alias="User"/>
</typeAliases>
```

也可以最直接扫描整个包下的所有实体类，自动起别名，默认情况下别名就是类的名称：

```xml
<typeAliases>
<package name="com.test.entity"/>
</typeAliases>
```

这样，SQL语句映射配置我们就编写好了，接下来调用：

```java
User user=session.selectOne("selectUserById",1);
System.out.println(user);
```

这样就可以查询到ID为1的用户信息了。

当然，如果你不需要转换为实体类，我们可以转换成一个Map对象：

```java
//Key为String类型，Value为Object类型
Map<String,Object>user=session.select("selectUserById",1);
System.out.println(user);
```

我们可以尝试接着写一个同时查询ID和年龄的操作：

```xml
<select id="selectUserByIdAndAge" resultType="com.test.User">
select * from user where id=#{id} and age=#{age}
</select>
```

因为这楼里需要多个参数，我们可以使用Map，注意Key的名称要和我们编写的SQL语句中占位符一致：

```java
User user=session.selectOne("selectUserByIdAndAge",Map.of("id",1,"age",18));
System.out.println(user);
```

接下来，我们来看看下面这种情况，实体类中定义的属性名称和我们数据库中名称似乎有点不太一样，这会导致Mybatis自动处理这些问题：

```java
@Data
public class User{
    int uid;
    String username;
    int age;
}
```

运行后我们会发现，Mybatis虽然可以查询到记录，但是数据并没有上传到数据库上，这就是因为数据库名称与类中属性名称不匹配导致的，但是，我们可以手动配置一个resultMap来解决这个问题，直接在Mapper中添加：

```xml
<select id="selectUserByIdAndAge" resultType="com.test.User">
select * from user where id=#{id} and age=#{age}
</select>
<resultMap id="user" type="com.test.User">
<result column="id" property="uid"/>
<result column="name" property="username"/>
</resultMap>
```

我们尝试编写查询一个列表，查询列表是无需像Map一样设置list这种类型，而是使用List内部所包含的类型，所以这里还是照常：

```xml
<select id ="selectUsers" resultType="com.test.USer">
select * from user;
</select>
```

由于返回的是一个列表，这里使用selectList：

```java
List<User>user=session.selectList("selectUsers");
System.out.println(user);
```

我们同样可以进行简单的条件查询，比如我们查询所有年龄大于等于18的用户：

```xml
<select id ="selectUsers" resultType="com.test.User">
select * from user where age &gt; #{age};
</select>
```

记得使用转义字符哦。

```java
List<User>user=session.selectList("selectUsersByAge",18);
```

我们接着来看一个特殊的选择方法selectMap，它可以将查询结果以一个Map的形式表示，只不过与以往的形式不同，他的Key与Value是反着的：

```java
Map<String,User>user=session.selectMap("selectUserById",1,"id");
```

此时得到的结果是:![QQ_1723711033070](https://oss.itbaima.cn/internal/markdown/2024/08/15/skVRAyvo8KqjxE7.png)

可以看到Map的id作为Key。

还有一个比较特殊的操作是selectCursor，它可以得到Cursor对象，同样用于列表查询，只不过使用起来与之前的ResultSet类似，它是通过迭代器的形式去进行数据的读取，官方解释它主要用于惰性获取数据，提高性能：

```java
public interface Cursor<T> extends Closeable,Iterable<T>{...}
```

可以看到他继承了Iteable接口，表明它可以获取迭代器或者直接使用foreach遍历：

```java
Cursor<User>cursor=session.selectCursor("selectUsers");
for(User user:cursor){
    System.out.println(user);
}
```

最后介绍一下select方法，支持我们使用Lambda表达式进行查询结果的处理：

```java
session.select("selectUsers",context->{
    System.out.println(context.getResultObject());
})
```

### 指定构造方法

我们都知道，Mybatis在执行完查询语句后，会自动将查询的结果转换为我们所需要的实体类，那么该具体怎么做呢：

实际上Mybatis一开始会通过实体类默认的无参构造得到一个初步的对象，然后通过反射进行赋值，我们先手动编写一个带有调试信息的无参构造：

```java
public User{
    System.out.prinln("???");
}
```

![QQ_1723726330745](https://oss.itbaima.cn/internal/markdown/2024/08/15/7vFVPi3xXSfGtye.png)

可以看到Mybatis确实调用了我们的无参构造方法来构建对象，属性则是通过反射进行赋值，这里截取部分源代码演示：

```java
//这里的object就是刚刚构造好的实体类对象，prop是要设置的值的字段信息，value就是要设置的值
private void setBeanProperty(PropertyTokenizer prop, Object object, Object value) {
  try {
    //Invoker是Mybatis内部编写一个用于反射设置对象属性值的工具
    Invoker method = metaClass.getSetInvoker(prop.getName());
    Object[] params = { value };
    try {
      method.invoke(object, params);  //通过Invoker为传入的实体类对象赋值
    } catch (Throwable t) {
      throw ExceptionUtil.unwrapThrowable(t);
    }
  } catch (Throwable t) {
    ...
  }
}
```

由于默认情况下直接通过无参构造来创建实体类对象，如果我们的类中存在其他构造方法覆盖默认的无参构造，那么Mybatis会选用可用的构造方法来进行构造。但是，如果存在多个构造方法，Mybatis会出现问题：

```java
@ToString
public class User{
    ...
        public User(int id){
        this.id=id;
    }
    public User(String name,int age){
        this.name=name;
        this.age=age;
    }
}
```

运行时会出现错误。

```
Exception in thread "main" org.apache.ibatis.exceptions.PersistenceException: 
### Error querying database.  Cause: org.apache.ibatis.executor.ExecutorException: No constructor found in com.test.User matching [java.lang.Integer, java.lang.String, java.lang.Integer]
### The error may exist in file:mappers/TestMapper.xml
```

因此，我们不需要删除多余的构造方法，只需要添加一个无参构造或者全参构造即可，注意，全参构造要与查询结果字段一一对应，但是注意，Mybatis仅仅是使用这种方法进行对象的创建，而字段的赋值无论是什么构造方法，都会使用反射进行一次赋值：

```java
public User(int id,String name,int age){
    this.id=id;
    this.name=name;
    this.age=age+20;  //这里我们让age在赋值时增加
}
```

最终结果依然是被赋值的结果，也就是说构造方法在默认情况下仅仅用于构造一个单纯的对象罢了。

如果让Mybatis完全使用构造方法进行对象的构建和赋值操作，那么我们需要手动配置：

```xml
<select id="selectUserById" resultMap="test">
select * from user where if=#{id}
</select>
<resultMap id="test" type="com.test.User">
    <constructor>
        
    </constructor>

</resultMap>
```

这一次，我们在resultMap中添加constructor标签，表示我们的查询结果直接使用指定的构造方法来处理。接着，我们需要配置一下constructr里面的内容，使其符合我们指定构造方法的定义，比如：

```java
public User(int id,String name){
    this.id=id;
    this.name=name+"同学";
    
}
```

那么，对应的xml文件为：

```xml
    <constructor>
        <idArg column="id" javaType="_int"/>  //主键使用idArg
        <arg column="name" javaType="String"/>
        
    </constructor>
```

注意参数的顺序，必须和构造方法的顺序一致，否则会导致Mybatis无法确认。指定构造方法后，若此字段被填入了构造方法作为参数，将不会通过反射给字段单独赋值，而构造方法中没有传入的字段，依然会被反射赋值。

### 接口绑定

之前，我们演示了创建一个映射器来将结果快速转化为实体类，但是这样还是不够方便，我们每次都需要找映射器对应操作的名称，而且还要找对应的类型，再通过SqlSession来执行对应的方法，那么能不能在方便一点呢：

所以，我们可以通过namespace来将各种操作绑定到一个接口上，然后使用方法的形式来表示，注意接口的参数和返回值必须正确对应，否则会出现问题：

```java
public interface TestMapper{
    User selectUserById(int id);
}
```

接着，将Mapper文件的命名空间修改为我们完整的接口名称：

```xml
<select id="selectUserById" resultType="com.test.User">
select * from user where id=#{id}
</select>
```

这里建议将对应的xml配置也放到放到同包中，作为内部资源：

![QQ_1723457472353](https://oss.itbaima.cn/internal/markdown/2024/08/12/N3bTsDLtlS1mckq.png)

作为内部资源后，我们需要修改一下配置文件中的mapper文件目录，不使用url而是resource表示是Jar内部的文件：

```xml
<mappers>
    <mapper resource="com/test/mapper/TestMapper.xml"/>
</mappers>
```

现在我们可以直接通过SqlSession获取我们编写接口的实现类(不用编写，自动生成)

```java
try(SqlSession sqlSession=MybatisUtil.openSession(true)){
    TestMapper mapper=sqlSession.getMapper(TestMapper.class);
    mapper.selectUser().forEach(System.out::println);
}
```

那肯定我们会很好奇，明明我们只编写了一个接口，为什么会自动生成他的实现类？我们可以调用getClass()来观察：

```java
TestMapper tm=sqlSession.getMapper(TestMapper.class);
System.out.println(tm.getClass());
```

我们发现，得到的类名称很奇怪`class jdk.proxy2.$Proxy4`，它其实是通过动态代理生成的，相当于在程序运行过程中动态生成了一个实现类，而不是预先定义好的，有关原理需要你们自己去了解。

我们继续：

有些时候，我们查询操作可能需要不止一个参数：

```xml
<select id="selectUserByIdAndAge" resultType="com.test.entity.User">
select * from user where id=#{id} and age=#{age}
</select>
```

一种最简单的方式就是和之前一样，我们使用一个Map作为参数，然后将这些参数添加到Map中进行传递：

```java
User selectUserByIdAndAge(Map<String, Object> map);
```

```java
TestMapper mapper = session.getMapper(TestMapper.class);
System.out.println(mapper.selectUserByIdAndAge(Map.of("id", 1, "age", 18)));
```

只不过，这样编写实在是太复杂了，要是由一种更简单的方式就好了，我们也可以直接将这两个参数定义到形参列表中：

```java
User selectUserByIdAndage(int id,int age);
```

这种方式查询，Mybatis并不能正确获取对应参数，这是因为Java代码编译后形参名称无法保留，导致Mybatis无法确定具体哪个参数叫什么名字，所以我们通过这样命名，{param1},#{param2}：

```sql
select * from user where id=#{param1} and age=#{param2}
```

当然，如果你实在需要使用对应的属性名称，我们也可以手动添加一个@Param注解来指定某个参数的名称：

```java
User selectUserByIdAndAge(@Param("id") int id, @Param("age") int age);
```

这样Mybatis就可以正确识别了。

### 复杂查询

前面介绍了简单查询，这节课我们学习一对一，多对一，一对多的实现方式。

#### 一对一

首先，我们来看一对一查询，假设，每个用户都有自己的详细信息表：
![QQ_1723792352474](https://oss.itbaima.cn/internal/markdown/2024/08/16/M4SX2Woa9CybQUw.png)

这里的id与用户的id一致，作为用户id的逻辑外键，表示对应用户的详细信息，对应实体类为：

```java
@Data
public class UserDetail{
    int id;
    String description;
    Date register;
    String avatar;
}

@Data
public class User{
    int id;
    String name;
    int age;
    UserDetail detail;
}
```

现在，我们想要在查询User的同时，查询用户的详细信息，这就是一对一，需要用到resultMap来自定义映射规则：

```xml
<select id="selectUserById" resultMap="test">
</select>
<resultMapp id="test" type="com.test.entity.User">
</resultMap>
```

Mybatis有两种不同的方式加载关联：

- 嵌套结果映射：使用嵌套的结果映射来处理连接结果的重复子集。
- 嵌套Select查询：通过执行另外一个SQL映射语句来加载期望的复杂类型。

##### 嵌套结果映射

我们先来看第一种，这里我们需要使用关联查询将用户的详细信息一并获取，然后配置关联查询相关信息，最后由Mybatis来对查询的结果进行处理即可，首先是关联查询的SQL语句，这里我们使用左连接：

```sql
select * from user left join user_detail on user.id=user_detail.id where user.id=#{id}
```

接着，我们需要在resultMap编写好对应关系，一对一查询我们可以使用association标签来指定，其中property是我们需要一对一处理的对象，在此标签内部填写需要进行一对一映射的对象属性：

property是实体类属性，column是数据库表的属性。

```xml
<resultMap id="test" type="com.test.entity.User">
    <id property="id" column="id"/>
    <result property="name" column="name"/>
    <result property="age" column="age"/>
    <!-- detail是实体类属性，用user表中id列去匹配uers_detail表的对用字段 -->
    <association property="detail" column="id" javaType="com.test.entity.UserDetail">
        <id property="id" column="id"/>
        <result property="description" column="description"/>
        <result property="register" column="register"/>
        <result property="avatar" column="avatar"/>
    </association>
</resultMap>
```

配置完成后，我们在查询Mybatis就可以自动把额外信息也封装好了：

![QQ_1723796178911](https://oss.itbaima.cn/internal/markdown/2024/08/16/3e6fAudX7G9qFsU.png)

##### 嵌套Select语句查询

接着，我们看第二种连接方式，使用嵌套select语句查询，也就是说，我们可以在查询user表的时候，同时查询user_detail表对应信息，分别执行两个选择语句，最后将由Mybatis将结果合并，效果和第一种方法一样：

```xml
<select id="selectUserById" resultMap="test">
    select * from user where id = #{id}
</select>
<resultMap id="test" type="com.test.entity.User">
    <id property="id" column="id"/>
    <result property="name" column="name"/>
    <result property="age" column="age"/>
    <association property="detail" column="id" select="selectUserDetailById" javaType="com.test.entity.UserDetail"/>
</resultMap>

<select id="selectUserDetailById" resultType="com.test.entity.UserDetail">
    select * from user_detail where id = #{id}
</select>
```

我们配置了两个select标签分别查询用户的基本信息和详细信息，并用association来指定关联，得到的结果是一样的。

我们可以开启Mybatis的日志来观察具体执行的操作，这需要我们在Mybatis配置文件添加：

```xml
<settings>
    <setting name="logImpl" value="STDOUT_LOGGING"/>
</settings>
```

这样就会打印日志到控制台了：

```
...
Opening JDBC Connection
Created connection 1962329560.
==>  Preparing: select * from user where id = ?
==> Parameters: 1(Integer)
<==    Columns: id, name, age
<==        Row: 1, 小明, 18
====>  Preparing: select * from user_detail where id = ?
====> Parameters: 1(Integer)
<====    Columns: id, description, register, avatar
<====        Row: 1, 我是一个阳光开朗大男孩, 2024-08-16 15:15:03, https://www.baidu.com
<====      Total: 1
<==      Total: 1
User(id=1, name=小明, age=18, detail=UserDetail(id=1, description=我是一个阳光开朗大男孩, register=Fri Aug 16 15:15:03 CST 2024, avatar=https://www.baidu.com))
Closing JDBC Connection [com.mysql.cj.jdbc.ConnectionImpl@74f6c5d8]
Returned connection 1962329560 to pool.
```

日志中，`==>`是发送给MySQL服务器的SQL语句以及其参数列表，`<==`是得到的结果，可以看到，这里一共执行了两次sql语句，分别是user表和user_detail表的查询操作。

#### 一对多

接下来看一对多查询，现在来一个新的表，用于存放用户借阅的图书，对应实体类如下：

```java
@Data
public class Book {
    int bid;
    String title;
    int uid;
}

@Data
public class User {
    int id;
    String name;
    int age;
    List<Book> books;   //直接得到用户所属的所有书籍信息
}
```

其中，uid作为book的逻辑外键，表示这本书是谁借的。

对于多对一查询，我们也可以进行关联查询让Mybatis自动解析结果并封装为对象，首先还是关联查询的SQL语句，这里我们让user左连接book表中：

```sql
select * from user left join book on user.id=book.uid where user.id=#{id}
```

![QQ_1723802885239](https://oss.itbaima.cn/internal/markdown/2024/08/16/4Ijp6iU5P9X2N8u.png)

这里配置xml文件时，我们需要collection标签来联合，Mybatis会根据我们配置的属性自动将关联数据变为一个集合并存放在对象中：

```xml
<resultMap id="test" type="com.test.entity.User">
    <id column="id" property="id"/>
    <result column="name" property="name"/>
    <result column="age" property="age"/>
    <collection property="books" ofType="com.test.entity.Book">
        <id column="bid" property="bid"/>
        <result column="title" property="title"/>
    </collection>
</resultMap>
```

![QQ_1723734667720](https://oss.itbaima.cn/internal/markdown/2024/08/15/udbylhUV7GT9znm.png)

#### 多对一

了解了一对多，那么多对一呢？

比如，每个用户都有一个小组，但是他们目前都在同一个小组中，此时我们查询所有用户信息的时候，需要自动携带他们的小组：
gid作为分组id的逻辑外键：

![QQ_1723818596301](https://oss.itbaima.cn/internal/markdown/2024/08/16/dsWXt4pEATocyRO.png)

接着，是实体类的设计：

```java
@Data
public class Group{
    int id;
    String name;
}

@Data
public class User{
    int id;
    String name;
    int age;
    Group group;
}
```

接着编写sql映射：

```sql
select *, groups.name as gname from user left join `groups` on user.gid = groups.id
```

注意，sql语句中一些字段存在歧义，我们需要手动为其写别名。

接着，xml编写：

```xml
<select id="selectAllUser" resultMap="test2">
    select *, groups.name as gname from user left join `groups` on user.gid = groups.id
</select>
<resultMap id="test2" type="com.test.entity.User">
    <id column="id" property="id"/>
    <result column="name" property="name"/>
    <result column="age" property="age"/>
    <association property="group">
        <id column="gid" property="id"/>
        <result column="gname" property="name"/>
    </association>
</resultMap>
```

### DML查询

接着，我们来看看修改相关的操作，Mybatis为我们提供了几个预设方法：

```java
int insert(String statement);
int insert(String statement, Object parameter);
int update(String statement);
int update(String statement, Object parameter);
int delete(String statement);
int delete(String statement, Object parameter);
```

可以看到，返回结果是int类型的，与JDBC一样，他代表执行SQL后受影响的行数。

接着，我们尝试编写一个插入操作，我们可以直接让User对象作为参数传入：

```xml
<insert id="addUser" parameterType="com.test.entity.User">
        insert int user(name,age)values(#{name},#{age})
</insert>
```

这里，我们将parameterType类型设置为我们的实体类型，这样下面在使用#{name}时Mybatis就会自动调用类中对应的Get方法来获取结果，不过，Mybatis也会自动判断。

有些时候，我们的数据插入后使用的是一个自增主键ID，那么我们该如何获取到该键的值呢：

```xml
<insert id="addUser" parameterType="com.test.entity.User" useGeneratedKeys="true" keyProperty="id" keyColumn="id">
    insert int user(name,age)values(#{name},#{age})
</insert>
```

useGenerateKeys设置为true表示我们希望获取数据库生成的键，keyProperty设置为User类中需要获取自增结果的属性名，keyColumn为数据库中自增的字段名称，但是一般不需要手动设置，但是某些数据库（像PostgreSQL）中，当主键列不是表中第一列的时候，必须设置。

这样我们就可以获取到自增后的值了：

![QQ_1723824700173](https://oss.itbaima.cn/internal/markdown/2024/08/17/OUWu97HmpPNyB1K.png)

和之前一样，我们也可以直接将其绑定到一个接口上：

```java
public interface TestMapper{
    int addUser(User user);
}
```

注意返回类型必须是int或者long，表示生效的行数。

接着，我们来看看修改操作，比如根据ID修改年龄：
```xml
<update id="setUserAgeById">
    update user set age=#{age} where id=#{id}
</update>
```

```java
int setUserAgeById(User user);
```

这里的参数我们选择使用User，和之前的insert一样，Mybatis会从传入的对象自动获取需要的参数，当然我们也可以将此方法设计为两个参数的形式：

```java
int setUserAgeById(@Param("age") int age ,@Param("id") int id);
```

删除操作：假设我们根据用户的id进行数据的删除：

```xml
<delete id="deleteUserById">
    delete from user where if=#{id}
</delete>
```

### 事务操作

我们可以获取SqlSession关闭自动提交来开启事务模式，和JDBC差不多，在创建SqlSession的时候不填写参数默认使用的就是事务模式：

```java
try(SqlSession session=sqlSessionFactory.openSession(false)){...}
```

我们发现，关闭自动提交后，内容是没有进入数据库中的：

```java
try(SqlSession session=MybatisUtils.openSession(false)){
    TestMapper mapper=session.getMapper(TestMapper.class);
    mapper.deleteUserById(1);  //虽然日志中已经提示生成1行，但是并没有提交
}
```

SqlSession接口为我们提供了事务操作相关方法，这里我们可以直接尝试进行事务的提交：

```java
TestMapper mapper=session.getMapper(TestMapper.class);
mapper.deleteUserById(7);
session.commit();  //通过SqlSession进行事务提交
```

注意，如果在提交事务之前没有进行任何的DML操作，那么调用commit也不会提交，但强制提交使用commit(true)。

回滚操作：

```java
TestMapper mapper = session.getMapper(TestMapper.class);
mapper.deleteUserById(1);
System.out.println(mapper.selectUserById(1));   //此时由于数据被删除，无法查到
session.rollback();   //进行回滚操作
System.out.println(mapper.selectUserById(1));   //之前被删除的数据回来了
```

### 动态SQL

在之前，讲解JDBC的时候，我们提到了批量执行语句的问题，当我们要执行很多条语句时，可能会一条一条提交：

```java
//现在要求把下面所有用户都插入到数据库中
List<String> users = List.of("小刚", "小强", "小王", "小美", "小黑"););
//使用for循环来一个一个执行insert语句
for (String user : users) {
    statement.executeUpdate("insert into user (name, age) values ('" + user + "', 18)");
}
```

如果把任务合在一起告诉数据库，效率会提高很多。

同样，我们推荐使用批处理来优化，一次性提交一个批量操作。

需要在Mybatis开启批处理，我们只需要创建SqlSession时进行一些配置：

```java
factory.openSession(ExecutorType.BATCH,autoCommit);
```

在使用openSession时直接配置ExecutorType为BATCH即可，这样SqlSession还会开启批处理模式，在多次处理相同SQL时会尽可能转换为一次执行，开启批处理后，无论是否处于事务模式下，我们都需要flushStatement()来一次性提交之前的所有批处理操作：

```java
TestMapper mapper=session.getMapper(TestMapper.class);
for(int i=1;i<=5;i++){
    mapper.deleteUserById(i);
}
session.flushStatement();
```

此时，日志中能看到Mybatis的优化SQL操作：

![QQ_1724050907084](https://oss.itbaima.cn/internal/markdown/2024/08/19/b2ZexXIYiHSsM7v.png)

处理批处理之外，还有一种方式，那就是使用动态SQL来一次性生成一个批量操作的SQL语句，这里先介绍一下什么是动态SQL。

> 动态SQL是Mybatis的特性之一。动态SQL在执行时可以进行各种条件判断以及循环拼接等操作，极大地提高了SQL语句编写的灵活性。

我们先来看看条件判断，在编写SQL时，我们可以添加一些用于条件判断的标签到SQL语句中，比如，我们希望再根据id查询用户时，如果查询的ID大于3，那么必须满足大于等于18，此时，动态SQL就能很轻松的实现这个操作：

```xml
<select id="selectUSerById" resultType="User">
    select * from user where id=#{id}
    <if test="id>3">
        and age>18
    </if>
</select>
```

这里if标签表示里面的内容会在判断条件满足时拼接到后面，如果不满足，那么就不拼接里面的内容到原本的SQL中，其中test属性就是我们需要填写的判断条件，它采用OGNL表达式进行个编写。

可以看到，当查询条件不同时，Mybatis会选择性拼接我们的SQL语句：

![QQ_1724052613799](https://oss.itbaima.cn/internal/markdown/2024/08/19/fSOXZdTjFR4oMgP.png)

除了if之外，Mybatis还提供了choose操作，类比于switch：

```xml
<select id="selectUserById" resultType="User">
    select * from user where id=#{id}
    <choose>
        <when test="id==1">
            and age &lt;=18
        </when>
        <when test="id==2">
            and age=18
        </when>
        <otherwise>
            and age>18
        </otherwise>
    </choose>
</select>
```

注意when中不允许使用<>这种模糊匹配操作。

最后，我们介绍一下foreach操作，他与java中的for类似，实现批量操作：

```java
for(int i=1;i<=5;i++){
    mapper.deleteUserById(i);
}
```

但实际上，这完全可以简写成一个SQL语句：

```sql
DELETE FROM users WHERE id IN(1,2,3,4,5);
```

所有，现在使用foreach来完成就简单了：

```xml
<delete id="deleteUsers">
    delete from user where id in
    <foreach collection="list" item="item" index="index" open="(" separator="," close=")">
        #{item}
    </foreach>
</delete>
```

其中collection就是我们需要遍历的集合或者数组等任意可迭代对象，item和index分别代表我们在foreach中使用的每一个元素和下标的变量名称，open和close用于控制起始和结束位置添加的符号，separator用于控制分隔符，然后执行操作：

```java
session.delete("deleteUsers",List.of(1,2,3,4,5));
```

最后执行的SQL语句为：

![QQ_1724059653501](https://oss.itbaima.cn/internal/markdown/2024/08/19/rFP1oJNM56ZebA4.png)

我们再来看一个例子，比如现在我们想要批量插入一些用户到数据库中，原本Java应该：（不推荐）

```java
TestMapper mapper = session.getMapper(TestMapper.class);
List<User> users = List.of(new User("小美", 17),
        new User("小张", 18),
        new User("小刘", 19));
for (User user : users) {
    mapper.insertUser(user);
}
```

实际上这种操作完全可以浓缩为一个SQL语句：

```sql
INSERT INTO user (name, age) VALUES ('小美', 17), ('小张', 18), ('小刘', 19);
```

那这时又可以直接使用咱们的动态SQL来完成操作了：

```xml
<insert id="insertAllUser">
    insert into user (name, age) values
    <foreach collection="list" item="user" separator=",">
        (#{user.name}, #{user.age})
    </foreach>
</insert>
```

![QQ_1724060416443](https://oss.itbaima.cn/internal/markdown/2024/08/19/DRAt7hbdZizqpSk.png)



通过使用动态SQL语句，我们基本上可以解决大部分的SQL查询和批量处理场景了。

### 缓存机制

其实缓存机制在我们学习IO流的时候已经介绍过了，我们可以提前将一部分内容放进缓存，下次需要获取数据时，就可以直接从缓存中获取，这样的话相当于直接从内存中获取而不是去数据库索要数据，效率会更高。

Mybatis为了查询效率，同样内置了一个缓存机制，我们在查询时，如果Mybatis中存在数据，那么我们可以直接从缓存中获取，而不是再去数据库中请求，节省性能开销。

![image-20230306163638882](https://oss.itbaima.cn/internal/markdown/2024/08/20/Vn4fQlW1roPMaDH.png)

Mybatis的缓存机制有点复杂，存在一级缓存和二级缓存，首先先来看一级缓存，默认情况下，只启用一级缓存，他仅仅对一个会话中的数据进行缓存（一级缓存强制启用，只能做调整）也就是每一个SqlSession都由一个对应的缓存，我们先来看看这段代码：

```java
TestMapper mapper=session,getMapper(TestMapper.class);
System.out.println(mapper.selectUserById(1));
System.out.println(mapper.selectUserById(1));  //再次获取
```

这里，我们连续获取了两次ID相同的用户，我们在日志中发现，查询操作只执行了一次。

![QQ_1724167595196](https://oss.itbaima.cn/internal/markdown/2024/08/20/OlFMk4gEYTZf2NC.png)

我们去掉@Data注解，会发新得到的两个对象是实际上是同一个：
![QQ_1724167645759](https://oss.itbaima.cn/internal/markdown/2024/08/20/4iTIlZgFa3JS5RM.png)

也就是说，我们的第二次查案寻不仅压根没执行SQL语句，甚至直接没有重新构造对象，而是直接获取好之前创建好的。可见，Mybatis确实存在缓存机制来进行性能优化。

那么，如果我们修改了数据库的内容，缓存还会生效吗：

```java
System.out.println(mapper.selectUserById(1));
mapper.updateAgeById(1,19);
System.out.println(mapper.selectUserById(1));
```

此时，我们更新了数据库的数据，之前缓存的内容也会失效，第二次获取时会重新查新。也就是说Mybatis知道我们对数据库里面的数据进行了修改，所以之前缓存的内容就不是当前数据库里面最新的内容了。但一定注意，一级缓存只针对单个会话，多个会话之间并不相通。

因此，一个会话DML操作指挥重置当前会话的缓存，不会重置其他会话的缓存，我们可以实验一下：
```java
try(SqlSession s1=MybatisUtils.openSession(true);
   SqlSession s2=MybatisUtils.openSession(true)){
    TestMapper m1=s1.getMapper(TestMapper.class);
    TestMapper m2=s2.getMapper(TestMapper.class);
    System.out.println(mapper.selectUserById(1));
    mapper.updateAgeById(1,19);
    System.out.println(mapper.selectUserById(1));
}
```

可以看到，没有影响会话的缓存。

一级缓存为我们提供了很高速的访问效率，但是它的作用范围实在是有限，如果一个会话结束，那么之前的缓存就全部失效了，但是我们希望将缓存扩展到所有会话全都能使用。

我们可以通过二级缓存来实现，二级缓存默认是关闭状态，我们在映射器xml中添加：

```xml
<cache/>
```

二级缓存是Mapper级别的，只要使用到Mapper的会话，都会关联到二级缓存，无论哪个会话失效，他之前查询的缓存依然会存在于二级缓存中，依然会被其他会话直接使用。

我们可以对cache配置：

```xml
<cache
       eviction="FIFO"
       flushInterval="60000"
       size="512"
       readOnly="true"/>
```

其中，size表示最大的缓存对象数量，当缓存达到上限时，会根据eviction配置的策略进行清理：

- `LRU` 表示最近最少使用：移除最长时间不被使用的对象。
- `FIFO` 表示先进先出：按对象进入缓存的顺序来移除它们。
- `SOFT` 表示软引用：基于垃圾回收器状态和软引用规则移除对象。
- `WEAK` 表示弱引用：更积极地基于垃圾收集器状态和弱引用规则移除对象。

flushInterval用来控制缓存刷新时间，当到达指定时间时会自动清理所有缓存，默认情况下如果不配置此项则不会进行定时清理。readOnly属性可被设置为true或者false，只读的缓存会给所有调用者返回相同的缓存对象，且对象不能被修改。这就提供了可观的性能提升，而可读写的缓存（通过序列化）返回缓存对象的拷贝，速度上会慢一些，但是更安全，因此默认值是false。

注意：二级缓存是事务性的，这意味着，当SqlSession结束并提交时，或是结束并回滚，而且没有执行flushCache=true的insert/delete/update语句时，缓存才会被更新。

开启二级缓存后，再次执行我们之前的操作，就可以直接在二级缓存命中了：
![QQ_1724169383598](https://oss.itbaima.cn/internal/markdown/2024/08/20/iIZPElyrYN2RdKf.png)

实际上，在开启二级缓存后，Mybatis会先从二级缓存中查找数据，当二级缓存没有时，才会从一级缓存中获取，当一级缓存中都还没有数据时，才会请求数据库。

当我们开启二级缓存后，默认情况下，一个Mapper中所有操作都会使用二级缓存，我们也可以单独配置其不使用二级缓存，只需要修改useCache属性即可：

```xml
<select id="selectUserById" useCache="false" resultType="com.test.User">
    select * from user where id = #{id}
</select>
```

有些操作比较特殊，比如共我们希望执行完某个操作后，直接清除所有缓存，无论是一级缓存还是二级缓存，那么此时就可以开启flushCache操作：

```xml
<select id="selectUserById" flushCache="false" resultType="com.test.User">
    select * from user where id = #{id}
</select>
```

开启次选项后，调用此操作将会直接导致一级二级缓存被清除。

虽然缓存会给我们提供很大的性能提升，但是缓存存在一个问题，叫做缓存一致性问题，也就是说当多个CPU在操作自己的缓存时，可能会出现各自的缓存内容不同步的问题。

![image-20230306163717033](https://oss.itbaima.cn/internal/markdown/2024/08/20/f4hm7o8jcrXbul6.png)

而Mybatis也会这样，我们来看看这个例子：

```java
TestMapper mapper = session.getMapper(TestMapper.class);
while (true){
    Thread.sleep(3000);
    System.out.println(mapper.selectUserById(1));
}
```

我们现在每循环三秒读取一次，在这个过程中，我们使用其他软件手动修改数据库中的数据，将1号用户的ID改成100，那么理想情况下，下一次读取将直接无法获取到这行数据，因为ID已经发生了变化。

当时结果是依然能够读取，并且sid并没有发生改变，证明了Mybatis的缓存在生效，因为我们是从外部进行修改，Mybatis不知道我们修改了数据，所以依然在使用缓存中的数据，但是这样很明显是不正确的，因此，如果存在多台服务器或者是多个程序都在使用Mybatis操作同一个数据库，并且都开启了缓存，需要解决这个问题，我们只能关闭所有二级缓存，并且在Mybatis每个操作都配置`flushCache`为true来保证刷新。

只不过这种操作实际上是治标不治本的，实现多服务器缓存共用才是最终解决方案，也就是让所有的Mybatis都使用同一个缓存进行数据存取，在后面，我们会继续学习Redis、Ehcache、Memcache等缓存框架，通过使用这些工具，就能够很好地解决缓存一致性问题。

### 使用注解

在之前的学习中，我们已经体验到Mybatis为我们带来的便捷了，我们只需要编写对应的映射器，并将其绑定到一个接口上，即可直接通过该接口执行我们的SQL语句，极大的简化我们之前JDBC那样的编码编写模式。

那么，接下来，我们实现无需xml映射器配置，直接使用注解在接口上进行配置。

现在，让我们删除Mapper.xml文件，，只保留Mapper相关的接口。

还是以查询所有用户为例，既然不需要配置Mapper.xml文件，那么我们现在需要重写在Myabtis的配置文件中进行mapper的配置，因为现在只需要使用接口来进行配置，所以使用package来指定一个包，包下所有接口都将直接作为Mapper配置接口：

```xml
<mapper>
    <package name="com.test.mapper"/>
</mapper>
```

现在我们还是在Mapper中添加一个对应的方法用于执行：

```java
public interface TestMapper{
    List<User>selectAllUser();
}
```

之前，我们需要这样编写：

```xml
<select id="selectAllUser" resultType="com.test.User">
    select * from user
</select>
```

现在，只需要一个注解即可，Mybatis为我们提供了丰富的注解用于表示不同的SQL语句这里的@Select代表的就是select标签，我们只需要直接编写SQL语句即可，而返回类型Mybatis会自动根据方法的返回值进行判断：

```java
public interface TestMapper{
    @Select("select * from user")
    Lisr<User>selectAllUser();
}
```

![QQ_1724143033753](https://oss.itbaima.cn/internal/markdown/2024/08/20/ALdMlG5evncp4kH.png)

包括一些SQL语句参数的使用也和之前完全一样，比如插入一个用户：

```java
@Insert("insert into user(name,age)values(#{name},#{age})")
int insertUser(User user);
```

虽然Mybatis为我们提供了之前xml配置中各种操作的对应注解，但是我们发现，这些注解并不能像之前xml那样直接修改一些属性，比如这里我们希望配置useGeneratedKeys来得到自动生成的主键，需要配置这些额外的参数，我们可以使用@Options注解：

```java
@Options(useGeneratedKeys = true,keyColumn="id",keyProperty="id")
@Insert("insert into user(name,age)values(#{name},#{age})")
int insertUser(User user);        
```

```xml
<insert id="insertUser" parameterType="com.test.entity.User" useGeneratedKeys="true"keyProperty="id"keyColumn="id">
    insert * from user(name,age)values(#{name},#{age})
</insert>
```

这两种写法效果完全一样，所以我们通过Mybatis为我们设计的这一系列注解就可以很轻松地取代掉之前地配置。

假设我们的实体类字段名称和数据库不同，此时该如何像之前一样配置resultMap呢？

```java
public class User {
    int uid;
    String username;
    int age;
}
```

```xml
<resultMap id="test" type="User">
    <id property="uid" column="id"/>
    <result column="name" property="username"/>
</resultMap>
```

我们可以使用`@Results`注解来实现这种操作，它的使用方式与resultMap几乎没什么区别：

```java
@Results({
        @Result(id = true, column = "id", property = "uid"), 
    // id=true表示这是主键字段
        @Result(column = "name", property = "username")
})
@Select("select * from user")
List<User> selectAllUser();
```

是不是感觉很简单？当然，如果你还是觉得这种方式配置起来不如之前方便，那么你也可以单独在XML中配置一个resultMap然后直接通过注解的形式引用：

```java
@ResultMap("test")
@Select("select * from user")
List<USer>selectAllUser();
```

那么，现在如果我们需要指定构造方法怎么办？就像我们之前在使用constrator标签一样，Mybatis为我们提供了@ConstructorArgs注解，配置方法与之前一致：

```java
public class User {
    int id;
    String name;
    int age;

    public User(int id, String name, int age) {
        this.id = id;
        this.name = name;
        this.age = age + 20;
    }
}
```

```java
@ConstructorArgs({
        @Arg(id = true, column = "id", javaType = int.class),
        @Arg(column = "name", javaType = String.class),
        @Arg(column = "age", javaType = int.class)
})
@Select("select * from user")
List<User> selectAllUser();
```

这与我们之前的XML配置完全一致：

```xml
<constructor>
    <idArg column="id" javaType="_int"/>
    <arg column="name" javaType="String"/>
    <arg column="age" javaType="_int"/>
</constructor>
```

我们再来看看之前的resultMap中配置的关联查询该如何编写，Mybatis也为我们提供了丰富的注解用于处理这类问题，我们先来看一对一查询：

```java
@Results({
    @Result(id=true,column="id",property="id"),
    @Result(column="id",property="detail",one=@One(select="selectDetailById"))
})
@Select("select * from user where id=#{id};")
User selectUserById(int id);
@Select("select * from user_detail where id=#{id};")
UserDetail selectDetailById(int id);
```

我们在配置@Result注解时，只需要将one或是many参数进行填写即可，他们分别代表一对一关联或者是一对多关联，使用@One和@Many注解来指定其他查询语句进行嵌套查询。

不过遗憾的是，我们无法完全通过注解来实现之前的联合查询解析（这是因为JAVA注解不允许循环使用）只能使用这种嵌套查询来完成复杂查询操作，因此，如果对这种复杂查询有着一定需求的话，建议使用之前的xml方式进行配置。

我们还可以使用注解进行动态SQL配置：

```xml
<select id="selectUserById" resultType="User">
    select * from user where id=#{id}
    <if test="id>3">
        and age>18
    </if>
</select>
```

Mybatis针对所有的SQL操作都提供了对应的Provider注解，用于配置动态SQL，我们需要先创建一个类编写我们的动态SQL操作：

```java
public class TestSqlBuilder{
    public static String buildGetUserById(int id){
        return new SQL(){{
            SELECT("*");
            FROM("user");
            WHERE("id=#{id}");
            if(id>3){
                WHERE("age>18");
            }
        }}.toString();
    }
}
```

构建完成后，接着我们使用@SelectProvider来引用这边编写好的动态SQL操作：

```java
@SelectProvider(type=TestSqlBuilder.class,method="buildGetUserById")
User selectUserById(int id);
```

效果和之前我们编写xml形式的动态SQL一致，当然，如果遇到了多个参数的情况，我们同样需要使用@Param来指定参数名称，包括TestSqlBuilder中编写的方法也需要添加，否则必须保证形参列表与这边接口一致。

虽然这样可以实现与之前差不多的效果，但是太复杂了，我们还需要单独编写一个类来做这种事情，实际上我们可以直接在@Select中编写一个xml配置动态SQL，Mybatis正常解析：

```java
@Select("""
        <script>
            select * from user where id=#{id}
            <if test="id>3">
        		and age>18
        	</if>
        </script>
        """)
User selectUserById(int id);
```

这里只需要包括一个script标签我们就能像之前XML那样编写动态SQL了，只不过由于IDEA不支持这种语法的识别，可能会出现一些莫名其妙的红标，但是是可以正常运行的。

最后我们来看一下二级缓存相关的配置，使用`@CacheNamespace`注解直接定义在接口上即可，然后我们可以通过使用`@Options`来控制单个操作的缓存启用：

```java
@CacheNamespace(size = 512, readWrite = false)
public interface TestMapper {
```

我们如果需要控制单个方法的缓存，同样可以使用`@Option`来进行配置：

```java
@Options(flushCache = Options.FlushCachePolicy.TRUE, useCache = false)
@Select("select * from user where id = #{id}")
User selectUserById(int id);
```

这里我们不如再做的更加极致一点，咱们把配置文件也给变成代码配置，彻底抛弃XML配置，实际上我们的XML配置中所有配置项都可以以Configuration对象的形式进行配置，最后在构造SqlSessionFactory时也可以通过此对象进行创建：

```java
private static Configuration initConfiguration() {
    Configuration configuration = new Configuration();
    PooledDataSource dataSource = new PooledDataSource(
            "com.mysql.cj.jdbc.Driver",
            "jdbc:mysql://localhost:3306/web_study",
            "test",
            "123456");
    Environment environment = new Environment("development", new JdbcTransactionFactory(), dataSource);
    configuration.setEnvironment(environment);
    configuration.getTypeAliasRegistry().registerAliases("com.test.entity");
    configuration.setLogImpl(StdOutImpl.class);
    configuration.addMappers("com.test.mapper");
    return configuration;
}
```

有关Mybatis的基本使用，我们就暂时介绍到这里。
