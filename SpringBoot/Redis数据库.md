# Redis数据库
什么叫Redis数据库，我们不是已经学习了MySQL吗，为什么还有一个数据库：
在我们之前学习到的MySQL数据库中，它是一种传统的关系型数据库，在小型Web应用中，MySQL+Mybatis就已经能够适应绝大部分数据存储工作了；

但是但是但是，MySQL的数据是存储在硬盘上的，那么他的缺点就已经很明显了，那就是IO操作十分缓慢，只适合读，不适合写，如果涉及到快速更新的内容，比如双十一、微博热搜之类的话题，需要撑住成千上百万的短时多次查询，能撑住的只有内存。
因此，我们找到了一种替代方案，应对大数据时代的重要考验。
## Redis AI 总结

### MySQL 与Redis 的本质区别：【硬盘】VS 【内存】
假设你的系统是一家*新华书店**。
- **MySQL（硬盘数据库）*：    
    - **它是什么*：它是书店最深处那个极其庞大、极其沉重、装满了几十万本书的**巨型仓库（硬盘）**。    - **特点**：只要书存进去了，*就算停电、地震，书绝对不会丢（持久化极其安全）*。但是！如果有个客人来找一本书，店员要去那个几十万本书的仓库里慢慢翻，**速度极其慢（磁盘 I/O 慢）**。    - **在你项目里干嘛*：存你那些极其宝贵、绝对不能丢的数据。比如图表的名字、大模型算出来的图表 JSON 代码（`chartData`、`genChart`）、- **Redis（内存数据库 / 缓存）*：    
    - **它是什么*：它是书店大厅前台的一块*玻璃小书架（内存）*，    - **特点**：它就放在前台，客人一进门就能拿到书，**速度快到发指（基于内存，每秒能查 10 万次！）**。但是！它的容量很小（内存很贵），而且**一旦停电，玻璃书架上的东西可能会全部清空（默认易丢失）**。    - **所以它是干嘛的，*：它专门用来放那些*被极其频繁查询、且丢了也无所谓（或者能重新去大仓库拿）的数据*！这就叫**“缓存”*。
---

### 唤醒你的肌肉记忆：你在《智能BI》里是怎么用Redis 的？

你绝对没有忘，因为这些代码都是你一行一行敲出来的。你回想一下这三个场景：
#### 场景一：保存用户登录状态（Token 鉴权）
- **痛点**：用户点开每一个页面，后端都要验证“他是不是登录了”。如果你每次都去庞大的MySQL仓库里查密码，MySQL会直接累死。- **Redis 出手**：用户登录成功后，你生成了一个 `UUID Token`，然后用 `stringRedisTemplate.opsForValue().set("user:token", ...)`。你把他的身份牌放在前台的玻璃书架（Redis）上！以后用户每点一个页面，系统只去极速的 Redis 里看一眼，瞬间放行：
#### 场景二：令牌自动续签（expire）
- **痛点**：用户用着用着掉线了。- **Redis 出手**：每次用户访问，你不仅去 Redis 里查他，你还顺手写了一句 `stringRedisTemplate.expire(..., 30, MINUTE)`。只要他活着，你就把他在前台玻璃书架上的生存时间重新拉满 30 分钟。
#### 场景三：防刷限流器（Redisson）
- **痛点**：黑客1 秒钟点击1000 次生成图表按钮，大模型接口被刷爆。- **Redis 出手**：你在前台玻璃书架旁雇了一个叫 **Redisson** 的终极保安。保安手里拿着几个铁桶，规定1 秒内只发 2 个牌子”。因为Redis 速度极快，保安能在零点几毫秒内判定这个用户是不是在恶意刷单，如果是，当场一脚踹飞，根本不让这1000 次请求去麻烦大仓库（MySQL）。
---

### 💡 一句话总结

- **MySQL** 是用于*“保命保底”*的重型金库（存核心业务数据）。- **Redis** 是用于*“挡子弹和提速”*的极速外挂（存高频Token、做限流、抗高并发）。
## NoSQL理论

NoSQL全称：Not Only SQL，它是一种非关系型的数据库，相比于传统的SQL关系型数据库，它：
- 不保证ACID特性（事务）。- 不遵循SQL标准。- 消除数据之间的关联性。
然而，他的优势是
- 远超传统数据库的性能（重点）。- 非常易于可拓展。- 数据模型更加灵活。- 高可用。
这样，NoSQL的优势一下就出来了，这不就是我们正要寻找的高并发海量数据的解决方案吗：
NoSQL数据库分为以下几种：

- **键值存储数据库**：与HashMap类似，都是采用键值对的形式来存储。- **列存储数据库，* 这部分数据库通常是用来应对分布式存储的海量数据。键仍然存在，但是它们的特点是指向了多个列。- **文档型数据库，* 它是以一种特定的文档格式存储数据，比如JSON格式，在处理网页等复杂数据时，文档型数据库比传统键值数据库的查询效率更高。- **图形数据库：** 利用类似于图的数据结构存储数据，结合图相关算法实现高速访问。
其中我们要学习的Redis数据库，就是一个开源的**键值存储数据库**，所有的数据全部存放在内存中，它的性能大大高于磁盘IO，并且它也可以支持数据持久化，他还支持横向扩展、主从复制等。
实际生产中，我们一般会配合使用Redis和MySQL以发挥它们各自的优势，取长补短。
## Redis安装和部署
我们这里还是使用Windows安装Redis服务器，但是官方指定是安装到Linux服务器上，我们后面学习了Linux之后，再来安装到Linux服务器上。由于官方并没有提供Windows版本的安装包，我们需要另外寻找：

- 官网地址：[https://redis.io](https://redis.io/)
- GitHub Windows版本维护地址：https://github.com/tporadowski/redis/releases

## 基本操作

Redis是一个键值数据库，因此，可以像Map一样，通过键值对向Redis数据库中添加数据（操作起来类似于向一个HashMap中存放数据）。
在Redis中，数据库是个整数索引标识，而不是一个数据库名称。默认情况下，我们连接Redis数据库后默认0号数据库，共16个，如果想要扩容数据库可以在Redis默认配置文件下修改。
切换数据库：

```sql
select 序号;
```

### 数据操作

添加数据：
```sql
set key value
-- 一次多个 mset key value key value...
```

所有存入的数据使用字符串形式来保存：
键值具有一定的命名规范，以便我们快速定位：

```sql
set user:info:用户ID:name kyle
-- set添加
-- 模块:子模块ID:属性属性名
```

通过键值获取存入的值：

```sql
get key
```

支持数据的过期时间设定：

```sql
set key value ex 3
-- ex表示秒，表示3s后过期set key value px 3
-- px表示毫秒
```

当数据达到时间后，会被自动删除。
我们也可以为已经创建了字段但是没有设定过期时间的键设置过期时间：

```sql
expire key 3
```

查询过期时间剩余多少：
```sql
ttl key
-- 秒显示
pttl key
-- 毫秒显示
persist key
取消过期时间，转化为永久（返-1，过期返-2）```

删除数据：（支持批量删除）
```sql
del key...
```

查询数据库中的所有键位：

```sql
key *
```

查询某个键位是否存在：
```sql
exists key...
```

随机哪一个键：
```sql
randomkey
```

我们也可以将数据库的内容转移到另一个数据库：
```sql
move key 数据库序号```

修改key值名称：

```sql
rename 旧key 新key
-- 若新key存在，直接覆盖renamenx 旧key 新key
-- 安全改名
```

如果存放的是一个数字，我们可以进行数学运算：
```sql
incr key
-- key++
incrby key b
-- key=key+b
decr key
-- key--
```

最后是查看key的数据的类型

```sql
type key
```

Redis数据库也支持多种数据类型，但是它更偏向于我们在Java中认识的那些数据类型。
## 数据类型介绍

一个键值对除了存储String类型之外，当然还可以存储其他类型。
### Hash

这种类型本质上就是HashMap，`在Java中`就像这样：（Redis本身不支持嵌套）

```java
//Redies默认存储String类型类似于这样：
Map<String, String> hash = new HashMap<>();

//而默认存储的Map类型，Map<String, Map<String, String>> hash = new hashMap<>();

```

由于值本身又是一个Map，因此我们可以在此Map的基础上放入各种类的属性和值，以实现一个Hash存储一种类和一个类的数据。
我们可以像这样来添加一个Hash类型的数据：

```sql
hset key 字段 值..
```

我们可以直接获取：
```sql
hget key 字段
-- 当然也可以一次性获取所有 hgetall key
```

同样，我们也可以判断某个字段是否存在：
```sql
hexits key 字段
```

删除Hash中的某个字段：
```sql
hdel key
```

我们发现，在操作一个Hash时，实际上就是我们普通操作命令前面添加一个`h`，这样就能以同样的方式去操作Hash里面存放的键值对了，这里就不一一列出所有的操作了。我们来看看几个比较特殊的。
我们现在想知道Hash一共存了多少个键值对：
```sql
hlen key
```

我们也可以一次性获取所有字段的值：

```sql
hvals key
```

唯一需要注意的是，Hash中只能存放字符串值，不允许出现嵌套的的情况。
### List

我们接着来看List，实际上也可以猜到，他就是一个列表，支持随机访问和双端操作，就和LinkedList一样。
我们可以直接向一个存在（不存在会自动创建）的List插入数据：
```sql
-- 向列表头部添加元素 lpush key element
-- 向列表尾部添加元素 rpush key element
-- 在指定元素的前/后插入元素 linsert key before/after 指定元素 element
```

同样的，获取双元素特别简单：

```sql
-- 根据下标获取元素
lindex key 下标
-- 获取并移出头部元素 lpop key
-- 获取并移出尾部元素 rpop key
-- 获取指定范围内 lrange key 开始下标 结束下标
```

注意，如果不清楚具体多少位，可以选择-1，表示从头开始的所有元素：

```sql
lrange a 0 -1
```

这里，push和pop还可以连续使用。
```sql
rpoplpush 当前数组 目标数组
-- 从前一个数组的最后一位取出放入目标数组的第一位```

它还支持阻塞操作，等待列表中有数据后才进行删除，如果没有，可以自定义超时时间：
```sql
blpop key ... timeout
```

### Set和SortedSet

Set集合和Java中的HashSet一样，不允许出现重复元素，不支持随机访问，但是能利用Hash提高查找速率。
向Set中添加一个和多个值：

```sql
sadd key value...
```

查看Set集合中有多少个值：

```sql
scard key
```

判断集合中是否包含指定值：

```sql
sismember key value
```

列出所有值：

```sql
smembers key
```

集合之间的运算：

```sql
-- 集合之间的差集sdiff key1 key2
-- 集合之间的交集 sinter key1 key2
-- 并集
sunion key1 key2
-- 将集合之间的差集存在目标集合中sdiffstore 目标集合 key1 key2
-- 同上
sinterstore 目标集合 key1 key2
-- 同上
sunionstore 目标集合 key1 key2
```

移动集合的值到另一个集合中：
```sql
smove key 目标集合 value
```

移出目标的值：

```sql
-- 随机移出
spop key
-- 指定移出
srem key value...
```

那么如果我们要求值要按照我们指定的顺序进行排列该怎么办？这里用到了SortedSet，这个会为值设定一个分数，分数的大小决定值所在的位置：
```sql
zadd key value score
```

当然，我们也可以根据分数段来获取：
```sql
-- 通过分数段来查看
zrangebyscore key start stop
-- 统计分数段的数量
zcount key start stop
-- 根据分数获取指定值的排名
zrank ket value
```

其他语法自行了解：https://www.jianshu.com/p/32b9fe8c20e1

有关Bitmap、HyperLogLog和Geospatial等数据类型，这里暂时不做介绍，感兴趣可以自行了解。
## 持久化
我们都知道，Redis区别于MySQL的最重要的原因就是IO操作极快，数据是保存在内存上的， 那么就又引申出了一个新的问题，如果发生断电或者电脑故障，那么数据不会丢失吗。
这时我们就需要持久化，将数据备份到硬盘中，防止数据丢失。
持久化的形式有两种：

- 直接复制：将内存中的数据直接读取并保存在硬盘中，需要时直接复制回来。- 保存过程：这时我们像硬盘中保存的是将数据写入内存的流程，如果发生丢失，我们可以按流程重新演绎一遍。
### RDB

RDB就是我们所说的第一种方案，那么我们如何启动这个操作呢？命令如下：
```sql
save
-- 上面是直接保存，会占用一点时间，下面是单独开一个子进程来后台保存bgsave
```

执行后，服务器目录下会生成一个`dump.rdb`文件，而这个文件中就保存了内存中所有的数据，当服务器重启后，会自动加载里面的内容到对应的数据库中，保存后我们关闭服务器：
```sql
shutdown
```

重启后我们可以看到数据依旧存在。
虽然很方便，但是如果数据库中的数据量很大，那么我们进行保存时会消耗很长的时间，此时我们需要进行设定，每隔一段时间自动保存；

另一种情况，如果我们一直持续读操作，那么我们需要延缓数据库自动保存的次数。
我们在配置文件中设置参数，并设定在一段时间内写入多少数据时，执行一次保存操作：

```txt
save 300 10 # 300秒（5分钟）内有10个写操作save 60 10000 # 60秒（1分钟）内有10000个写操作```

配置的save使用时都是bgsave（后台执行）。
###  AOF

虽然RDB解决了持久化的问题，但是它依然拥有缺点：比如它每次保存都是完整的去保存数据库的内容，再比如后台保存时会产生额外的开销，当然，**最严重的是**，它不是实时保存的，如果发生错误，依然可能会有少量数据丢失。
而AOF就是另一种方案，以日志的形式将我们每次执行的命令都进行保存，服务器重启时会将命令依次执行，通过重演的方式进行数据恢复，这样就能很好的解决实时存储的问题。
但是，我们多久执行一次日志写入呢？当然这也是可以配置的：

- always：每次执行写操作。- everysec：每秒保存一次（默认配置），这样就算丢失数据也只会丢一秒以内的数据。- no：看系统心情保存。
可以在配置文件中配置：
```sql
# 注意这里也要改appendonly yes

# appendfsync always
appendfsync everysec
# appendfsync no
```

重启服务器后，我们可以看到目录下多了一个`appendonly.aof`文件，存储的就是我们执行的命令。
AOF也有缺点：每次启动服务器都要重新重演，更加耗时间，并且随着时间的推移，aof文件也会变得无比的巨大，我们同样需要改进。
Redis有一个AOF重写机制来进行优化，比如：
```sql
lput test 666
lput test 777
lput test 888
```

实际上用一条语句也可以实现：
```sql
lpush test 666 777 888
```

正是因此，只要我们语句达到的结果相同，那么怎么修改都可以，所有我们可以通过这样的方式对语句进行压缩。
我们可以输入命令来执行操作：

```sql
bgrewriteaof
```

或是在配置文件中配置重写：
```txt
# 百分比计算，这里不多介绍
auto-aof-rewrite-percentage 100
# 当达到这个大小时，触发自动重写auto-aof-rewrite-min-size 64mb
```

至此，我们就完成了两种方案的学习，我们来进行一下总结：
RDB：
- 优点：加载速度快，数据体积小。- 缺点：存储速度慢，会发生数据丢失。
AOF：
- 优点：存储速度快，支持实时存储。- 缺点：加载速度慢，数据体积大。
## 事务和锁机制

### 事务

和MySQL一样，在Redis中也有事务机制，当我们需要保证多条命令一次性完整执行而中途不受到其他命令干扰时，就可以使用事务机制。
我们可以使用命令来开启事务：

```sql
multi
```

开启后我们发现，它实际上是在整个事务中创建了一个命令队列，开启后的所有执行任务均被进行排列，只有当使用命令来执行事务时，所有任务才开始按顺序执行：
```sql
exec
```

我们也可以中途取消事务，那么之前所有的操作全部丢失：
```sql
discord
```

### 锁机制
与MySQL同理，当两个事务同时操作同一个数据时，这时会动用锁机制来保证事务的完整进行。
Redis与MySQL不同，Redis是乐观锁，MySQL是悲观锁（乐观锁与悲观锁详见八股文）

Redis会使用watch来监视数据，如果执行事务之前，watch监测到数据发生了修改，那么会立刻取消事务：
```sql
watch
```

我们可以开两个客户端进行测试。
取消监视可以使用：
```sql
unwatch
```

至此，Redis的基础内容就讲解完毕了。## 使用Java与Redis交互

上面我们学习了如何通过命令窗口操纵数据库，现在我们需要和Java进一步的结合，这里我们用到了Jedis框架，他能够实现Java与Redis数据库的交互，导入依赖：
```xml
<dependencies>
    <dependency>
        <groupId>redis.clients</groupId>
        <artifactId>jedis</artifactId>
        <version>4.0.0</version>
    </dependency>
</dependencies>
```

### 基本操作

我们先来看看如何链接到数据库，代码如下：
```java
	public static void main(String[] args){
	//创建Jedis对象
	Jedis jedis=new Jedis("localhost",6379);
	
		//使用之后关闭连接
		jedis.close();
}
```

通过Jedis对象，我们就可以直接通过命令调用Redis方法了：

```Java
	public static void main(String[] args){
		//直接使用try-with-resource，省去close
		try(Jedis jedis=new Jedis("localhost",6379)){
			jedis.set("test","kyle");  //等同于set test kyle
			System.out.println(jedis.get("test"));  //等同于get test命令
		}
	}
```

Hash数据的类型也是这样：

```java
public static void main(String[] args) {
    try(Jedis jedis = new Jedis("192.168.10.3", 6379)){
        jedis.hset("hhh", "name", "sxc");   //等同于 hset hhh name sxc
        jedis.hset("hhh", "sex", "19");    //等同于 hset hhh age 19
        jedis.hgetAll("hhh").forEach((k, v) -> System.out.println(k+": "+v));
    }
}
```

我们接着来看看列表操作：

```java
public static void main(String[] args) {
    try(Jedis jedis = new Jedis("192.168.10.3", 6379)){
        jedis.lpush("mylist", "111", "222", "333");  //等同于 lpush mylist 111 222 333 命令
        jedis.lrange("mylist", 0, -1)
                .forEach(System.out::println);    //等同于 lrange mylist 0 -1
    }
}
```

实际上我们只需要按照对应的操作去调用同名方法即可，所有的类型封装Jedis已经帮助我们完成了。
### SpringBoot整合Redis

我们接着来看看如何在SpringBoot中整合Redis框架，只需要一个starter即可，但是它的底层并没有用Jedis，而是Lettuce：
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

starter提供的默认配置会去连接本地的Redis服务器，并使用0号数据库，当然也可以手动修改，我们先配置文件：
```yaml
spring:
	redis:
	# Redis服务器地址
	host: 192.168.10.3
    #端口
    port: 3679
    #使用几号数据库    database: 0
```

starter已经为我们提供了两个对应的模版类：
```java
@Configuration(
    proxyBeanMethods = false
)
@ConditionalOnClass({RedisOperations.class})
@EnableConfigurationProperties({RedisProperties.class})
@Import({LettuceConnectionConfiguration.class, JedisConnectionConfiguration.class})
public class RedisAutoConfiguration {
    public RedisAutoConfiguration() {
    }

    @Bean
    @ConditionalOnMissingBean(
        name = {"redisTemplate"}
    )
    @ConditionalOnSingleCandidate(RedisConnectionFactory.class)
    public RedisTemplate<Object, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) {
        RedisTemplate<Object, Object> template = new RedisTemplate();
        template.setConnectionFactory(redisConnectionFactory);
        return template;
    }

    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnSingleCandidate(RedisConnectionFactory.class)
    public StringRedisTemplate stringRedisTemplate(RedisConnectionFactory redisConnectionFactory) {
        return new StringRedisTemplate(redisConnectionFactory);
    }
}
```

我们如何去使用呢？我们可以直接注入`StringRedisTemplate`来使用模板：

```java
@SpringBootTest
class SpringBootTestApplications{
    
    @Autwired
    StringRedisTemplate template;
    
    @Test
    void contextLoads(){
        ValueOperations<String,String>operations=template.opsForValue();
        operations.set("c", "xxxxx");   //设置值        System.out.println(operations.get("c"));   //获取值      	
        template.delete("c");    //删除键        System.out.println(template.hasKey("c"));   //判断是否包含键        
    }
}
```

实际上，所有的值的操作都被封装到了ValueOperations对象中，而普通的键操作可以直接通过模板对象来使用，大致方法与Redis一致。
我们接着来看看事务操作，由于String没有专门的Redis事务管理器，所以只能借用JDBC来使用，只不过无所谓，正常情况下反正我们也要用到这玩意：
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
</dependency>
```

```java
@Service
public class RedisService {

    @Resource
    StringRedisTemplate template;

    @PostConstruct
    public void init(){
        template.setEnableTransactionSupport(true);   //需要开启事务    }

    @Transactional    //需要添加此注解
    public void test(){
        template.multi();
        template.opsForValue().set("d", "xxxxx");
        template.exec();
    }
}
```

我们还可以为RedisTemplate对象配置一个Serializer来实现对象的JSON存储：
```java
@Test
void contextLoad2(){
   //注意Student需要实现序列化接口才能存入Redis
    template.opsForValue().set("student", new Student());
    System.out.println(template.opsForValue().get("student")); 
}
```

## Redis与分布式

现在，我们来探讨Redis在分布式状态下的应用场景。
### 主从复制

在分布式场景下，我们可以考虑让Redis实现主从模式：
![image-20230307000109568](https://oss.itbaima.cn/internal/markdown/2023/03/07/bzwPflgBD5O1saN.png)

主从复制，是指将一台Redis服务器的数据，复制到其他的Redis服务器。前者称为主节点（Master），后者称为从节点（Slave）。数据的复制是单向的，只能从主节点到从节点。前者负责写，后者负责读，实现读写分离。
好处显而易见：

- 实现读写分离，提高性能。- 在写少读多的场景下，我们可以安排大量从节点，这样能够大幅度的分担压力，并且就算挂掉一个，其他的也可以正常使用。
那么现在我们开启两台Redis服务器，修改二者的配置文件`redis.windows.conf`：
```conf
# Accept connections on the specified port, default is 6379 (IANA #815344).
# If port 0 is specified Redis will not listen on a TCP socket.
port 6001
```

一个服务器的端口设定为6001，复制一份，另一个的端口为6002，接着我们指定配置文件进行启动，打开cmd：
![image-20230307000143566](https://oss.itbaima.cn/internal/markdown/2023/03/07/Si54lok9eqtKPf1.png)

现在我们的两个服务器就启动成功了，接着我们可以使用命令查看当前服务器的主从状态，我们打开客户端：

![image-20230307000151282](https://oss.itbaima.cn/internal/markdown/2023/03/07/2TbMQeZknSOzFpy.png)

我们可以输入`info replication`命令来查看当前服务器的状态，可以看到，默认角色为：Master，也就是说所有服务器在启动时都是主节点，需要我们手动来指定（比如现在指定6002）从节点：
![image-20230307000200296](https://oss.itbaima.cn/internal/markdown/2023/03/07/XqpNcihJ5jsZRoI.png)

可以看到，在输入`replicaof 127.0.0.1 6001`命令后，就会让6001服务器作为主节点，而当前节点作为6001的从节点，并且角色也会变成：slave，接着我们来看6001的情况：

![image-20230307000208687](https://oss.itbaima.cn/internal/markdown/2023/03/07/YABKJDsbQkE1UM5.png)

可以看到从节点信息中已经出现6002服务器，也就是说现在我们6001和6002就形成了主从关系（还包含一个偏移量，这个偏移量反应的是从节点的同步情况）
> 主服务器和从服务器都会维护一个名叫偏移量的值，主服务器每传输n字节的值，偏移量就会加n；同理，从服务器每接收n字节的值，偏移量就会加n，通过两台服务器的偏移量大小可以来维护二者的数据是否一致，如果不一致，那么就需要进行增量同步了。
那么我们现在可以来测试一下，在主节点新增数据，看看是否会同步到从节点：
![image-20230307000216155](https://oss.itbaima.cn/internal/markdown/2023/03/07/taxoisA8Tpg2DWM.png)

可以看到，我们在6001服务器插入的`a`，可以在从节点6002读取到，那么，从节点新增的数据在主节点能得到吗？我们来测试一下：

![image-20230307000224291](https://oss.itbaima.cn/internal/markdown/2023/03/07/dS2V8xafPj6lKND.png)

可以看到，从节点压根就没办法进行数据插入，节点的模式为只读模式。那么如果我们现在不想让6002作为6001的从节点了呢：

![image-20230307000234718](https://oss.itbaima.cn/internal/markdown/2023/03/07/dV7Rxov6pblW2g5.png)

可以看到，通过输入`replicaof no one`，即可变回Master角色。接着我们再来启动一台6003服务器，流程是一样的：
![image-20230307000406674](https://oss.itbaima.cn/internal/markdown/2023/03/07/TC7z2mt3EGMPWfq.png)

可以看到，在连接之后，也会直接同步主节点的数据，因此无论是已经处于从节点状态还是刚刚启动完成的服务器，都会从主节点同步数据，实际上整个同步流程为：

1. 从节点执行replicaof ip port命令后，从节点会保存主节点相关的地址信息。2. 从节点通过每秒运行的定时任务发现配置了新的主节点后，会尝试与该节点建立网络连接，专门用于接收主节点发送的复制命令。3. 连接成功后，第一次会将主节点的数据进行全量复制，之后采用增量复制，持续将新来的写命令同步给从节点。
当我们的主节点关闭后，从节点依然可以读取数据：
![image-20230307000415001](https://oss.itbaima.cn/internal/markdown/2023/03/07/MmNshyQxa2ijSRT.png)

但是从节点会疯狂报错：
![image-20230307000424822](https://oss.itbaima.cn/internal/markdown/2023/03/07/pEIo93MQXShrsZD.png)

当然，每次去敲命令来配置主从实在是太麻烦了，因此我们也可以在配置文件中直接添加：

```
replicaof 127.0.0.1 6001
```

这里我们把6002和6003服务器都配置一下，现在我们重启三个服务器。
![image-20230307000432434](https://oss.itbaima.cn/internal/markdown/2023/03/07/GpAa5kfyC3zVRZK.png)

当然，除了作为Master的从节点之外，我们还可以将其作为从节点的从节点，比如我们现在让6003作为6002的从节点：
![image-20230307000444990](https://oss.itbaima.cn/internal/markdown/2023/03/07/OdAs1weYgkDrQvf.png)

也就是说，现在差不多是这样的的一个情况：

![image-20230307000459161](https://oss.itbaima.cn/internal/markdown/2023/03/07/2ADSR8LtpMhCFfK.png)

采用这种方式，优点肯定是显而易见的，但是缺点也很明显，整个传播链路一旦中途出现问题，那么就会导致后面的从节点无法及时同步。
### 哨兵模式

前面我们学习了关于主从复制的一些操作，下面我们来看看哨兵模式。
经过之前的学习，我们知道了最关键的还是主节点，一旦主节点发生错误，那么整个主从系统都将开始瘫痪，因此，我们需要想一个办法。
这里，我们就用到了哨兵：

![image-20230307000508084](https://oss.itbaima.cn/internal/markdown/2023/03/07/YGq8MDZbRK6E7Po.png)

哨兵用来对所有的节点进行监控，一旦发现主节点瘫痪，那么会立即对从节点进行投票，选出一个新的从节点作为主节点（注意要实现这样的功能最小的系统必须是一主一从，再小的话就没有意义了）
![image-20230307000516875](https://oss.itbaima.cn/internal/markdown/2023/03/07/WhkUqfxcHn4CApP.png)

接下来，我们修改配置文件来启动哨兵，这里我们复制出一个服务器，并将配置文件全部删除，后续会自动添加文件：

```
sentinel monitor kyle 127.0.0.1 6001 1
```

第三个字段是名称，随意，后面是主节点的相关信息，最后一位我们后边来看，然后我们启动服务器：
![image-20230307000534399](https://oss.itbaima.cn/internal/markdown/2023/03/07/xB78t53RgykXvo9.png)



![image-20230307000542878](https://oss.itbaima.cn/internal/markdown/2023/03/07/STh2RgjW7ycPCNB.png)



可以看到以哨兵模式启动后，会自动监控主节点，然后还会显示那些节点是作为从节点存在的。
现在我们把主节点直接关闭，看看发生什么：

![image-20230307000627807](https://oss.itbaima.cn/internal/markdown/2023/03/07/97HnwfuNjUK5qx4.png)

可以发现，从节点开始报错，一开始不会直接进行选举，而是会重连，但是一段时间以后，依然无法连接，此时哨兵输出了以下内容：
![image-20230307000646050](https://oss.itbaima.cn/internal/markdown/2023/03/07/GWt8Q6mfSv7TgCb.png)

可以看到进行了重新选举，003节点被选为了新的主节点，并且之前的主节点6001变成了新的主节点的从节点：
![image-20230307000653822](https://oss.itbaima.cn/internal/markdown/2023/03/07/4WzTVZ15dMiQ3f8.png)

 

![image-20230307000703587](https://oss.itbaima.cn/internal/markdown/2023/03/07/gGHVvOhBKe9wSEz.png)

当我们再次启动6001时，会发现，它自动变成了6003的从节点，并且会将数据同步过来：

![image-20230307000717002](https://oss.itbaima.cn/internal/markdown/2023/03/07/eqLycu8s1rSRtFa.png)

那么，这个选举规则是怎样的呢：
1. 首先会根据优先级进行选择，可以在配置文件中进行配置，添加`replica-priority`配置项（默认100），越小表示优先级越高。2. 如果优先级一样，那就选择偏移量最大的
3. 要是还选不出来，那就选择runid（启动时随机生成的）最小的。
要是哨兵挂了了怎么办，没关系，我们可以多启动几个哨兵，只需要把哨兵的配置复制一下，然后修改端口，这样就可以同时启动多个哨兵了，我们启动3个哨兵（一主二从三哨兵），这里我们吧最后一个值改为`2`：
```
sentinel monitor kyle 192.168.0.8 6001 2
```

这个值实际上代表的是当有几个哨兵认为主节点挂掉时，就判断主节点真的挂掉了。
那么，如何通过Java代码将哨兵模式下的主节点获取呢？我们需要配置依赖：

```xml
<dependencies>
    <dependency>
        <groupId>redis.clients</groupId>
        <artifactId>jedis</artifactId>
        <version>4.2.1</version>
    </dependency>
</dependencies>
```

```java
public class Main{
    public static void main(String[] args){
        try(JedisSentinePool pool=new JedisSentinePool("kyle",new HashSet<>(Arrays.asList("192.168.0.8:26741", "192.168.0.8:26740", "192.168.0.8:26739")))){  //IP地址不区分主从，第一个字段填写哨兵名称            Jedis jedis=pool.getResource();  //这就是Master节点
            jedis.set("test", "114514");    //直接写入即可，实际上就是向Master节点写入

            Jedis jedis2 = pool.getResource();   //再次获取
            System.out.println(jedis2.get("test"));   //读取操作
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}
```

这样，Jedis对象就可以通过哨兵来获取，当Master节点更新后，也能得到最新的。
### 集群搭建

如果我们的服务器不够用了，但是现在我们又需要继续存储，我们就可以使用集群来扩容。
由于单机的存储量就那么多，已经没办法拓展了，但是现在我们需要更多的内容，这时我们就可以让N 台机器的 Redis 来分别存储各个部分的数据，这样就实现了容量的横向扩展。同时，每台 Redis 还可以配一个从节点，这样就可以保证数据的安全性。
![image-20230307000754039](https://oss.itbaima.cn/internal/markdown/2023/03/07/TjCw8DLi1VqYvpZ.png)

那么，问题来了，如果用户来了一个写入的请求，该请求该传输到哪个节点呢？这里我们先研究一下Redis 的机制：

首先，Redis 集群包含 16384 个插槽，集群中的每个 Redis 各维护一部分插槽以及插槽所映射的键值数据，那么这个插槽是什么意思呢：
实际上，这个插槽其实就是键的 Hash 计算后的结果，注意，这里出现了CRC 循环冗余校验，这里采用CRC16，能得到 16 个bit位的数据，也就是说算出来的结果是 0-65535 之间，再进行取模，最后得到结果：

**Redis key 的路由计算公式：slot = CRC 16（key）% 16384**

结果的值是多少，就应该放到哪个对应的Redis 下面，比如，1号Redis 节点负责维护 0-25565 之间的插槽，当插入一个数据a=10，a 经过Hash 计算后的结果是666，那么a 就会存放在1号Redis 节点中；
简而言之，就是通过哈希计算来分配到各个 Redis 中。
那么现在，我们来搭建一个简单的集群，这里创建6 个配置，先开启集群模式：
```txt
# Normal Redis instances can't be part of a Redis Cluster; only nodes that are
# started as cluster nodes can. In order to start a Redis instance as a
# cluster node enable the cluster support uncommenting the following:
#
cluster-enabled yes
```

接着，记得把持久化文件全部删空，所有节点的内容全部为空。
然后输入 `redis-cli.exe --cluster create --cluster-replicas 1 127.0.0.1:6001 127.0.0.1:6002 127.0.0.1:6003 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003`，这里的 `--cluster-replicas 1` 指的是每个节点配一个从节点：
![image-20230307000805968](https://oss.itbaima.cn/internal/markdown/2023/03/07/7DikHoxKJPve9qa.png)

输入之后，会为你展示客户端默认分配的方案，并且会询问你是否合理，可以看到 6001。002。003全部被选择为主节点，我们直接输入yes即可：
![image-20230307000814076](https://oss.itbaima.cn/internal/markdown/2023/03/07/yxZhjouXB79qfDd.png)



最后分配成功，可以看到插槽的分配情况：

![image-20230307000830886](https://oss.itbaima.cn/internal/markdown/2023/03/07/8kg9TbadF2qyHJW.png)



现在我们随便连接一个节点，尝试插入一个值：

![image-20230307000840119](https://oss.itbaima.cn/internal/markdown/2023/03/07/YMf8DtlkCsqBpO1.png)



在插入时，出现了一个错误，实际上这就是因为a计算出来的哈希值（插槽），不归当前节点管，我们得去管这个插槽的节点执行，通过上面的分配情况，我们可以得到15495属于节点6003管理：
![image-20230307000849127](https://oss.itbaima.cn/internal/markdown/2023/03/07/EZmR2bLFudSskIf.png)



6003节点插入成功，当然我们也可以使用集群方式连接，这样我们无论在哪个节点都可以插入，只需要添加`-c`表示以集群模式访问：
![image-20230307000907196](https://oss.itbaima.cn/internal/markdown/2023/03/07/mVw7EXFJQOcinIb.png)



可以看到，在6001节点成功对a的值进行了更新，只不过还是被重定向到了6003节点进行插入。
我们可以输入`cluster nodes`命令来查看当前所有节点的信息：
![image-20230307000914746](https://oss.itbaima.cn/internal/markdown/2023/03/07/pEJdI2UWTcNZFqu.png)



那么现在如果我们让某一个主节点挂掉会怎么样？现在我们让6001挂掉：
![image-20230307000922277](https://oss.itbaima.cn/internal/markdown/2023/03/07/zd6L3WosVE8JUqf.png)



可以看到原本7001从节点6001，晋升为了新的主节点，而之前的6001已经挂了，现在我们将6001重启试试看：

![image-20230307000933812](https://oss.itbaima.cn/internal/markdown/2023/03/07/eUfYJS8yhVijvaw.png)



可以看到6001变成7001的从节点，那么要是7001和6001都挂了呢：
![image-20230307000944827](https://oss.itbaima.cn/internal/markdown/2023/03/07/9W2BQtMXrUCnySV.png)



这时我们尝试插入新的数据：
![image-20230307000953377](https://oss.itbaima.cn/internal/markdown/2023/03/07/S8r5TE7gJ3M6iDW.png)



可以看到，当存在节点不可用时，会无法插入新的数据，现在我们将6001和7001恢复：
![image-20230307001001435](https://oss.itbaima.cn/internal/markdown/2023/03/07/2RL4GNqSWJXFuME.png)

恢复后就又可以正常使用了。
最后我们来看看，如何使用 Java 链接到集群模式下的 Jedis，我们需要用到 JedisCluster 对象，```java
public class Main {

    public static void main(String[] args) {
        //和客户端一样，随便连一个就可以，也可以多连几个，构造方法有很多种选择
        try (
            JedisCluster cluster = new JedisCluster(
                new HostAndPort("192.168.0.8", 6003)
            )
        ) {
            System.out.println(
                "集群实例数量， + cluster.getClusterNodes().size()
            );
            cluster.set("a", "yyds");
            System.out.println(cluster.get("a"));
        }
    }
}

```
操作基本上和 Jedis 对象一样，这里就不多赘述了。
