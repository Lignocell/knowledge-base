## 架构梳理



|      |           目录            |                             目的                             |
| :--: | :-----------------------: | :----------------------------------------------------------: |
|      |          main.go          |                            主函数                             |
|      |            ig/            | 实现设备与服务端之间的通信，将设备消息转换成系统内部的数据，再将处理结果返回给设备。|
|      |           api/            |                      设备绑定解绑查询。                     |
|      |           ota/            |                  管理设备固件升级配置下发。                 |
|      |          vision/          |                 视觉模型接口用于图片识别等。                |
|      |      configs/server/      |                       负责服务端配置。                      |
|      |           user/           |          实现用户注册登录以及基于 JWT 的身份认证。          |
|      |    core/connection*.go    | 每台设备的连接生命周期，包括建立连接存活时间以及断开连接等。|
|      |        core/chat/         |          负责对话流程管理，并维护会话上下文和记忆。         |
|      |    core/providers/asr/    |                        语音识别服务。                       |
|      |    core/providers/llm/    |                 统一封装AI接口，如 OpenAI。                 |
|      |    core/providers/tts/    |                 语音服务，将文本转换为语音。                |
|      |   core/providers/vllm/    |               提供视觉AI能力，支持图片理解等。              |
|      |         core/mcp/         |              实现 MCP 协议，支持 AI 进行调用。              |
|      |      core/function/       |                     管理 AI 可调用功能。                    |
|      |        core/image/        |                        负责图片处理。                       |
|      |        core/pool/         |                    管理连接池及相关资源。                   |
|      |        core/auth/         |         实现设备的身份认证，与用户登录认证相互独立。        |
|      | core/transport/websocket/ |              基于 WebSocket 与设备建立长连接。              |
|      |          models/          |                定义用户、设备以及绑定关系等、               |
|      |     configs/database/     |                         数据库相关。                        |
|      |         binding/          |                          绑定相关。                         |
|      |         registry/         |                  设备注册，注册信息持久化。                 |
|      |           task/           |                 本地异步任务调度，Worker池。                |
|      |      user/service.go      |                     实现用户注册、登录、                    |
|      |        user/jwt.go        |                     封装 JWT 的生成等。                     |
|      |       user/auth.go        |                          用户鉴权。                         |
|      |      user/handle.go       |            提供用户模块的Controller，与HTTP交互。           |
|      |       user/redis.go       |                          初始化Reds                          |

## 当前待整理的问题

|                             问题                             |                           当前情况                           |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| stress.go、stress2.go、wsclient.go、test/connectivity.go、test/pool_recycling.go | 都定义了 main 函数，编译时报错，目前临时移除项目并做了备份，没有上传到git仓库。|
|                     编译代码时服务器卡死                     | 加入Swap缓存区，以及限制编译并行度，是否考虑升级服务器配置。|





---

## 任务目标

**1. 用户系统基础** 
注册、登录、JWT签发，密码BCrypt加密，唯一索引防并发重复注册

**2. 接口鉴权改造**
绑定接口(bind/unbind)、IG通信接口(message/image/control/broadcast)全部接入JWT鉴权，替换掉之前前端随便传user_id"的不安全模式

**3. 管理员权限校验**
补一个AdminOnly，把 /devices/online、/bindings、/bindings/:user_id 这几个全局查询接口，改为仅管理员可见

**4. 补充管理员专属的用户管理接口** 

- 查看所有注册用户列表（分页）
- 查看/修改指定用户状态（封禁/解封）
- 管理员手动重置某用户密码
- 手动删除某用户（采用软删除，将状态置为：delete）

**5. 登录安全加固**
用Redis做登录失败次数限制，防止枚举

**6. 后台管理可视化界面** — html+css/vue
基于第一、二步接口做登录页+后台管理。

**7. App对接**

**8. 补充**：

- **接口文档化**——用md或者Knife4j或者swagger。
- **测试数据清理**