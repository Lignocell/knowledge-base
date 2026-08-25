## 背景

BI：译为 business intelligence，其实就是商业数据可视化报表的显示功能吧。### 传统 BI 平台（差异点）
https://chartcube.alipay.com/

1. 需要人工上传数据2. 需要人工筛选分析用到的行和列（需要专业知识）
3. 需要人工选择图表类型（同上）
4. 生成图标

### 智能 BI 平台（亮点）

- 用户只需要导入最原始数据，输入需要分析的目标（比如帮我生成一个人口增长趋势），让 AI 自己帮我们生成。
## 需求分析
1. 智能分析：让用户输入原始数据，自动生成图表和分析结论。2. 图标管理。3. 图标生成的异步化（消息队列）。4. 对接 AI 能力。
## 架构图
客户需求——输入数据，输入诉求——》业务后端（Spring Boot）————》AI（生成结果返回）
                                 |
                                 |
                                 |————》数据库（存储图标和数据）
多并发模式下，采用消息队列。
##  技术栈

### 前端（直接找源码）
1. React
2. Ant Design Pro+Umi
3. 可视化开发库（Echarts）4. umi openapi 代码生成

### 后端(重点)

1. Spring Boot
2. MySQL 数据库 3. Mybatis-Plus 数据访问框架
4. 消息队列（RabbitMQ）5. Open AI 接口开发：AI 接口
6. Excel 的上传和数据的解析（Easy Excel）7. Swagger + Knife4j 项目接口文档
8. Hutool 工具类
---
## 项目计划

### 1.0

前端项目初始化后代项目初始化前端开发- 快速开发登录功能- 图表分析页面开发- 图表管理页面开发后端开发- 库表设计
- 图标管理开发- 文件上传接口开发前后端业务流程跑通
#### 前端
直接找源码，配置 npm。
#### 后端

##### 库表设计

- 用户表```sql

create table if not exists user  
(  
    id           bigint auto_increment comment 'id' primary key,  
    userAccount  varchar(256)                 not null comment '账号',  
    userPassword varchar(512)                 not null comment '密码',  
    userName     varchar(256)                 null comment '用户昵称', 
     
    userAvatar   varchar(1024)                 null comment '用户头像',  
    userRole     varchar(256) default 'user'        not null comment '用户角色：user/admin',  
    
    createTime   datetime     default CURRENT_TIMESTAMP not null comment '创建时间',  
    
    updateTime   datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间', 
     
    isDelete     tinyint      default 0      not null comment '是否删除',  
    index idx_userAccount (userAccount)  
    
) comment '用户' collate = utf8mb4_unicode_ci;
```

- 图表 chart 
```sql
create table if not exists chart  
(  
    id           bigint auto_increment comment 'id' primary key, 
     
    goal         text   null comment '分析目标',
    
    chartData    text   null comment '图表数据',
    
    chartType    varchar(128)   null comment '图表类型',
    
    genChart     text   null comment '生成的图表数据,
    
    genResult   text   null comment '分析结论',
    
    userId        bigint null comment '创建用户id' ,
       
    createTime   datetime     default CURRENT_TIMESTAMP not null comment '创建时间',  
    
    updateTime   datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间', 
     
    isDelete     tinyint      default 0      not null comment '是否删除'
    
) comment '图表信息表' collate = utf8mb4_unicode_ci;
```

##### 具体代码

自动生成增删改查代码（MybaitsX~~这是个插件~~）##### Model 分类
- Entity：实体类，只能在数据库和 Mapper/Service 之间活动。由于数据库中有密码等敏感字段，不允许直接传输给前端。- DTO：Data Transfer Object，在前端到 Controller 上活动。专用与接收前端传递的信息,可以用于接收 checkPassword（数据库中没定义）。- VO：View Object，Controller 层传给前端。用于密码脱敏，二次包装（性别数据库为 1，而展现出来的是男）。- **流程**：前端—DTO—Entity—VO—前端。
### 2.0

#### 智能分析业务开发
##### 业务流程

1. 用户输入
   a.分析目标
   b.上传原始数据（Excel）   c.更精确的去控制图表类型，比如图表类型，图表名称。2. 后端过滤
   a.校验用户的输入是否合法   b.成本控制（次数统计）
3. 把处理后的数据输入给 AI 接口，让 AI 模型提供图表信息和结论文本。4. 把结果发送给前端。
##### 开发接口
根据用户输入的文本和文件，返回图表信息和结论文本。
**原始数据压缩**
由于 AI 接口都会有输入字数限制，尽可能压缩数据。如何调用 AI 提词（prompt）。
或者使用 CSV 来对 Excel 文件进行手动压缩。
使用 easyexcel 库（开源）来读取文件：https://easyexcel.opensource.alibaba.com/

##### 调用 AI

输入，系统预设（所谓的 AI 的身份，它是一个数据分析师）+ 目标 + 压缩后的数据。
一般而言，在系统方面做预设比直接拼接的效果要好。
### 3.0

#### 智能分析业务流程

#### 利用 AI 生成文本和图表
##### 生成图表

AI 无法生成现成的图表，但是可以生成代码，代码利用前端的可视化组件库（Echarts）在网页进行展示。
**AI 提问技巧*
1）使用系统预设（全局设置），比如：
```txt
你是一个数据分析师和前端开发专家，接下来我尝试按照以下固定格式为你提供内容，分析需求：
{数据分析的需求和目标}
原始数据，{csv 格式的原始数据，逗号作为分隔符}
请根据以上内容，按照以下指定格式生成内容（此外不要输出任何多余的开头、结尾、注释）、[[[[[[
(前端 Echarts V6 的 option 配置对象 js 代码，合理地将数据进行可视化，不要生成任何多余的内容，比如注释
[[[[[[
【明确的数据库分析结论，越详细越好，不要生成多余的注释】```

2）控制输出格式（便于 AI 输出的内容更加的规范化）

生成的内容：
```js
【【【【】{
 title: {
 text: '网站用户增长情况',
 subtext: ''
 },
tooltip: {
 trigger: 'axis',
 axisPointer: {
 type: 'shadow'
 }
 },
 legend: {
 data: ['用户']
 },
 xAxis: {
 data: ['1月', '2月', '3月']
 },
 yAxis: {},
 series: [{
 name: '用户',
 type: 'bar',
 data: [10, 20, 30]
 }]
}
【【【【】根据数据分析可得，该网站用户数量逐日增长，时间越长，用户数量增长越多】
```

3）指定一个示例问答。（或者说给 AI 提供一个例子）

#### 3 种调用 AI 的方式
1. 直接调用 OpenAI 或者其他 AI 原始大模型管网的接口。   优点：不经封装，最灵活，最原始
   缺点：要钱、要魔法。
本质上 OpenAI 就是提供 HTTP 接口，我们可以用任何方法去使用。

2. 使用云服务商提供的封装后的 AI 接口。   优点：不用魔法。   缺点：要钱，比直接调用原始方式更贵。
### 4.0

1. 完善图表管理功能。   - 查看所有图表历史记录（分页查看）(仅管理员或本人
2. 完善系统功能。   - 防止并发。
#### 系统优化

现在的系统安全吗：
- 如果用户上传一个超大的文件怎么办？
- 如果用户疯狂点提交？
- 如果 AI 生成太慢，又有很多用户同时生成，给系统造成压力，怎么提高用户体验：
1. 如果用户上传一个超大的文件怎么办？比如 1000 G：   
   只要涉及到用户上传的操作，一定要校验文件（头像）。   - 文件的大小。   - 文件的后缀。   - 文件的内容（成本要高）。   - 文件的合规性（懂得都懂，建议用第三方的审核功能，比如腾讯云的图片万象数据审核）。
#### 数据存储

问题，1. 如果用户的图表数据很大，全部存储在数据库的字段中，随着时间的推移，数据量日益提高，查询效率是会变慢的。2. 如果用户需要单独将历史图表中的某一图表的原始数据提取出来，我们该怎么办。
解决问题：（分库分表思路）	把每个图表对应的原始数据单独提取，拿到另一个表中，而不是都存储在一个字段里。（非聚簇索引？）（就是创建一个子数据库）
	
	Mybatis的动态SQL：根据代码灵活的动态生成
```sql
select * from chart_(2048321220819345409)
```

优点，1. 存储时分开存储，互不影响。2. 查询时使用 sql 语句灵活取出需要的数据，查询性能更快。
#### 限流

现在的问题：使用系统是需要消耗成本的，所以用户有可能疯狂刷量。解决问题，1. 限制用户总次数。2. 用户在短时间内，疯狂使用，导致服务器资源被占满。   限制单个用户在每秒使用一次。思考阈值是多少？参考正常用户的使用。
##### 限流的实现
1. 本地限流（单机限流）
   每个服务器单独限流，一般适用于单体式项目，就是项目只有一台服务器。   Guava RataLimiter：谷歌的限流 API。2. 分布式限流（多机限流）   如果项目有多个服务器，比如微服务，那么建议分布式限流。   把统计用户的使用频率数据放到一个集中的存储进行统计，比如 Redis（Redisson-一个操作 Redis 的工具库，内置一个限流数据工具类）。
##### 限流算法
1. 固定窗口限流
2. 滑动窗口限流
3. 漏桶限流
4. 令牌桶限流
##### 限流粒度
1. 针对某个方法进行限流。2. 针对某个用户限流。3. 针对某个用户 x 方法限流，比如单个用户单位时间内最多执行 XX 次这个方法。
### 5.0

1. 系统问题分析
2. 系统优化-异步化 3. 线程池4. 前后端的异步化改造
#### 系统问题分析

**问题场景，* 调用服务能力有限，或者时间较长时，要考虑**异步化*了。- 用户等待时间有点长（等待 AI 生成）- 业务服务器可能会有很多请求处理，导致系统资源紧张，更甚至服务器宕机，无法处理新的请求。- AI 能力是有限的，比如个模型3 s 只能处理 1 个请求，会导致 AI 对后台系统拒绝服务。
#### 异步骤
同步：一件事做完再做下一件事。异步：不用等第一件事做完，就可以做另一件事，等第一件事处理完成后，会收到通知，再进行后续处理。
#### 业务流程分析：
标准异步化的业务流程

1. 用户进行耗时很长的操作时，点击提交后，不需要在界面傻等，而是把这个任务保存到数据库中记录下来。2. 执行新任务时，	a. 任务提交成功
	    i. 如果程序中有多余线程，可以立刻去做。	    ii. 如果都在繁忙，那么继续放在等待队列里。	b.  任务提交失败
		i. 拒接这个任务，不去执行。		ii. 通过保存在数据库的记录来看到提交的任务，并且在程序闲的时候，可以从数据库中放回程序里继续执行。3. 程序（线程）从任务队列中提取任务依次执行，每完成一件事情，更改状态。4. 用户可以查询任务的执行状态，或者在任务执行成功或失败时得到通知（发邮件、系统消息提醒、短信等等）、5. 如果非常复杂，我们可以拆分成几个小任务，每完成一个小任务更新一次状态。
应用层
1. 用户点击智能分析页提交时，=先把图表保存在数据库=。2. 用户可以在图表管理页面，查看所有图表（包括已生成的，生成中的，生成失败的）信息和状态。3. 用户可以修改生成失败的图表信息，点击重新生成。
问题，1. 任务队列最大容量多少？
2. 程序如何从任务队列中取出任务去执行？这个流程如何实现，怎么保证程序最多同时执行多个任务？

#### 线程池
为什么需要线程池，- 线程的管理比较复杂（比如什么时候新增线程，什么时候减少空闲线程）。- 任务存取比较复杂（什么时候接受任务，什么时候拒绝任务，如何保证多个线程之间不争抢同一任务）。作用：帮助轻松管理线程，协调任务的执行过程。
##### 实现线程池
Spirng：ThreadPoolTaskExecutor 配合@Async 注解来实现。（不建议）
Java：使用 JUC 并发编程包中的 ThreadPoolExecutor 来实现灵活的线程池。
**线程池参数*

```Java
public ThreadPoolExecutor(int corePoolSize,  
                          int maximumPoolSize,  
                          long keepAliveTime,  
                          TimeUnit unit,  
                          BlockingQueue<Runnable> workQueue,  
                          ThreadFactory threadFactory,  
                          RejectedExecutionHandler handler)
```

`corePoolSize`：核心线程数，类比为正式员工数，正常情况下，我们系统应该能同时工作的线程池处于随时就绪的状态。`maximumPoolSize`：最大线程数，类比为最多招募的人数（核心外包），极限情况下，线程池最多有多少个线程。（设置为极限情况）
`keepAliveTime`：空闲线程存活时间，类比为临时工干完活后大概过多久开掉，非核心线程在多久没任务时删除。`TimeUnit`：空闲线程存活时间单位。` BlockingQueue<Runnable> workQueue`：任务队列，用于存放线程需要执行的队伍。可以看成排队人数，当排队人数满时才会调用外包（一定要设置）`ThreadFactoy`：控制每个线程的生成，线程的属性。`RejectedExecutionHandler`：拒绝策略，当任务队列满了，我们需要采取什么措施。

如何确定线程池参数？结合业务场景和实际情况来判断，不断优化。
要考虑系统最脆弱的地方在哪里（木桶效应）。现有条件：比如 AI 生成能力的并发只允许 4 个线程同时执行，AI 能力允许 20 个任务排队。
一般情况下，任务分为 IO 密集型和计算密集型。计算密集型：占用 CPU，比如音视频处理，图像处理，数学计算等，一般设置为 corePoolSize 等于 CPU 的核心数+1 。IO 密集型：吃带宽、内存/硬盘的读写资源。corePoolSize 可以设置大一点，一般情况下为 2n+1 

#### 实际开发流程
1. 在 chart 表添加任务状态字段（比如排队中、执行中、已完成、失败），任务执行信息字段（用于记录任务执行中、或者失败）。
```sql
ALTER TABLE 
chart ADD COLUMN status VARCHAR(128) NOT NULL DEFAULT 'wait' COMMENT '状态：可选值：wait、running、succeed、failed',     
ADD COLUMN execMessage TEXT NULL COMMENT '执行信息';
```

2. 用户点击提交时，先把图表保存到数据库中，然后提交任务。3. 任务：修改任务状态字段变为“执行中”，执行成功，修改为“完成”，保存执行结果；执行失败后，状态改为“失败”，记录失败信息。

### 优化策略
1. guava Retrying 重试。2. 如果任务根本没有提交到队列中（或者队列满了），是不是可以用定时任务把失败状态的图表存放到队列中（补偿）。3. 建议给任务的执行增加一个超时时间，超时自动标记为失败。
## 6.0

### 系统现状分析（单机系统）

已经经过了从同步到异步的改造，目前的异步是通过本地的线程池实现的。
- 无法集中限制，只能单机限制。
	解决方案：在一个集中的地方去管理下发任务（比如集中当前正在执行的任务数）  
- 任务由于是在内存中执行的，可能会丢失。  >  虽然可以人工从数据库中捞出来，但是其实是需要额外开发（比如定时任务），这种重试的场景是非常典型的，不需要我们开发者过于关心，或者自己去实现。
	解决方案：把任务放在一个可以持久化的硬盘上。
- 优化：如果系统功能越来越多，长耗时任务越来越多，系统会越来越复杂，比如要开多个线程池、资源可能会出现项目抢占)。其实我们可以把长耗时任务独立成一个程序，不影响主业务。  服务拆分（应用解耦）。
	解决方案：可以有一个中间人，让中间人来帮我们去链接两个系统（比如核心系统和智能生成业务）。


### 分布式消息队列
中间件连接多个系统，帮助多个系统紧密协作的技术（组件）。Redis、消息队列、分布式存储 Etcd。
#### 消息队列

存放消息的队列，先进先出。在多个不同的系统、应用之间实现消息的传输。
##### 消息队列的模式
生产者：Producer
消费者：Consumer
消息：Message
消息队列：Queue

生产者与消费者之间实现了解耦，互不影响。
#### 为什么要用消息队列：

1. 异步处理：生产者发完消息后可以去忙别的，消费者什么时候消费都可以，不会阻塞。2. 削峰填谷：先把应用的请求放到消息队列中，消费者（实际执行操作的应用）可以按照自己的需求慢慢去取。
#### 分布式消息队列的优势

1. 数据持久化：可以把消息集中存储到硬盘里。2. 可扩展性：可以根据需求随时增加和减少节点，随时保持稳定的服务。3. 应用解耦：可以连接各个不同语言、框架开发的系统，让这些系统能够灵活传输读取数据。4. 发布订阅

#### 应用场景

1. 耗时
2. 高并发场景3. 分布式系统协作（跨团队、跨业务协作）4. 请稳定性场景（金融）
#### 缺点：
要给系统引入额外的中间件，会更加复杂，额外维护中间件，额外的部署成本。消息队列：消息丢失、顺序性、重复消费、数据的一致性。（分布式系统就要考虑）
#### 主流的分布式消息队列选型 

ativemq、rabbitmq、kafka、rocketmq、zeromq、pulsar、Apache inLong（Tube）
#### Rabbitmq

特点：生态好、好学习、易于理解、时效性强、支持不同语言的客户端、拓展性、可用性高，适用于绝大多数中小型规模分布式系统。
## 知识点（问题）
### isNotBlank 与 isNotEmpty 辨析

- Blank 和 Empty 更加严格，Blank 会把空格也判为空。
### 直播辨析

- 线程池：并发（多个线程处理）
- 消息队列：适用于分布式下的信息传输，负载均衡（多线程模式下的任务分配），重启后数据和任务不会丢失。
### 为什么添加字段后不修改 Mapper/XML 也可以直接运行？

- MybatisPlus 使用了反射机制，自动将 sql 语句进行拼接。- 要求：当需要联表查询时才需要手动修改。
### 为什么要去继承 Serivalizable?

1. 授权 Java 将对象转化成字节流，转化后可以在网络中进行传输，或者持久化硬盘或者 Redis 中。2. 如果不实现此接口，会报错。3. 只要涉及到 Java 的字节流传输，就一定要加。（为了规范性，大部分情况都是要继承的）

### SerivalVersionUID 的意义
1. 相当于类的版本号，当被转换成二进制文件后，如果修改了字段，那么还原添加时，JVM 会进行比较，一致下会正常还原。2. 可以全部定义为 1L，JVM 在对比版本号时，采用【`包名 + 类名] + serialVersionUID` 】
### userAccount.intern()是什么方法
- synchronized 认的是 Java 内存中的对象地址。如果两人并发注册同一账号，前端传到后端的 String 对象在内存中的地址是不同的，会导致锁失效。intern() 强制去字符串常量池中寻找，只要字面量相同，就返回同一个物理内存地址，从而完美锁住并发。。- intern():会改变规则，转而去字符串常量池里寻找，如果账号一致，那么强制返回同一内存地址。
### QueryWrapper 是什么

- `queryWrapper.eq("userAccount", userAccount);`，它就会在底层自动帮你翻译成原生 SQL 语句， `WHERE userAccount = '你输入的账号'`

### BeanUtils.copyProperties(user, loginUserVO)原理

- 底层依然是反射机制。- 自动扫描二者的所有属性，如果二者存在相同的字段，那么自动复制，如果没有会自动忽略。- 缺点：只能浅拷贝；高并发下会产生损耗。- 替代方案：在追求极致性能的大型微服务中，推荐使用 MapStruct，它在编译期生成硬编码的 getter/setter，性能接近原生代码。
### `@Target(ElementType.METHOD)` 解释

- 规定该标签只能在方法上使用。
### `@Retention(RetentionPolicy.RUNTIME)` 解释

- 规定生存周期，RUNTIME 表示运行期。
### @RequestPart("file") MultipartFile multipartFile 意义

- 获取标签为 file 的文件，转化成字节流（就是 MultipartFile）。
### `@org.springdoc.core.annotations.ParameterObject`

- Knife4j 的架包，为了在测试文档中将字段进行拆分，方便测试。### `String suffix = FileUtil.getSuffix(originalName)`

- Hutool 工具类，获取文件拓展名。
### Redisson 基础用法

```Java
@Service
public class RedisLimiterManager {

    @Resource
    private RedissonClient redissonClient;

    /**
     * 区分不同的限流器
     */
    public void doRateLimit(String key) {
        RRateLimiter limiter = redissonClient.getRateLimiter(key); //限制用户（key）        //设定限制规则，        //RateType.OVERALL：表示所有服务器（范围）
        //2次请求        //1s内        //RateIntervalUnit.SECONDS：单位表示秒
        limiter.trySetRate(RateType.OVERALL, 2, 1, RateIntervalUnit.SECONDS);

        boolean canDo = limiter.tryAcquire(1); //获取一次令牌（请求）        if (!canDo) {
            throw new BusinessException(ErrorCode.TOO_MANY_REQUEST);
        }
    }
}

```
- 优势：传统的 Guava RateLimiter 只能做单机限流。而 Redisson 的 RRateLimiter 是基于 Redis 的，支持 OVERALL（分布式全局限流），完美适配集群部署。
### trim()含义

- 将字符串前面和后面的所有空格、换行符、制表符全部去掉、- 字符串中间的不会碰。
### genChart = genChart.replaceAll("\"\\s+xAxis\"", "\"xAxis\"")

- `"\`：表示双引号。- `\\s`：第一个`\` 表示转义字符，`\s` 代表任何空白字符
- `+`：表示一个或者无数个。所以整体表示 xAxis 的前后空格全部替换删除。
### RabbitConfig 配置

```Java
package com.example.bi_backend.config;

import com.example.bi_backend.constant.BiMqConstant;
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * RabbitMq配置类 */
@Configuration
public class RabbitMqConfig {

    /**
     *消费者队列配置     */
    @Bean
    public Queue queue() {
        //持久化，重启后任务不会丢失        return new Queue(BiMqConstant.BI_QUEUE_NAME, true);
    }

    /**
     * 交换机配置     * 在这里选择是直连（Direct），还是扇出（Fanout），还是主题（Topic）     */
    @Bean
    public DirectExchange exchange() {
        //1.持久化        //2.自动删除
        return new DirectExchange(BiMqConstant.BI_EXCHANGE_NAME, true, false);
    }

    /**
     * 连接
     */
    @Bean
    public Binding binding() {
        return BindingBuilder.bind(queue())
            .to(exchange())
            .with(BiMqConstant.BI_ROUTING_KEY);
    }
}

```

### ackMode = "MANUAL"什么含义- 将消费者收到消息后自动删除改为手动。防止断联或消息丢失

### `@SneakyThrows` 含义

- 将 try-catch 改为自动生成。
### `Channel` 是什么？

- Channel 是建立在 TCP 连接（Connection）内的虚拟轻量级信道。所有的消息收发（发数据）和指令控制（如 ACK 确认、NACK 拒收），全部必须通过 Channel 与 RabbitMQ 服务器进行交互。
### `channel.basicNack(tag, false, false);` 是干什么的？三个参数各是什么？

- 表示传输失败。- tag：表示传输失败的 id。- false：表示只拒收这一条错误，如果 true 则改完全部拒收。- false：表示将信息丢弃（或扔进死信队列）。
### Cors 配置类
```Java
@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        // 覆盖所有请求        registry
            .addMapping("/**")
            // 允许发送 Cookie                .allowCredentials(true)
            // 放行哪些域名（全部）
            .allowedOriginPatterns("*")
            //放行那些方法
            .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
            //允许前端添加请求头            .allowedHeaders("*")
            //允许后端暴露特殊标签给前端            .exposedHeaders("*");
    }
}

```

### @EqualsAndHashCode (callSuper = true)  

- 表示此注解下的类要比较所有信息包括他本身的类和所继承的父类。

### 异步/MQ 架构下的异常兜底策略（防僵尸数据）
1. 向线程池提交任务时，必须捕获 RejectedExecutionException，防止队列满时任务丢失，并在 catch 中将数据库状态更新为 failed。2. 使用 CompletableFuture 时，利用 .exceptionally(...) 捕获线程内部（如 AI 超时）抛出的运行时异常，进行业务补偿。
