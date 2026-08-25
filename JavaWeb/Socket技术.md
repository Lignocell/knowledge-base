# Socket技术

首先，我们通过Socket技术（它是计算机之间进行通信的一种方式）来实现两台计算机之间的通信，Socket也被翻译为套接字，是操作系统底层提供的一项通信技术，支持TCP和UDP。而java就对Socket进行了封装，以便于利用。

要实现Socket通信，首先就需要一个数据发送者和一个数据接收者，也就是客户端和服务端，我们需要提前启动服务端，来等待服务端连接，而客户端只需要随时启动去连接服务端即可。默认采用TCP连接。

首先先编写服务端，服务端使用ServerSocket对象来实现，还记得我们之前说过，每一个应用都需要一个端口去链接，那么此时可以绑定一个端口号来用于客户端的连接。

```java
ServerSocket server=new ServerSocket(1212);  //参数为绑定的接口，之后一律使用此端口进行通信
```

创建好后，由于服务器会一直占用资源，所以我们需要和之前的IO一样进行释放：

```java
try(ServerSocket server =new ServerSocket(1212)){
    
}catch(IOException e){
    e.printStackTrace();
}
```

接着，我们可以调用`accept()`方法来监听客户端的连接，如果没有客户端连接，程序现在处于阻塞状态，等待客户端连接：

```java
try(ServerSocket server =new ServerSocket(1212)){
 server.accept();   
}catch(IOException e){
    e.printStackTrace();
}
```

当客户端连接到来时，accept()会返回结果，我们可以打印出来返回结果：

```java
Socket s=server.accept();
System.out.println("接受来自客户端的连接，+s.getInetAddress()+":"+s.getPort());
//getInetAddress返回的是客户端的ip地址
//getPort返回的是客户端的端口号
```

接着，我们来编写客户端，同样使用Socket对象来完成，两个参数分别是服务端地址和接口，这里我们因为是本地连接服务端，也就是自己链接自己，所以我们使用本机的ip就可以：

```java
Socket socket=new Socket("localhost",1212);
```

各位可以尝试输入一下`ipconfig`命令查看网络列表，这里解释一下localhost。92.168.x.x。27.0.0.1的区别：

> 所有计算机都有一个特殊的网络和IP地址，27.0.0.1，它被称作是本地环回地址，我们访问此IP地址等于访问这台电脑自己，这个地址主要用于本地主机和本地服务之间的通信，所以说如果我们要访问自己电脑上的服务端，只需要填写这个IP地址即可。
>
> 那这个跟我们从路由器得到的IP地址有什么区别吗，路由器得到192.168.XX.XX是路由器为我们分配的一个局域网地址，使用自己的地址同样可以代表这台计算机本身，但是当我们切换网络时，局域网地址可能会出现变化，所以说它不适合作为本地连接的IP地址使用。
>
> localhost实际上是一个域名，但是它等价于127.0.0.1，操作系统自带的域名解析（通过本地主机文件hosts实现）可以将其自动解析到127.0.0.1上，所以说很多时候我们使用localhost也可以代表本地主机。但是注意，在我们之后学习Web服务器时，浏览器会将它们认为是两个不同的站点。

当Socket对象创建时，就会自动连接了：

```java
try(Socket socket=new Socket("localhost",1212)){
    System.out.println("成功连接到服务端");
}catch(IOEexception e){
    e.printStackTrace();
}
```

先启动服务端，再启动客户端，这样就成功了。

![image-20250607161007758](D:/knowledge_point/images/image-20250607161007758.png)

注意：客户端不需要指定自己的端口，一般都是自动分配，所以说我们收到来自客户端的连接时一般都是一个随机的端口号，然后前面的IP地址就是客户端用于访问我们服务端的IP地址，如果各位使用局域网IP地址访问的话，这里会出现一些变化哦。

## 使用Socket数据运输

我们前面介绍了使用Socket来建立两台计算机之间的连接，现在我们来进行数据传输。

我们可以通过Socket直接获取一个输入流和一个输出流，这和JavaSE一样：

```java
 server.accept();//等待客户端连接
 Socket s=server.accept();
 System.out.println("接受来自客户端的连接，+s.getInetAddress()+":"+s.getPort());

 InputStream in=s.getInputStream();
 int len=0;
 byte[] buffer=new byte[1024];
 while((len=in.read(buffer))>0){  //当客户端没有数据发送时，read会陷入阻塞状态
 System.out.println("接收到客户端数据，+new String(buffer,0,len));
```

接下来编写客户端这边，不断地读取控制台上的数据，不断向服务端发送数据：

```java
  try(Socket socket=new Socket("localhost",1212);
        Scanner sc=new Scanner(System.in)){
            System.out.println("已连接到服务器");

            OutputStream os=socket.getOutputStream();
            while(true){
                System.out.print("请输入要发送的数据，);
                String data=sc.nextLine();
                os.write(data.getBytes());
            }
        }catch(IOException e){
            e.printStackTrace();
        }
    }
```

然后，我们接下来启动试试：

<img src="D:/knowledge_point/images/image-20250607162712366.png" alt="image-20250607162712366" style="zoom:50%;" />

<img src="D:/knowledge_point/images/image-20250607162725395.png" alt="image-20250607162725395" style="zoom:50%;" />

这样，我们就成功了，如果我们此时想要当客户端发送了数据以后，服务端发送一个收到的回复的话，我们可以继续编写：

```java
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
int len;
byte[] buffer = new byte[1024];
 while ((len = in.read(buffer)) > 0) {   //当客户端没有数据发送时，read会处于阻塞状态
    System.out.println("接受到客户端数据: " + new String(buffer, 0, len));
    out.write(("已收到长度为 " + len + " 字节的数据").getBytes());   //将响应内容写入到输出流
}
```

在客户端这边，同样在发送完数据后阻塞读取一次数据：

```java
InputStream in=socket.getInputStream();
//阻塞读取响应内容
int len;
byte[] buffer = new byte[1024];
len = in.read(buffer);
System.out.println(new String(buffer, 0, len));
```

现在当客户端发送数据后，服务端就会实时响应结果给客户端，实现消息互相发送：

<img src="D:/knowledge_point/images/image-20250607163643265.png" alt="image-20250607163643265" style="zoom:50%;" />

除了发送消息之外，有了输入输出流，即使是文件传输也不在话下，我们可以来编写一个文件传输程序，让客户端传输文件到服务端去：

```java
try(ServerSocket server = new ServerSocket(8080)) {
    Socket socket = server.accept();
    System.out.println("接受到来自客户端的连接准备开始进行文件传输"););
    InputStream in = socket.getInputStream();
    FileOutputStream stream = new FileOutputStream("test");
    long len, total = 0;
    byte[] buffer = new byte[1024];
    while ((len = in.read(buffer)) > 0) {
        System.out.println("正在进行文件传输，当前已接收: " + total + " 字节数据");
        stream.write(buffer, 0, (int) len);
        total += len;
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

```java
try (Socket socket = new Socket("localhost", 8080);
     Scanner scanner = new Scanner(System.in)) {
    System.out.println("已连接到服务端，请输入要发送的文件路径: ");
    OutputStream out = socket.getOutputStream();
    FileInputStream stream = new FileInputStream(scanner.nextLine());
    stream.transferTo(out);
} catch (IOException e) {
    e.printStackTrace();
}
```

各位小伙伴同样可以试试看从一台电脑发送文件到另一台电脑上。

## Socket实现UDP通信

接下来，我们来看看如何使用Socket来实现UDP通信，java为我们提供了DatagramSocket API，它是一种UDP Socket，用于发送和接收UDP数据包。

由于UDP并不像TCP那样需要提前连接，所以我们只需要创建一个Socket等待数据来即可。

```java
try(DatagramSocket ds=new DatagramSocket(8080)){  //端口号
    
}catch(IOException e){
    e.printStackTrace();
}
```

接着，我们即可连续读取客户端发送来的数据：

```java
while(true){
    //UDP数据包，类似于数据缓存区，数据会先存入那里
    DatagramPacket dp=new DatagramPacket(new byte[1024],1024);
    ds.receive(dp);  //将收集到的数据送入DatagramPacket对象
    System.out.println(new String(dp.getData()));
}
```

客户端这边由于不需要预先建立连接，所以我们直接创建一个UDP数据包，并在数据包中指定发送的IP地址和端口等内容，发送后直接就可以到达：

```java
try (DatagramSocket socket = new DatagramSocket();
     Scanner scanner = new Scanner(System.in)) {
    while (true) {
        String str = scanner.nextLine();
        byte[] data = str.getBytes();
        InetAddress address = InetAddress.getByName("127.0.0.1");  //直接在数据包中填写要发送到的目标主机IP地址和端口信息
        DatagramPacket packet = new DatagramPacket(data, data.length, address, 8080);
        socket.send(packet);
    }
} catch (IOException e){
    e.printStackTrace();
}
```

这个相比TCP就简单很多了，直接发送就能收到：

![QQ_1721295794893](https://oss.itbaima.cn/internal/markdown/2024/07/18/wtQ43YDA7MjsUTC.png)



这里简单介绍了一下UDP通信。

## 使用浏览器访问Socket服务器

最后我们来研究一下HTTP协议，我们前面说过，浏览器访问一个网站实际上用的就是HTTP协议，并且HTTP协议是基于TCP协议的，所以说我们可以创建一个ServerSocket来处理浏览器的访问请求，看看HTTP请求到底长啥样。首先我们还是直接编写一个服务端来等待连接：

```java
try(ServerSocket server = new ServerSocket(8080)){
    Socket socket = server.accept();
    InputStream in = socket.getInputStream();
    while (!socket.isClosed()) {
        int i = in.read();
        if(i == -1) break;
        System.out.print((char) i);
    }
}catch (IOException e){
    e.printStackTrace();
}
```

此时我们使用Chrome浏览器访问：[http://localhost:8080](http://localhost:8080/)，可以直接在服务端收到以下数据：

![QQ_1721298866890](https://oss.itbaima.cn/internal/markdown/2024/07/18/eQdhX6LrRwJbpTK.png)



这正是我们之前说的HTTP协议对应的报文格式，可以看到当我们使用浏览器访问服务端时，浏览器会默认向我们的服务端发送一个GET请求，路径为根路径"/"，并且还包含了很多请求标头。

但是此时我们会发现，浏览器会一直处于加载中状态：

![QQ_1721299010236](https://oss.itbaima.cn/internal/markdown/2024/07/18/REX4Q2Og8em1WGK.png)



这是因为HTTP规定请求完成之后服务端需要给一个响应结果，所以说浏览器实际上一直在等待我们的服务端发送一个请求结果给它，但是我们这里没有做任何处理，所以说就会一直卡住。

现在我们来尝试给它返回一个简单的HTML页面（看不懂代码没关系，这里只是测试一下）

```java
try(ServerSocket server = new ServerSocket(8080)){
    Socket socket = server.accept();
    OutputStreamWriter writer = new OutputStreamWriter(socket.getOutputStream());
    String html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>测试网站</title>
            </head>
            <body>
                <h1>欢迎访问我们的测试网站</h1>
                <p>这个网站包含很多你喜欢的内容，但是没办法展示出来，因为我们还没学会</p>
            </body>
            """;
    writer.write("HTTP/1.1 200 OK\r\n");   //根据HTTP协议规范，返回对应的响应格式
    writer.write("Content-Type: text/html;charset=utf-8\r\n");  //务必加一下内容类型和编码，否则会乱码
    writer.write("\r\n");
    writer.write(html);
    writer.flush();
}catch (IOException e){
    e.printStackTrace();
}
```

此时我们使用Chrome浏览器再次访问服务端，就可以展示出我们返回的数据了：

![QQ_1721299638581](https://oss.itbaima.cn/internal/markdown/2024/07/18/CT3YFcXf5HOiPne.png)



是不是感觉非常神奇，只需要返回给浏览器一个HTML代码，就成功以网站的形式打开了。这也是我们后续学习的主要方向，只不过使用Socket这种框架来编写网站，太过于原始了，尤其是对HTTP协议报文的处理上，自己写太过麻烦了，后面我们会学习各种Web服务端，它们是专用于网站服务器的程序，我们就能快速编写更加高级的Web应用程序。
