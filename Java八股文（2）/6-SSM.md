# SSM：Spring、Spring MVC 与 MyBatis

> 目标：2027 年腾讯、阿里 Java 后端暑期实习；共 100 题，只列题目，不填写答案。
> 图标：👑 重点；⭐ 难点；👑⭐ 重难点。档位表示复习优先级，难点不一定优先做。

| 档位 | 定位 | 复习安排 | 题数 |
| --- | --- | --- | --- |
| S | 核心必做 | 第一轮完成，能独立讲清并应对追问 | 34 |
| A | 重点掌握，常见考察与延伸 | 第二轮完成，掌握概念、原理与应用 | 51 |
| B | 有概率考察，补充细节 | S、A 稳定后再补 | 14 |
| C | 特别偏，低优先 | 最后浏览，时间紧可暂缓 | 1 |

> 先跨模块完成 S，再做 A，最后补 B、C；同档先看 👑，带 ⭐ 的题预留更多理解时间。简历或项目涉及的技术，应提高其复习优先级。
> 划档是结合目标与时间预算作出的复习建议，不代表两家公司官方题频或 2027 年出题预测。相似题不合并；带“截图文字不全”的题仅录可见文字，不补写隐藏内容。
> 选题范围参考：[JavaGuide 面试专题](https://interview.javaguide.cn/home.html)。


## 模块一：IOC 与框架基础

### Q1：【S】什么是 IOC？控制反转的核心思想和优势？结合 Spring 框架聊聊 👑


### Q2：【S】什么是 Spring 框架？Spring 的核心特性和设计理念是什么？ 👑


### Q3：【A】使用 Spring 框架的优势？Spring 如何简化 Java 企业级开发？


### Q4：【S】Spring IOC 容器的实现原理？BeanFactory 的核心机制？ 👑⭐


### Q5：【B】Spring 的发展历程？Spring 4.x、5.x、6.x 版本的重要特性？


### Q6：【A】Spring 的配置方式有哪些？XML、注解、Java 配置的对比？


### Q7：【S】Spring 和 Spring Boot 的关系？Spring Boot 如何简化 Spring 开发？ 👑


### Q8：【A】Spring 框架包含哪些核心模块？各模块的作用和关系？


### Q9：【A】Spring 框架的整体架构设计？分层结构的优势？


### Q10：【A】Spring 中使用了哪些设计模式？如何体现这些模式？ 👑


------

## 模块二：依赖注入与常用注解

### Q11：【S】@Autowired、@Resource、@Inject 注解的区别？结合 Spring 框架聊聊 👑


### Q12：【A】@Autowired 和 @Resource 注解的区别？JSR-250 规范的支持？结合 Spring 框架聊聊


### Q13：【S】@Autowired 注解的工作原理？byType 和 byName 的装配策略？结合 Spring 框架聊聊 👑⭐


### Q14：【S】@Bean 和 @Component 的区别？方法级别 vs 类级别的 Bean 定义？结合 Spring 框架聊聊 👑


### Q15：【S】@Component、@Service、@Repository、@Controller 的区别？结合 Spring 框架聊聊 👑


### Q16：【A】@ComponentScan 注解的配置？包扫描的规则和过滤器？结合 Spring 框架聊聊


### Q17：【A】@Configuration 和 @Component 的区别？配置类的特殊性？结合 Spring 框架聊聊 👑


### Q18：【A】@Qualifier 注解的作用？如何解决多个候选 Bean 的问题？结合 Spring 框架聊聊


### Q19：【A】@Value 注解的使用？属性注入和 SpEL 表达式？结合 Spring 框架聊聊


### Q20：【S】什么是依赖注入？DI 的实现方式有哪些？结合 Spring 框架聊聊 👑


### Q21：【A】Spring 常用注解分类？配置注解、Bean 注解、依赖注入注解？


### Q22：【A】Spring 的属性注入？@Value 注解和 PropertyPlaceholder？


### Q23：【B】Spring 注解处理的底层原理？AnnotationMetadata 的解析？ ⭐【截图文字不全】【截图底部遮挡，末尾待核对】


------

## 模块三：Bean 生命周期与容器

### Q24：【A】@PostConstruct 和 @PreDestroy 的执行时机？生命周期回调？结合 Spring 框架聊聊 👑


### Q25：【A】@Scope 注解的使用？自定义作用域的实现？结合 Spring 框架聊聊


### Q26：【A】什么是 FactoryBean？与普通 Bean 和 BeanFactory 的区别？结合 Spring 框架聊聊 👑⭐


### Q27：【A】BeanDefinition 的作用？Bean 元数据的存储和管理？结合 Spring 框架聊聊 ⭐


### Q28：【S】BeanFactory 和 ApplicationContext 的区别？各自的使用场景？结合 Spring 框架聊聊 👑


### Q29：【S】BeanPostProcessor 的作用？如何自定义 Bean 的后置处理？结合 Spring 框架聊聊 👑⭐


### Q30：【S】Spring Bean 的生命周期？完整的创建和销毁流程？ 👑⭐


### Q31：【S】Spring Bean 的作用域？singleton 和 prototype 的实现原理？ 👑


### Q32：【A】Spring 的初始化和销毁回调？多种方式的执行顺序？ ⭐


### Q33：【A】Spring 的懒加载机制？@Lazy 注解的实现原理？


### Q34：【S】Spring 的三级缓存机制？如何解决循环依赖问题？ 👑⭐


### Q35：【B】Spring 容器的扩展点？Aware 接口的设计和使用？


### Q36：【A】Spring 容器的启动过程？refresh() 方法的核心步骤？ ⭐


### Q37：【S】Spring 如何处理循环依赖？构造器循环依赖为什么无法解决？ 👑⭐


------

## 模块四：AOP 与动态代理

### Q38：【A】@Aspect 注解的使用？如何定义切面和通知？结合 Spring 框架聊聊 👑


### Q39：【A】如何实现自定义的 AOP 功能？切面的最佳实践？结合 Spring 框架聊聊 👑


### Q40：【A】如何在 AOP 中获取方法参数和返回值？ProceedingJoinPoint 的使用？


### Q41：【S】什么是 AOP？面向切面编程的核心概念和优势？结合 Spring 框架聊聊 👑


### Q42：【A】AspectJ 定义的通知类型？Before、After、Around 等的使用场景？


### Q43：【S】Spring AOP 的代理创建时机？什么时候使用 CGLIB 代理？ 👑⭐


### Q44：【A】Spring AOP 的多切面执行顺序？@Order 注解的作用？ ⭐


### Q45：【A】Spring AOP 的切点表达式？execution、within、args 等指示符？


### Q46：【S】Spring AOP 的实现原理？JDK 动态代理和 CGLIB 代理的选择？ 👑⭐


### Q47：【S】Spring AOP 的限制？什么情况下 AOP 不会生效？ 👑⭐


### Q48：【B】Spring AOP 的性能影响？如何优化 AOP 的性能？ ⭐


### Q49：【A】Spring AOP 和 AspectJ 的区别？各自的实现方式和特点？


### Q50：【A】Spring AOP 中的织入时机？运行时织入的实现原理？ ⭐


------

## 模块五：Spring MVC 与请求处理

### Q51：【S】@Controller 和 @RestController 的区别？JSON 响应的处理？结合 Spring 框架聊聊 👑


### Q52：【S】@RequestMapping 和衍生注解的区别？@GetMapping 等的使用场景？结合 Spring… 👑【截图文字不全】


### Q53：【S】拦截器和过滤器的区别？各自的使用场景和执行时机？结合 Spring 框架聊聊 👑


### Q54：【A】什么是 MVC 模式？Spring MVC 的架构设计和优势？


### Q55：【S】Spring MVC 的参数绑定？@RequestParam、@PathVariable、… 👑【截图文字不全】


### Q56：【A】Spring MVC 的处理器映射？@RequestMapping 注解的匹配规则？


### Q57：【S】Spring MVC 的核心组件？DispatcherServlet 的作用和工作流程？ 👑


### Q58：【A】Spring MVC 的拦截器？HandlerInterceptor 的实现和配置？ 👑


### Q59：【B】Spring MVC 的内容协商？如何支持多种响应格式？


### Q60：【A】Spring MVC 的视图解析？ViewResolver 的工作原理？


### Q61：【A】Spring MVC 的数据验证？@Valid 和 @Validated 的使用？


### Q62：【S】Spring MVC 的完整请求处理流程？从请求到响应的详细步骤？ 👑


### Q63：【A】Spring MVC 的文件上传？MultipartFile 的处理机制？


### Q64：【B】Spring MVC 的异步处理？DeferredResult 和 Callable 的使用？ ⭐


### Q65：【A】Spring MVC 的异常处理机制？@ExceptionHandler 的使用？ 👑


### Q66：【A】Spring 的 Bean 验证？@Valid 和 @Validated 的区别？


------

## 模块六：事务原理与事务失效

### Q67：【S】@Transactional 注解的实现原理？事务代理的创建过程？结合 Spring 框架聊聊 👑⭐


### Q68：【A】Spring 事务的超时控制？timeout 参数的作用和实现？


### Q69：【S】Spring 事务的传播行为？七种传播级别的含义和使用场景？ 👑⭐


### Q70：【S】Spring 事务的隔离级别？与数据库隔离级别的关系？ 👑


### Q71：【S】Spring 事务的回滚机制？rollbackFor 和 noRollbackFor 的使用？ 👑


### Q72：【A】Spring 事务的最佳实践？事务设计的原则和注意事项？


### Q73：【A】Spring 事务管理的实现方式？声明式事务和编程式事务？


### Q74：【A】Spring 事务管理器？DataSourceTransactionManager 的工作原… ⭐【截图文字不全】


### Q75：【S】Spring 事务管理中 AOP 的应用？@Transactional 的实现原理？ 👑⭐


### Q76：【S】Spring 事务失效的常见场景？如何避免事务不生效？ 👑⭐


### Q77：【B】Spring 事务与多数据源？如何实现多数据源的事务管理？ ⭐


------

## 模块七：MyBatis 原理与使用

### Q78：【A】什么是 MyBatis？与 Hibernate 的区别和各自的优势？


### Q79：【A】MyBatis 的插件机制？Interceptor 的实现和应用场景？ ⭐


### Q80：【S】MyBatis 的动态 SQL？if、choose、foreach 等标签的使用？ 👑


### Q81：【A】MyBatis 的分页实现？PageHelper 插件的工作原理？


### Q82：【S】MyBatis 的缓存机制？一级缓存和二级缓存的实现原理？ 👑


### Q83：【A】MyBatis 的结果映射？ResultMap 的配置和自动映射？


### Q84：【A】MyBatis 的批量操作？foreach 标签和 BatchExecutor？


### Q85：【A】MyBatis 的最佳实践？与 Spring 事务的集成和注意事项？


### Q86：【S】MyBatis 的 SQL 映射？#{} 和 ${} 占位符的区别和安全性？ 👑


### Q87：【C】MyBatis 是否适用于非关系型数据库，对于这个场景有什么思考？【偏题：跨数据库适用性】


### Q88：【A】Spring 集成 MyBatis 的配置？SqlSessionFactory 的创建过程？ ⭐


------

## 模块八：条件配置与扩展特性

### Q89：【A】@Conditional 注解体系？条件化配置的实现原理？结合 Spring 框架聊聊


### Q90：【B】@EnableXxx 注解的设计模式？如何实现模块化配置？结合 Spring 框架聊聊


### Q91：【A】@Import 注解的使用？配置类的导入和组合？结合 Spring 框架聊聊


### Q92：【A】@Profile 注解的使用？多环境配置的最佳实践？结合 Spring 框架聊聊


### Q93：【B】Spring 的国际化支持？MessageSource 的使用和配置？


### Q94：【B】Spring 的环境抽象？Profile 和 PropertySource 的作用？


### Q95：【B】Spring 的类型转换系统？Converter 和 Formatter 的区别？


### Q96：【A】Spring 的事件机制？ApplicationEvent 和 ApplicationListener？


### Q97：【A】Spring 的条件化配置？@Conditional 注解的实现机制？


### Q98：【B】Spring 的验证框架？JSR-303 注解验证的集成？


### Q99：【B】Spring 的资源抽象？Resource 接口的设计和实现？


### Q100：【B】Spring 如何与其他框架集成？集成原理和最佳实践？
