# Listener

监听器不是重点，只做了解，什么是监听器呢：

如果我们希望，在应用程序加载的时候，或是Session创建的时候，亦或是在Request对象创建的时候进行一些操作，那么这个时候，我们就可以使用监听器来实现。

![img](https://oss.itbaima.cn/internal/markdown/2023/03/06/xl4hzgOaSCdXHcu.png)

默认为我们提供了很多类型的监听器，这里我们就演示一下监听器Session的创建即可：

```java
@WebListener
public class TestListener implements HttpSessionListener {
    @Override
    public void sessionCreated(HttpSessionEvent se) {
        System.out.println("有一个Session被创建了");
    }
}
```

了解即可。
