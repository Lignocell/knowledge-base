# 🍃 决战 Spring 与 MyBatis

## 模块一：Spring 的两大灵魂（绝对的重点！）
### Q1：什么是 IOC？控制反转的核心思想和优势？⭐⭐⭐⭐⭐
- IOC即控制反转。- 核心是依赖对象管理从业务代码移动至框架容器，由本来的主动创建依赖转化为由对象声明，交由容器统一实现。- 优势是降低耦合度，提升可测试性，增强代码的可维护性。
### Q2：什么是依赖注入（DI）？⭐⭐⭐⭐⭐
- 依赖注入是控制反转原则的实现，由外部容器向对象提供依赖，而非对象内部主动实现。
#### Q2.1：@Autowired 和 @Resource 注解的区别？

- 共同点：二者均用于依赖注入。- 不同点：
  - @Autowired是spring框架提供，用于按类型进行匹配。  - @Resource是JSR-250规范，用于按名称进行匹配，如果找不到，才按照类型匹配。
### Q3：什么是 AOP？面向切面编程的核心概念和优势？⭐⭐⭐⭐⭐
- AOP是面向切面编程，是对面向对象编程的补充。- 他的核心是在多个模块中，提取通用的代码功能存放在独立的切面中。- 优势是降低耦合度，提高代码的灵活性。- 所以接口是插入功能，而AOP则是顺滑的附加功能。
#### Q3.1：AOP 和传统工具方法的具体区别，- 具体传统方法属于强侵入性的主动调用。- AOP 本质上是基于动态代理的被动拦截，实现零侵入解耦。### Q4：Spring AOP 的实现原理？JDK 动态代理和 CGLIB 代理的选择？（复习前面的知识！）⭐⭐⭐
- SpringAOP通过动态代理实现面向切面编程，在运行时AOP会扫描注解，将具体横向方法织入代码本身逻辑中。- 若目标类实现接口，那么使用JDK动态代理。JDK代理性能更好，有接口限制。- 若没有，默认使用CGLIB代理。CGLIB更通用，但是会增加类加载开销。- 在SpringBoot中，现在全部使用CGLIB代理。
------

## 模块二：Spring 核心机制与常用注解（项目实战题）

### Q5：Spring Bean 的生命周期？  （背关键点就可以）
1. 实例化：反射调用构造器实例化Bean对象。2. 属性注入：看到 `@Resource`，把依赖的其他 Bean 塞进这个空壳里（这就是 DI）。3. 初始前置处理：调用BeanPostProcessor的postProcessorBeforeInitialization方法，这里可以对bean进行定制化处理。4. 初始化阶段：如果Bean实现了InitializingBean接口会调用afterPropertiesSet方法，或是执行@PostConstruct注解，以及init-method执行的初始化方法。5. 初始化后置处理：调用BeanPostProcessor的postProcessorAfterInitialization方法，这里是AOP实现的位置。6. 容器关闭销毁：首先调用@preDestroy注解，然后如果实现了DisposableBean接口会调用destroy方法，最后执行destory-method指定的销毁方法。
### Q6：Spring Bean 的作用域？（重点区分 singleton 单例 和 prototype 多例）
- singleton，prototype，session，globalSession，request。- singleton：单例模式，默认作用域，只允许存在一个，启动时会创建并缓存，适合无状态组件。- prototype：多例模式，通过getBean()创建，不会被缓存，容器不负责销毁，适合有状态组件。
### Q7：@Component、@Service、@Controller ，@Repository的区别？⭐⭐⭐⭐

- 本质上都是用于将类标记为Spring容器管理的Bean。
- @Component：适用于标记无明确职责的基础组件。
- @Controller：标记前端响应层，负责处理HTTP的接收和请求。
- @Service：标记业务逻辑层，负责封装核心业务流程。
- @Repository：标记数据访问层，负责处理数据持久化操作。
#### Q7.1：@Controller 和 @RestController 的区别？

- 二者的主要区别在于响应值的处理方式不同。- @Controller：默认返回视图名称，Spring会通过ViewResolver将名称解析为视图模板（Thymeleaf），然后渲染成HTML返回给客户端。- @RestController：@Controller与@ResponseBody的结合版，将返回值直接序列化成JSON或者xml格式返回给客户端，跳过视图解析步骤。
------

## 模块三：Spring 事务机制（极高频，且极容易挖坑）

### Q8：Spring 事务管理的实现方式？@Transactional 的实现原理？⭐⭐⭐⭐

- 分为编程式事务与声明式事务。- 编程式事务：通过TransactionTemplate或者PlatformTransactionManager来显式管理事物的边界。- 声明式事务：通过@Transactional来声明，底层基于AOP实现对事务的自动操作。
### Q9：Spring 事务失效的常见场景？如何避免事务不生效？⭐⭐⭐⭐⭐（大厂最爱问的坑题）

1. 方法内部调用问题：当类内部存在两个不同的方法，A是普通方法，B是携带了事务的方法，当A在内部调用B时会绕过B的事务机制；因此，我们只需要在A上携带事务就可以解决。2. 异常处理不当：Spring默认只能处理RuntimeException和Error时进行回滚。其他异常使用：
  ```java
  // 加上这个参数，告诉 Spring：只要是 Exception 的所有异常，都会回滚，  @Transactional(rollbackFor = Exception.class)
  ```
3. 数据库引擎选择错误：只有InnoDB才能使用事务机制。4. 访问权限选择错误：只有public可以。5. 事务传播行为配置不当：被调用的方法配置了 `NOT_SUPPORTED`（挂起事务）等传播机制，导致脱离了当前事务。
## 模块四：MyBatis 基础扫盲（防身用）
### Q10：MyBatis 与 SQL 映射，{} 和 ${} 占位符的区别和安全性？⭐⭐⭐⭐⭐（必考：SQL 注入）
- #{}：该符号会进行预编译成`?`，当传入参数时，Mybatis会自动检测并进行类型转换，转换成字符串。- ${}：没有任何操作，传入参数时，直接将参数放入语句中。- 安全性：前者安全性更高，能有效防止sql恶意注入，篡改sql语句，实用性也更高。后者一般只在动态传入表名、列名等无法预编译的场景下使用
