# Spring Cloud

> 目标：2027 年中国大陆暑期实习，首选 Google（谷歌）/ Microsoft（微软）；以 Java 为主力语言、偏后端方向；兼顾国内其他公司的后端实习；共 101 题，只列题目，不填写答案。
> 图标：👑 重点；⭐ 难点；👑⭐ 重难点。档位表示复习优先级，难点不一定优先做。

| 档位 | 定位 | 复习安排 | 题数 |
| --- | --- | --- | --- |
| S | 核心必做 | 第一轮完成，能独立讲清并应对追问 | 16 |
| A | 重点掌握，常见考察与延伸 | 第二轮完成，掌握概念、原理与应用 | 48 |
| B | 有概率考察，补充细节 | S、A 稳定后再补 | 37 |
| C | 特别偏，低优先 | 最后浏览，时间紧可暂缓 | 0 |

> 本截图涉及较多旧组件，其实现细节一般列为 B 档；先掌握微服务原理及项目实际使用的组件。保留截图原题，不额外扩展技术栈。
> 版本提示依据：[Spring Cloud Netflix 维护模式说明](https://cloud.spring.io/spring-cloud-netflix/multi/multi__modules_in_maintenance_mode.html)、[Sleuth 官方说明](https://docs.spring.io/spring-cloud-sleuth/docs/current/reference/html/index.html)。

## 模块一：微服务基础与架构

#### Q1：【A】单体应用、SOA 和微服务架构有什么区别？


#### Q2：【A】什么是服务治理？Spring Cloud 提供了哪些服务治理功能？


#### Q3：【B】什么是领域驱动设计（DDD）？在 Spring Cloud 项目中如何应用？ ⭐


#### Q4：【S】什么是微服务？微服务架构有哪些核心特征？ 👑


#### Q5：【S】什么是 Spring Cloud？它解决了哪些微服务问题？ 👑


#### Q6：【A】微服务架构带来了哪些挑战？Spring Cloud 如何解决？ 👑


#### Q7：【B】微服务架构如何进行版本管理？Spring Cloud 如何支持多版本部署？


#### Q8：【B】微服务架构中的安全问题如何解决？Spring Cloud Security 的作用？ ⭐


#### Q9：【S】微服务相对于单体应用有什么优势和劣势？ 👑


#### Q10：【A】Spring Cloud Alibaba 和 Spring Cloud Netflix 的区别？


#### Q11：【B】Spring Cloud 的依赖管理是如何工作的？


#### Q12：【A】Spring Cloud 的自动配置原理是什么？如何自定义配置？ ⭐


#### Q13：【S】Spring Cloud 由哪些核心组件组成？各自解决什么问题？ 👑


#### Q14：【B】Spring Cloud 有哪些版本？如何选择合适的版本？


#### Q15：【S】Spring、Spring Boot 和 Spring Cloud 的关系是什么？ 👑


------

## 模块二：注册发现与 Eureka

#### Q16：【B】@EnableEurekaClient 和 @EnableDiscoveryClient 的区别？


#### Q17：【A】服务注册中心宕机了怎么办？Spring Cloud 如何处理？ 👑


#### Q18：【B】如何实现多注册中心？Spring Cloud 支持吗？


#### Q19：【A】什么是 Eureka？Eureka Server 和 Eureka Client 的作用？


#### Q20：【B】什么是 Eureka 自我保护模式？如何配置和关闭？


#### Q21：【S】为什么需要服务注册与发现？在 Spring Cloud 中如何实现？ 👑


#### Q22：【B】Consul 在 Spring Cloud 中如何使用？有哪些特性？


#### Q23：【B】Eureka 的服务剔除机制是怎样的？相关参数如何配置？


#### Q24：【A】Eureka 的服务注册和发现流程是怎样的？


#### Q25：【B】Eureka 和 ZooKeeper 作为注册中心有什么区别？


#### Q26：【A】Eureka 如何实现高可用？集群配置需要注意什么？


------

## 模块三：Nacos

#### Q27：【A】如何在 Spring Cloud 中集成 Nacos 作为注册中心？ 👑


#### Q28：【A】什么是 Nacos？相比 Eureka 有哪些优势？ 👑


#### Q29：【A】Nacos 的服务注册表结构是怎样的？支持哪些数据格式？ ⭐


#### Q30：【A】Nacos 配置中心的长轮询机制是什么？ ⭐


#### Q31：【A】Nacos 中的 Namespace、Group、Service 的关系是什么？


#### Q32：【A】Nacos 作为配置中心如何使用？与 Config Server 的区别？


------

## 模块四：负载均衡与远程调用

#### Q33：【A】@LoadBalanced 注解的作用是什么？工作原理？


#### Q34：【A】如何在 Feign 中配置负载均衡策略？


#### Q35：【A】如何在 Feign 中实现请求拦截器？


#### Q36：【S】什么是 OpenFeign？相比原生 Feign 有什么改进？ 👑


#### Q37：【A】微服务的通信方式有哪些？Spring Cloud 支持哪些通信协议？ 👑


#### Q38：【B】为什么 Feign 第一次调用耗时很长？如何优化？ ⭐


#### Q39：【S】Feign 的工作原理是什么？如何生成代理对象？ 👑⭐


#### Q40：【A】Feign 如何处理请求参数和响应结果？支持哪些注解？


#### Q41：【A】Feign 如何处理异常？如何自定义错误解码器？


#### Q42：【A】Feign 如何配置超时时间？与 Ribbon 的超时配置关系？ 👑⭐


#### Q43：【B】Feign 如何实现日志记录？有哪些日志级别？


#### Q44：【B】Feign 如何支持文件上传？需要哪些配置？


#### Q45：【A】RestTemplate 和 Feign 的区别是什么？如何选择？


#### Q46：【A】Spring Cloud LoadBalancer 和 Ribbon 的区别？


#### Q47：【B】Spring Cloud 和 Dubbo 的区别是什么？各自适用场景？


#### Q48：【S】Spring Cloud 中的负载均衡是如何实现的？ 👑


#### Q49：【A】Spring Cloud 中有哪些远程调用方式？各自的特点？


------

## 模块五：配置中心与动态刷新

#### Q50：【A】配置中心如何处理敏感信息？支持加密吗？可以结合 Spring Cloud 具体说说


#### Q51：【A】如何保证配置中心的高可用？可以结合 Spring Cloud 具体说说


#### Q52：【A】如何实现配置的动态刷新？@RefreshScope 的原理？ 👑


#### Q53：【A】什么是 Spring Cloud Config？工作原理是什么？


#### Q54：【A】为什么需要配置中心？Spring Cloud 提供了哪些配置管理方案？ 👑


#### Q55：【B】Spring Cloud Bus 的作用是什么？如何实现配置广播？


#### Q56：【B】Spring Cloud 的 Config Client 如何获取配置？配置文件命名规则是什么？


#### Q57：【B】Spring Cloud 的 Config Server 如何搭建？支持哪些存储后端？


------

## 模块六：熔断、降级与限流

#### Q58：【A】@SentinelResource 注解的作用是什么？如何使用？


#### Q59：【S】什么是断路器？Spring Cloud 中如何实现？ 👑


#### Q60：【S】什么是服务降级？在 Spring Cloud 中如何实现？ 👑


#### Q61：【S】什么是服务熔断？熔断和降级的区别是什么？ 👑


#### Q62：【S】什么是服务限流？Spring Cloud 支持哪些限流方式？ 👑⭐


#### Q63：【S】什么是微服务雪崩效应？Spring Cloud 如何防止？ 👑


#### Q64：【A】什么是 Sentinel？相比 Hystrix 有哪些优势？


#### Q65：【A】Sentinel 的控制台如何使用？如何配置规则？


#### Q66：【A】Sentinel 如何实现限流？支持哪些限流算法？ 👑⭐


#### Q67：【A】Sentinel 在 Spring Cloud 中如何使用？


------

## 模块七：网关与 Gateway

#### Q68：【S】什么是 Spring Cloud Gateway？核心概念有哪些？ 👑


#### Q69：【S】为什么需要 API 网关？Spring Cloud 提供了哪些网关组件？ 👑


#### Q70：【A】Spring Cloud Gateway 的工作流程是什么？ 👑⭐


#### Q71：【B】Spring Cloud Gateway 和 Zuul 的区别是什么？


#### Q72：【A】Spring Cloud 的 Gateway 的过滤器有哪些类型？如何自定义过滤器？


#### Q73：【A】Spring Cloud 的 Gateway 如何处理跨域问题？


#### Q74：【A】Spring Cloud 的 Gateway 如何配置路由规则？支持哪些断言工厂？ 👑


#### Q75：【A】Spring Cloud 的 Gateway 如何实现负载均衡？


#### Q76：【B】Spring Cloud 的 Gateway 如何实现灰度发布？ ⭐


#### Q77：【A】Spring Cloud 的 Gateway 如何实现限流？有哪些限流策略？ 👑⭐


#### Q78：【A】Spring Cloud 的 Gateway 如何与注册中心集成？支持动态路由吗？


------

## 模块八：链路追踪与监控

#### Q79：【B】什么是 Spring Cloud Sleuth？核心概念有哪些？【旧链路追踪组件，降低优先级】


#### Q80：【A】为什么需要链路跟踪？Spring Cloud 如何实现？


#### Q81：【B】Sleuth 如何与 Zipkin 集成？数据如何收集和展示？【旧链路追踪组件，降低优先级】


#### Q82：【A】Spring Boot Actuator 在微服务监控中的作用？提供了哪些端点？


------

## 模块九：分布式事务与服务拆分

#### Q83：【A】微服务架构中的数据一致性问题如何解决？ 👑⭐


#### Q84：【A】微服务架构中如何处理跨服务事务？Spring Cloud 有哪些方案？ 👑⭐


#### Q85：【A】微服务如何进行服务拆分？有哪些拆分策略？ 👑


------

## 模块十：部署与工程实践

#### Q86：【B】Spring Cloud 如何与 Docker 和 Kubernetes 集成？ ⭐


#### Q87：【B】Spring Cloud 项目如何实现优雅启动和关闭？


------

## 模块十一：旧组件：Ribbon

#### Q88：【B】如何配置 Ribbon 的超时时间和重试机制？可以结合 Spring Cloud 具体说说


#### Q89：【B】什么是 Ribbon？Ribbon 的负载均衡策略有哪些？


#### Q90：【B】在 Spring Cloud 中，如何自定义 Ribbon 的负载均衡策略？


#### Q91：【B】Ribbon 的工作原理是什么？如何与 Eureka 集成？


#### Q92：【B】Ribbon 的配置参数有哪些？如何调优？可以结合 Spring Cloud 具体说说


#### Q93：【B】Ribbon 如何实现服务实例的健康检查？可以结合 Spring Cloud 具体说说


------

## 模块十二：旧组件：Hystrix

#### Q94：【B】如何配置 Hystrix 的各种参数？核心参数有哪些？ ⭐


#### Q95：【B】什么是 Hystrix Dashboard？如何搭建监控面板？


#### Q96：【B】什么是 Hystrix？Hystrix 的核心功能有哪些？


#### Q97：【B】Feign 如何与 Hystrix 集成实现熔断？


#### Q98：【B】Hystrix 的工作原理是什么？断路器状态如何转换？ ⭐


#### Q99：【B】Hystrix 的线程池隔离和信号量隔离有什么区别？ ⭐


------

## 模块十三：旧组件：Zuul

#### Q100：【B】什么是 Spring Cloud Zuul？Zuul 1.x 和 2.x 的区别？


------

## 模块十四：并发基础（截图混入题）

#### Q101：【A】线程之间如何通信及线程之间如何同步 👑【截图混入的并发题，保留不漏】
