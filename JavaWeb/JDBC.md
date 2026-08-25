# JDBC

JDBC是什么呢？Java Data Base Connectivity（Java数据库连接）官方解释是Java语言与广泛数据库之间独立于数据库的连接标准API，根本上说JDBC是一种规范，它提供的接口，一套完整的，允许便捷式访问底层数据库。可以用Java来写不同类型的可执行文件：Java应用程序，Java Applets，Java Servlet，JSP等，不同的可执行文件都通过JDBC来访问数据库，又兼容了存储优势。简单来说就是Java与数据库的连接的桥梁，用Java代码就能操作数据库的增删改查、存储过程、事务等等。

我们可以发现，JDK自带了一个java.sql包，而这里面就定义了大量的接口，不同类型的数据库，都可以通过实现此接口，编写适用于自己的数据库实现类。而不同的数据库厂商实现的这套标准，我们称之为数据库驱动。

## 使用JDBC连接数据库

当我们成功引入了MySQL数据库驱动以后，我们就可以正式使用JDBC了，在这之前我们可以先打印一下看看自己的依赖是否成功接入：

```java
public static void main(String[] args){
      //DriverManager是管理数据库驱动的工具类，我们可以通过它来查看当前是否已经引入的驱动列表
    DriverManager.drivers().forEach(System.out::println);
}
```

结果如下图所示：

![QQ_1721900134689](https://oss.itbaima.cn/internal/markdown/2024/07/25/7yATgfIEeHmY6MG.png)

要访问一个数据库，第一步肯定是创建一个新的连接，我们可以通过DriverManager来创建一个新的数据库连接：

```java
try(Connection connection=DriverManager.getConnection("连接url","用户名,"密码")){
    
}catch(SQLException e){
    e.printStackTrace();
}
```

还记得我们再上一章讲到的网站url吗。互联网上的所有资源，都有一个唯一确定的url，而MySQL本身也是以一个服务端的形式运行的，我们要连接也需要对应的url才行：

```
jdbc:mysql://localhost:3306/study
```

接着，我们要创建一个用于执行SQL的Statement对象，然后就可以像在命令行中那样直接使用SQL命令了：

```java
try(Connection connection =DriverManager.getConnection("jdbc:mysql://localhost:3306/study","root","123456");
    Statement statement=connection.createStatement()){
    //使用executeQuery来执行一个查询SQL语句
    ResultSet rs=statement.executeQuery("select * from student");
}catch(SQLException e){
    e.printStackTrace();
}
```

这里我们得到一个ResultSet对象，我们使用它来获取查询结果，它类似于迭代器，需要使用next来向下迭代，但是使用上会有些小小的差别：

```java
ResultSet rs=statement.executeQuary("select * from student");
while(rs.next()){
    System.out.println("rs.getInt("sid")+" "");
    System.out.println("rs.getString("name")+" "");
    System.out.println("rs.getSex("sex")+");
}
```

## 了解DriverManager

我们知道，要操作数据库，需要通过DriverManager.getConnection创建连接，而开始连接之前，JDBC会自动扫描我们所有引入的数据库驱动并进行加载，此时会调用registerDriver方法完成对Driver接口实现类的加载：

```java
public static void registerDriver(java.sql.Driver driver, DriverAction da)
    throws SQLException {
    /* Register the driver if it has not already been added to our list */
    if (driver != null) {
        registeredDrivers.addIfAbsent(new DriverInfo(driver, da));
    } else {
        // This is for compatibility with the original DriverManager
        throw new NullPointerException();
    }
    println("registerDriver: " + driver);
}
```

这里我们提到，系统会自动发现Driver接口的实现类并加载，这实际上是一种SPI机制：

> Java的SPI（Service Provider Interface）机制是一种服务发现机制，它允许通过接口来加载服务实现。SPI通常用于在框架或库中提供可插拔的功能，使得不同的实现可以被动态加载和使用。这个机制在Java的标准库和许多开源项目中得到了广泛应用。

我们之前多多少少接触过API的概念，实际上我们使用的许多类都是一种API，比如集合类，我们使用的往往是其接口，我们不需要关心其具体实现内容，我们只需要知道接口定义某个方法的用途，按照接口的定义去使用即可。

而SPI来到了另一侧，也就是说接口定义了这些操作，我们需要去实现接口定义的这些操作，这样才可以使得这个功能可以实实在在的使用。（每个数据库厂商使用的接口具体实现是不一样的，JDBC只负责提供接口，厂商是需要自己具体实现，而SPI为数据库厂商提供了一个接口的规范）

当数据库驱动加载完成后，才可以继续完成数据库连接的建立，我们在上一节的实例代码中直接使用了getConnection创造连接，我们可以观察一下getConnection做了什么：

```java
@CallerSensitive
public static Connection getConnection(String url,
    String user, String password) throws SQLException {
    java.util.Properties info = new java.util.Properties();
		//这里判断的是数据库用户名和密码是否填写
    if (user != null) { 
        info.put("user", user);
    }
   	...
		//接着会调用内部的私有getConnection方法
    return (getConnection(url, info, Reflection.getCallerClass()));
}
```

```java
private static Connection getConnection(
    String url, java.util.Properties info, Class<?> caller) throws SQLException {
    //这里需要通过调用此方法的类来获取其类加载器，便于后续加载数据库驱动
    ClassLoader callerCL = caller != null ? caller.getClassLoader() : null;
    if (callerCL == null || callerCL == ClassLoader.getPlatformClassLoader()) {
        callerCL = Thread.currentThread().getContextClassLoader();
    }
		//检查数据库连接的url是否为空，如果是直接报错
    if (url == null) {
        throw new SQLException("The url cannot be null", "08001");
    }
  	...
		//这一步用于确保数据库驱动已经全部加载，包括上面在一开始说的数据库驱动加载部分
    ensureDriversInitialized();
    // 遍历所有已经加载的驱动，然后有合适的就可以直接建立连接了
    SQLException reason = null;
    for (DriverInfo aDriver : registeredDrivers) {
        // 如果调用此方法的Class有权限加载并使用当前驱动，就可以开始创建连接了
        if (isDriverAllowed(aDriver.driver, callerCL)) {
            try {
                ...
                Connection con = aDriver.driver.connect(url, info);
                if (con != null) {
                    // 如果连接不为空，则创建成功，这里直接就返回了
                    ...
                    return (con);
                }
            } catch (SQLException ex) ...
        } else ...
    }
    // 如果代码走到这里那肯定是出问题了，要是一个能连接的驱动都没找到，直接报错
    if (reason != null)    {
        println("getConnection failed: " + reason);
        throw reason;
    }
		...
}
```

我们看到实际上在源代码中，有很多地方都会打印日志，为什么到使用的时候就没有了呢：

```java
public static void println(String message) {
    synchronized (logSync) {
        if (logWriter != null) {  //注意这里需要logWriter不为null才能打印
            logWriter.println(message);
          	...
        }
    }
}
```

所以，如果需要打印日志的话，我们给它设置一个logWriter即可：

```java
DriverManager.setLogWriter(new PrintWriter(System.out));
```

这样我们就可以在控制台看到日志打印信息了：

![QQ_1722271131107](https://oss.itbaima.cn/internal/markdown/2024/07/30/Wq3PJAHTip1XCys.png)

下一部分我们接着来介绍Connection和Statement。

## 了解Connection与Statement

Connection是数据库的连接对象，它执行SQL语句并在连接上下文中返回结果。

Connection对象也包含数据库相关的一些信息，当我们连接成功后，可以通过getMetaData来获取数据库信息对象：

```java
DatabaseMetaData meta = connection.getMetaData();
System.out.println("数据库名称： " + meta.getDatabaseProductName());
System.out.println("数据库版本： " + meta.getDatabaseMajorVersion() + "." + meta.getDatabaseMinorVersion());
System.out.println("当前用户: " + meta.getUserName());
System.out.println("数据库驱动： " + meta.getDriverName());
System.out.println("数据库驱动版本： " + meta.getDriverMajorVersion() + "." + meta.getDriverMinorVersion());
System.out.println("数据库驱动 " + meta.getCatalogTerm());
```

我们也可以使用Connection对象获取一些连接上的信息，比如：

```java
System.out.println("当前选择的数据库，+connection.getCatalog());
```

```java
System.out.println("数据库超时时间："+connection.getNetworkTimeout()+"ms");
```

```java
//不支持=0
//读未提交=1
//读已提交=2
//可重复读=4
//序列化=8
System.out.println("事务隔离级别，+connection.getTransactionIsolantion());
```

我们来看statement对象，它是执行SQL语句的关键，它用于执行静态SQL语句并返回其生成结果的对象。

```java
ResultSet set=statement.executeQuery("select * from student");
```

我们可以看到，executeQuery是查询表中的所有数据，除此之外，还有其他方法，我们在下面一一学习。

## 执行DQL和DML操作

还记得我们在数据库基础中学到的DQL与DML吗？它是我们用于向数据库中增删改查数据的操作，包括SELECT,UPDATE,INSERT,DELETE，我们先从SELECT开始。

前面我们学习了Statement，其中的executeQuery是用于执行SELECT查询语句的，我们先来看看它的定义：

```java
//执行给定的 SQL 语句，该语句返回单个 ResultSet 对象。
ResultSet executeQuery(String sql) throws SQLException;
```

在这里会返回一个ResultSet对象作为结果，他表示一个数据库结果集的数据表，通常通过执行查询数据库语句来生成。

使用起来也很简单，类似于迭代器：

```java
//一开始的位置在第0行
set.next();
```

```java
set.next();
System.out.println(set.getString("name"));
```

注意：如果使用序列号堆区数据，列的下表是从1开始的。

但是但是但是，如果我们在使用了statement.executeQuery()得到ResultSet后，再次执行一次查询，那么之前得到的ResultSet在读取时会出现错误。

> 默认情况下，每个Statement对象只能同时打开一个ResultSet对象。因此，如果一个ResultSet对象的读取与另一个对象的读取交错，则每个对象都必须有不同的Statement对象生成。如果存在打开的语句的当前对象，则Statement接口中的所有执行方法都会隐式关闭语句的当前ResultSet对象。

```java
ResultSet set1=statement.executeQuery("select * from student order by id desc");
ResultSet set2=statement.executeQuery("select * from student order by id desc");
set1.next();
System.out.println(set1.getString("name"));
```

![QQ_1722334285876](https://oss.itbaima.cn/internal/markdown/2024/07/30/H6iY7jUywJt3mWd.png)

我们接下来来看看DML操作，Statement为我们提供了executeUpdate方法：

```java
int executeUpdate(String sql) throws SQLException;

//当返回的行计数可能超过 Integer. MAX_VALUE时，应使用此方法。
long executeLargeUpdate(String sql) throws SQLException
```

这里的返回结果是一个int类型值，他代表：

1. SQL数据库操作语言（DML）语句执行生效的行计数。
2. 不返回任何内容的SQL语句，结果是0.

我们从insert语句开始，看看如何使用的：

```java
int i=statement.executeUpdate("insert into student(name,age) values ('小明',18)");
System.out.println("生效行数，+i);
```

![QQ_1722335370807](https://oss.itbaima.cn/internal/markdown/2024/07/30/jN571UbaGpmzoBR.png)

当然，还有一个普通的execute方法：

```java
// 执行给定的 SQL 语句，该语句可能会返回多个结果。
boolean execute(String sql) throws SQLException;
```

注意：这个方法的返回结果是一个布尔类型的结果：

- 如果结果是ResultSet对象（SELECT语句，SQL），返回true。
- 如果它是更新技术或者没有结果（DML），返回false。

也就是说，该方法一般用于我们不确定传入的SQL语句是DQL还是DML时才会被使用。

```java
boolean result=statement.execute("select * from student");
System.out.println(result ?"存在结果集:"不存在结果集");
```

如果我们执行的是一个DQL语句，就会得到结果集，结果集可以通过getResultSet方法获取：

```java
statement.execute("select * from student");
ResultSet rs=statement.getResultSet();
while(rs.next()){
    System.out.println(rs.getString("name"));
}
```

如果我们执行的是一个DML语句，那么这里会返回false，更新生效的行数可以通过getUpdateCount方法来获取：

```java
statement.execute("update student set name='小明' where sid = 1");
```

## 批处理操作

我们接下来看看批处理操作，当我们要执行多条语句时，现有的知识会使我们一个一个提交：

```java
List<String>ss=List.of("小刚","小强","小王","小花","小张");
//使用for循环来一个个执行insert语句
for(String s:ss){
    statement.executeUpdate("insert into student values('"+s+"',18)");
    
}
```

虽然这样符合逻辑，但是这样其实是每次执行一次插入，而不是一次性全部插入，会产生额外的的开销，那么该如何一口气全部交给数据库处理呢，我们可以对SQL语句进行优化：

```SQL
INSERT INTO student(name,age)VALUES
('小刚',18),
('小强',18),
('小花',18),
('小王',18),
('小张',18);
```

但是，有时候很难实现对SQL语句的优化，此时，我们可以使用批处理来完成：

```java
List<String>ss=List.of("小刚","小强","小王","小花","小张");
for(String s:ss){
    //使用addBatch将一个SQL语句添加到批处理列表中
    statement.addBatch("insert into student values ('" + s +"',18)");
}
int[] results=statement.executeBatch();  //统一执行批处理
System.out.println(Arrays.toString(results));
```

我们可以使用addBatch方法将任务添加到批处理队列中，所有任务添加完成后，再使用executeBatch进行一次性的批处理操作。

并且这里会返回一个int数组表每一个操作受影响的行数。

## 将查询结果映射为对象

现在，我们可以从数据库中查询数据了，但是，我们查询到的数据是零零散散的，那么，有什么方法可以集中管理这些数据呢？其实我们不难发现，每一个表中的一条记录，正好对应了java中每一个对象：

```
1 小明 18
```

```java
public class student{
    private int sid;
    private String name;
    private int age;
}
```

因此，为了方便，我们在查询到数据之后，一般会将每条记录都创建为一个对应的实体类对象。

接着，我们来完善一下：

```java
public class student{
    ...
    public student(int sid,String name,int age){
        this.sid=sid;
        this.name=name;
        this.age=age;
    }
    public void say(){
        System.out.println(name + age + sid);
    }
}
```

接下来，我们现在就可以在查询数据时直接转换为我们的实体类对象了：

```java
while(rs.next()){
    student ss=new student(rs.getInt("id")),
    rs.getString("name"),
    rs.getInt("age");
    ss.say();
}
```

只不过，普通的类型对于我们操作不太方便，比如我们想要获取对象的一些数据，还需要额外编写对应的geter方法，为了方便，我们可以使用新增的记录类型来编写，这是专门用于数据表示的特殊类型，它在编译时自带了我们实体类封装所需要的getter方法，以及对应的比较方法重写：

```java
public record Student(int sid,String name,int age){
    public void say(){
        System.out.println(name + age+ sid);
    }
}
```

## 实现登陆与SQL注入攻击

在生活中，很多网站都支持用户名和密码登录，这也是一种安全机制，防止别人非法访问我们自己的账户。

通过一个密码验证，就可以很好地解决这个问题，在进行操作之前，需要账号密码登录。

实际上想要设计一个这样的系统也很简单，同样是设计一张用户表，只不过这次我们需要带上用户自己设定的密码，并且用户的名字或是ID必须是唯一的，否则无法区分：

![QQ_1722413094272](https://oss.itbaima.cn/internal/markdown/2024/07/31/IbmOj4HJUsytQfa.png)

接着，我们设计一个对应的实体类：

```java
public record Account(int id,String name,String password){
    public boolean verifyPassword(String password){
        return this.password.equals(password);
    }
}
```

接着我们就可以从控制台接受数据并校检了：

```java
try(Connection connection=DriverManager.getConnection("jdbc:mysql://localhost:3306/study","root","123456");
   Statement statement=connection.createStatement();
   Scanner sc=new Scanner(System.in)){
    System.out.println("请输入用户名，);
    String username=sc.nextLine();
    System.out.println("请输入密码：");
    String password=sc.nextLine();
    ResultSet rs=statement.executeQuery("select * from account where name = '" + username +"'and password = '" + password + "'");
    if(rs.next()){
        Account acc=new Account(rs.getInt(1),rs.getString(2),rs.getInt(3));
        System.out.println(account + "登录成功");
    }else{
        System.out.println("用户名和密码错误");
    }
}catch(SQLException e){
    e.printTrackTrace();
}

```

这样，我们就实现了一个基本的用户名密码登录系统了。

但是，仍然有一些不正常的问题：

```sh
请输入用户名: test
请输入密码：1111' or 1=1; -- 
```

此时，我们会发现，结果登录成功了，现在我们带入查看一下：

```sql
select * from account where name = 'test' and password = '1111' or 1=1; --;'
```

所有最终执行的SQL变成了这样：

```sql
select * from account where name = 'test' and password = '1111' or 1=1;
```

因此，这样对我们的SQL语句结构遭到了破坏，现在让我们想想怎么解决这种问题。

## PreparedStatement

我们发现，如果单纯的使用Statement来执行SQL命令，会存在严重的SQL注入攻击漏洞！而这种问题，我们使用PreparedStatement来操作：

> PreparedStatement在执行之前会被预编译，因此如果同样的SQL查询多次执行，性能会更好。数据库只需要编译一次，而不是每次都编译，并且PreparedStatement使用参数化查询，自动对输入进行转义，从而有效防止SQL注入攻击。

我们还是以之前的用户登录为例，这次，我们换成更加安全的PreparedStatement来操作：

```java
PreparedStatement ps=connection.preparedStatement("select * from account where name = ? and password = ?")
```

我们需要提前给到PreparedStatement一个SQL语句，并且使用`?`作为占位符，他会预编译一个SQL语句，通过直接将我们的内容进行替换的方式来填写数据。

现在，我们修改一下之前的写法：

```java
try(Connection connection=DriverManager.getConnection("jdbc:mysql://localhost:3306/study","root","123456");
   PreparedStatement ps=connection.preparedStatement("select * from account where name = ? and password = ?")
   Scanner sc=new Scanner(System.in)){
    System.out.println("请输入用户名，);
    ps.setString(1,sc.nextLine());  //我们需要手动条件set方法填入参数到对应的位置中
    System.out.println("请输入密码：");
    ps.setString(2.sc.nextLine());
    ResultSet rs=statement.executeQuery();
    if(rs.next()){
        Account acc=new Account(rs.getInt(1),rs.getString(2),rs.getInt(3));
        System.out.println(account + "登录成功");
    }else{
        System.out.println("用户名和密码错误");
    }
}catch(SQLException e){
    e.printTrackTrace();
}

```

执行之前的SQL注入攻击案例，此时我们会发现无法破解，我们来看看实际执行的SQL语句是什么，这里直接打印Statement对象。

```java
System.out.println(statement);
```

实际执行的SQL语句如下：

```sql
select * from account where name = 'test' and password = '1111\' or 1=1; --'
```

此时我们发现，我们输入的恶意内容中单引号被转义了，也就是说它现在仅仅代表的是单引号这个字符，而真正用作囊括内容的是后面的那个单引号，也就是PreparedStatement自动将可能会产生歧义的地方进行了处理，保证了我们输入的内容是什么，那么这里填入的一定是什么。这样就可以防止语义被改变，从根源上解决SQL注入攻击。

## 事务操作

还记得我们在数据库基础中学习到的事务操作吗：

JDBC默认的事务处理行为是自动提交，所以前面我们执行一个SQL语句就会被自动提交（相当于没有启动事务），因此，需要使JDBC进行事务管理时，首先通过Connection对象调用setAutoCommit(false)方法，将SQL语句的提交由驱动程序转交给应用程序负责。

```java
connection.setAutoCommit(false);
```

一旦关闭自动提交，那么现在执行的所有操作如果在最后不进行commit()的话，所有的操作都会丢失，只有提交之后，所有的操作才会保存：

```java
connection.setAutoCommit(false);
statement.executeUpdate("insert into user (name, age) values ('小强', 18)");
```

![QQ_1722421744878](https://oss.itbaima.cn/internal/markdown/2024/07/31/QOxKItqvPiM5C7L.png)



我们尝试在最后进行一次`commit()`操作即可正常保存：

```java
connection.setAutoCommit(false);
statement.executeUpdate("insert into user (name, age) values ('小强', 18)");
connection.commit();
```

和命令行一样，在同一个连接下，如果我们不提交的情况下使用查询，确实可以查到我们之前插入的数据，但是实际上它并不在数据库中：

```java
connection.setAutoCommit(false);
statement.executeUpdate("insert into user (name, age) values ('小强', 18)");
ResultSet rs = statement.executeQuery("select * from user");
while (rs.next()) System.out.println(rs.getString("name"));
```

我们也可以使用`rollback()`来手动回滚之前的全部操作：

```java
connection.rollback();
```

比如：

```java
statement.executeUpdate("insert into user (name, age) values ('小赵', 18)");
statement.executeUpdate("insert into user (name, age) values ('小刘', 18)");
connection.rollback();
//只有这里的插入最终生效了，前面的被回滚了
statement.executeUpdate("insert into user (name, age) values ('小强', 18)");
connection.commit();
```

有时候为了操作更方便，我们还可以自由创建回滚点，快速回滚到我们想要回滚的位置上：

```java
connection.setAutoCommit(false);
statement.executeUpdate("insert into user (name, age) values ('小赵', 18)");
Savepoint savepoint = connection.setSavepoint();
statement.executeUpdate("insert into user (name, age) values ('小刘', 18)");
connection.rollback(savepoint);  //回滚到回滚点，撤销前面到回滚点部分的全部操作
statement.executeUpdate("insert into user (name, age) values ('小强', 18)");
connection.commit();
```

通过开启事务，我们就可以更加谨慎地进行一些操作了，如果我们想从事务模式切换为原有的自动提交模式，我们可以直接将其设置回去：

```java
connection.setAutoCommit(false);
statement.executeUpdate("insert into user (name, age) values ('小赵', 18)");
connection.setAutoCommit(true);  //重新开启自动提交，开启时把之前的事务模式下的未提交的内容给提交了
statement.executeUpdate("insert into user (name, age) values ('小刘', 18)"); 
//没有commit也成功了
```

有关事务相关操作，我们就暂时先介绍到这里。
