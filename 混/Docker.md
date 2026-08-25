# Docker技术

Docker官网，https://www.docker.com

## 容器技术入门

在以前，我们想要安装一套环境，需要花费一整天去安装一套环境，而有了Dokcer之后，我们的程序和环境部署就很简单了，只要把这些环境的打包成一个镜像。到服务器部署时，可以直接下载镜像实现一键部署，做到开箱即用。

### 从虚拟机到容器

容器火的根本原因还是它的集装箱思想，我们知道，如果我们要写一个比如论坛、电商这类的Java项目，那么数据库、消息队列、缓存这类中间件是必不可少的，因此我们如果想要将一个服务部署到服务器，那么实际上还要提前准备好各种各样的环境，先安装好MySQL、Redis、RabbitMQ等应用，配置好了环境，再将我们的Java应用程序启动，整个流程下来，光是配置环境就要浪费大量的时间，如果是大型的分布式项目，可能要部署很多台机器，那岂不是我们得一个一个来？项目上个线就要花几天时间，显然是很荒唐的。

而容器可以打包整个环境，比较MySQL、Redis等以及我们的Java应用程序，可以被一起打包为一个镜像，当我们需要部署服务时，只需要像我们之前那样，直接下载镜像运行即可，不需要再进行额外的配置了，整个镜像中环境是已经配置好的状态，开箱即用。

### 容器工作机制描述

我们先来看看Docker的整体架构：

![](https://oss.itbaima.cn/internal/markdown/2022/06/30/PeaxwNQXkiYSlUv.png)

实际上分三个部分：

- Docker客服端：docker命令都是在客户端上执行的，操作会发送到服务端上处理。
- Docker服务端：服务端是启动容器的主体，一般是作为服务在后台运行，支持远程连接。
- Registry：存放Docker镜像的仓库，跟Maven一样，可以分为公有仓库和私有仓库，镜像可以从仓库下载到本地存放。

当我们需要在服务器上部署一个已经打包好的应用与环境，我们只需要下载打包好的镜像就可以了，我们执行：

```sh
sudo docker run -d -p 80:80 nginx
```

管理员执行docker，d表示后台模式，p80:80是端口，Nginx是镜像名称。

实际上，命令输入后：

1. Docker客户端将操作发送给服务端，告诉服务器我们要运行nginx这个镜像。
2. Docker服务器先去看看本地有没有这个镜像，发现没有。
3. 接着，去公共仓库Docker Hub去查找下载镜像了。
4. 下载完成后，镜像成功保存到本地。
5. Docker服务端加载Nginx镜像，启动容器开始正常运行（容器和容器之间，容器与外部之间，相互隔离，互不影响）。

所以，整个流程中，Docker就像是一搜运输船，镜像就像是集装箱，通过运输船将世界各地的货物送往我们的港口，货物到达港口后，Docker并不关心集装箱里面的是什么，只需要创建容器开箱即用就可以了。相比我们传统的手动安装配置环境，不知道方便了几个层次。

不过容器依然是寄托于宿主主机的运行的，所以一般在生产环境下，都是通过虚拟化先创建多台主机，然后再到各个虚拟机中部署Docker，这样的话，运维效率就大大提升了。

从下一章开始，我们就正式地来学习一下Docker的各种操作。

## 容器和镜像

启动容器最关键的就是镜像，我们先来学习镜像。

### 初试容器镜像

首先，我们先了解一下镜像的相关操作，比如我们希望先从服务器内将一个镜像部署到本地，这里选用`hello world`，这个真是万年不变。

```sh
docker pull hello-world
```

![image-20220701111043417](https://oss.itbaima.cn/internal/markdown/2022/07/01/tZ4S2HYvNKr7qiD.png)

可以看到Using default tag，事实上，一个镜像的名称有两部分组成，一个是`repository`，还有一个是`tag`，其中，repository为镜像名称，tag则是版本号，一般latest表示最新版本。

所以，如果想要指定的话：

```sh
dacker pull hello-world 1.1.2
```

镜像下载到本地后，想要启动容器，那么直接：

```sh
dacker run hello-world
```

当然，如果仅仅是只想创建而不想马上运行的话，可以使用：

```sh
docker create hello-world
```

可以看到：

![image-20220701111314331](https://oss.itbaima.cn/internal/markdown/2022/07/01/Brl4cnK8WsjP7LV.png)

启动时，会使用当前镜像创建一个容器，可以输入ps来查看当前容器的列表：

```sh
docker ps -a
```

注意后面要加一个`-a`表示查看所有容器（其他选项可以使用-h查看），如果不加，只会显示当前运行中的容器，但是HelloWorld是一次性的不是Nginx那样的常驻程序，所以容器启动打印了上面的内容后，容器就停止运行了：

![image-20220701111840091](https://oss.itbaima.cn/internal/markdown/2022/07/01/zMN3TPR7aHu5YGb.png)

可以看到，我们创建的hello-world以及nginx，其中会生成随机id，创建时间，当前运行状态，以及可以起一个名称（一个镜像可以创建多个容器）。

在创建容器时，我们手动指定名称或者自动生成，名称可以用来运行容器：

```sh
docker run --name-lbwnb hello-world
```

![image-20220701125951980](https://oss.itbaima.cn/internal/markdown/2022/07/01/qOblnhr5CJiIBG6.png)

我们可以手动开启停止的容器：

```sh
docker start 容器名称/容器id
```

注意启动的对象我们要填写容器的ID或是容器的名称才可以，容器ID比较长，可以不写全只写一半，但是你要保证你输入的不完全容器ID是唯一的。

![image-20220701124845982](https://oss.itbaima.cn/internal/markdown/2022/07/01/XfFORtqhK9lcBi7.png)

如果想要停止容器直接输入stop命令就可以了：

```sh
 docker stop 容器名称
```

还有重启

```sh
docker restart 容器名称
```

如果不想要这个容器了，那么直接删除，并且该容器处于停止状态下：

```sh
docker rm 容器名称
```

如果我们希望容器停止后自动删除，可以在运行时加入`--rm`参数：

```sh
docker run --rm 镜像名称
```

删除后，容器将不复存在，当没有任何关于nginx的容器之后，我们可以删除nginx的本地镜像：

![image-20220701125204728](https://oss.itbaima.cn/internal/markdown/2022/07/01/bmHqND36yCUBPVj.png)

我们可以使用`images`命令来检查一下当前本地有那些镜像：

```sh
docker images
```

![image-20220701125514145](https://oss.itbaima.cn/internal/markdown/2022/07/01/fEscbGJXw4e7YFK.png)

至此，我们已经了解了Docker的简单使用。

### 镜像结构介绍

我一直将镜像比作房子的蓝图，而容器就是根据蓝图建的房子，所以房子可以建很多。

我们在打包项目时，实际上需要一个基本的操作系统环境，这样我们可以在该操作系统上安装各种依赖软件，比如数据库、缓存等，像这种基本的系统镜像，我们称为base镜像（精装房），我们的项目在之后基本都是基于base镜像打包：

另一些中是基于当前操作系统执行简单的命令，之前的Hello-World就是。

一般base镜像（毛坯房/地基）就是各个Linux操作系统的发行版，比如我们正在使用的Ubuntu，还有CentOS、Kali等等。这里我们下载CentOS的base镜像：

```sh
docker pull centos
```

Linux操作体系是由内核空间和用户空间组成，其中内核空间就是整个Linux系统的核心，Linux启动后会加载bootfs文件系统，加载完成后会自动卸载掉，之后会加载用户空间的文件系统，这一层是我们自己可以操作的部分：

- bootfs包含了BootLoader和Linux内核，用户是不能对这层做任何修改的，在内核启动后，bootfs会自动卸载。
- rootfs包含了系统常见的目录结构，包括`/dev`，`/proc`，`/bin`等等以及一些基本的文件和命令，也就是我们进入系统后能够操作整个文件系统，包括我们在Ubuntu下使用的apt和CentOS下使用的yum，都是用户空间上的。

base镜像底下使用的是宿主主机的内核，就是主机内核版本是多少，CentOS内核版本就是多少，而rootfs则可以在不同的容器中运行多种不同的版本。

使用`uname`可以查看当前内核版本：

```sh
uname -r
```

-r代表release表示版本号，uname表示打印操作系统的核心信息。

因此，Docker可以模拟多种Linux操作系统环境，我们可以尝试启动一下刚才下载的镜像：

```sh
Docker run -it centos
```

-i表示在容器上打开一个标准的输入接口，t表示分配一个伪tty设备，可以支持终端登录，一般是两个一起使用，否则base容器启动后就自动停止了。

![image-20220701135834325](https://oss.itbaima.cn/internal/markdown/2022/07/01/13BYcCWHsDMrwvq.png)

然后我们来看看内核版本：

```sh
uname -r
```

可以看到内核版本是一样的（这也是缺点，如果软件对内核版本有要求的话，那么此时Docker直接挂了）。

基于base镜像，我们就可以在此基础上安装各种各样的软件了，几乎所有的镜像都是从base的基础上安装和配置出来的：

![image-20220701143105247](https://oss.itbaima.cn/internal/markdown/2022/07/01/SDwEqz2b7lA9nJa.png)

每安装一个软件，就在base镜像上一层一层叠加上去的，这样多个容器可以将不同层次自由拼装，比如，现在好几个容器都需要使用CentOS的base镜像，而上面运行的软件不同，此时就可以使用分层结构，我们只需要本地保存一份base镜像，就可以给不同的容器拼装使用。

我们可以看到，除了软件之外，最上层还有一个可写容器层：

我们知道，所有的镜像会叠起来组成一个统一的文件系统，如果不同层中存在相同位置的文件，那么上层文件就会覆盖下层文件，最终我们看到的是一个叠加之后的文件系统；当我们需要修改容器中的文件时，实际上并不会对镜像进行直接修改，而是在最顶上的容器层进行修改，不会影响到下面的镜像，所以各个操作如下：（最上面一层称为容器层，下面称为镜像层）

- 文件读取：读取一个文件，Docker会从上往下依次寻找。
- 文件创建和修改：创建新文件会直接添加到容器层中；修改文件同样从头往下找，找到后复制到容器层再进行修改。
- 删除文件：从上往下，找到后不会删除，只会在容器层中标记这个删除操作（容器删除后才会删除）。

这样保证了镜像层的完整性，实现多个容器共享使用。

### 构建镜像

前面我们了解了Docker镜像的结构，实际上所有常用的应用程序都有对应的镜像，我们只需要下载这些镜像就可以使用了，而不需要手动安装，当然如果冷门的应用就得手动安装，接下来让我们看看如何搭建自己的Docker镜像。

构建镜像有两种方式，一种使用commit命令来完成，另一种是Dockerfile，我们现在看第一种。

比如，我们现在想要在Ubuntu的base镜像汇总安装Java环境，并打包成一个新的镜像。

启动Ubuntu，然后使用yum命令来安装Java环境：

```sh
docker pull ubuntu 
```

然后运行Ubuntu：

```sh
docker run -it ubuntu
```

直接使用apt命令来安装Java环境，在这之前更新一下：

```sh
apt update
```

接着：

```sh
apt install openjdk-8-jdk
```

安装完成后显示：

```sh
java -version
```

这样，我们就完成对Java的安装了，接着我们可以退出这个镜像，然后将其构成我们新的镜像：

![image-20220701152130041](https://oss.itbaima.cn/internal/markdown/2022/07/01/LAIx5GYCJhsbmSo.png)

我们使用commit命令可以将容器保存为新的镜像：

```sh
docker commit 容器名称 新的镜像名称
```

![image-20220701152302171](https://oss.itbaima.cn/internal/markdown/2022/07/01/sbWLlEoMj2ZPcUV.png)

![image-20220701152418060](https://oss.itbaima.cn/internal/markdown/2022/07/01/3q4juA8vOJew9W6.png)

可以看到，安装了软件之后的镜像比我们原有的大小大得多，这样我们就可以通过这个镜像来直接启动一个带Java的Ubuntu操作系统容器了；虽然自定义度很高，但是不是很推荐，因为效率很低，普通用户实际上采用Dockerfile更好一些。

首先，直接新建一个名为Dockerfile的文件：

```sh
touch Dockerfile
```

接着，我们来进行编辑，Dockerfile内部需要我们编写多种指令来告诉Docker我们镜像的相关信息：

```dockerfile
FROM base镜像
FROM ubuntu
```

首先，我们需要使用FROM指令来选择当前镜像的基础镜像（必须从这个指令开始），我们直接用ubuntu即可；当然如果不需要基础镜像的话，我们可以使用`scratch`表示从零开始。

基础镜像设定完成后，我们来安装Java环境：

```dockerfile
RUN apt update
RUN apt install -y openjdk-8-jdk
```

`-y`表示yes。

OK，现在我们的Dockerfile就编写完成了。

只要完成一次构建即可：

```sh
docker build -t <镜像名称> <构建目录>
docker build -t ubuntu-java-file .
```

执行后，Docker会在构建目录中选择Dockerfile文件，然后开始依次执行Dockerfile中的指令：

![image-20220701155443170](https://oss.itbaima.cn/internal/markdown/2022/07/01/g6RFwA5t4EsdvnY.png)

注意：Docker镜像构筑有缓存机制，计算中途退出重新进行构建，也会直接将之前已经构建好的每一层镜像，直接拿来用，除非修改了Dockerfile文件重新构建，只要某一层发生变化其上层的构建缓存都会失效，当然包括`pull`时也会有类似的机制。

![image-20220701155812315](https://oss.itbaima.cn/internal/markdown/2022/07/01/foLHIZScQ1KVbvC.png)



最后成功安装，会出现在本地：

![image-20220701155847721](https://oss.itbaima.cn/internal/markdown/2022/07/01/95ueUgyaTcrz6Mi.png)



可以看到安装出来的大小跟我们之前的是一样的，因为做的事情是一模一样的。

我们可以使用`history`命令来查看构建历史：

![image-20220701160128689](https://oss.itbaima.cn/internal/markdown/2022/07/01/GYyHFcjSKJwvWi6.png)

如果遇到镜像ID为missing的一般是从Docker Hub中下载的镜像会有这个问题，但是问题不大。

### 发布镜像到远程仓库

现在，我们可以将镜像发布到DockerHub中，就像Git远程仓库那样：

https://hub.docker.com

注册账号后，我们先创建一个公共的镜像仓库，然后将本地的镜像上传

然后我们执行这条指令：

```sh
docker tag ubuntu-java-file:latest 用户名/仓库名称:版本
```

这里我们将版本改为2.0版本吧，不用默认的latest（nagocoler是乱起的)。

这里的含义其实是相当于clone了一份需要上传的镜像，以供后续上传使用：

![image-20220701165231001](https://oss.itbaima.cn/internal/markdown/2022/07/01/chAPS2DFW5q7GkE.png)

接着我们需在本地登录一下：

```sh
docker login -u nagocoler
```

登录后即可上传：

```sh
docker push nagocoler/ubuntu-java:1.0
```

注意公共仓库是可以被搜索和下载的，所以我们这里把本地的镜像全部删掉，去下载我们刚刚上传好的镜像。这里我们先搜索一下，搜索使用`search`命令即可：

```sh
docker search nagocoler/ubuntu-java
```

![image-20220701170253126](https://oss.itbaima.cn/internal/markdown/2022/07/01/SIUpBOzN5vsiydn.png)

我们可以使用pull命令将其下载下来：

```sh
docker pull nagocoler/ubuntu-java:1.0
```

![image-20220701171148334](https://oss.itbaima.cn/internal/markdown/2022/07/01/uXBk3WPsDM4aZKo.png)

上传之后的镜像是被压缩过的，所以下载的内容就比较少一些。运行试试看：

![image-20220701171253440](https://oss.itbaima.cn/internal/markdown/2022/07/01/RJVdstMnxjSYFoW.png)

Docker Hub也可以自行搭建私服，但是这里就不多做介绍了。

## 容器网络管理

前面我们已经了解了一些基础操作，现在我们来学习容器的网络管理。

### 容器网络类型

Docker在安装完成后，会在我们的主机上创建三个网络，使用network ls查看：

```sh
docker network ls
```

![image-20220702161742741](https://oss.itbaima.cn/internal/markdown/2022/07/02/7KEumyqriRY2QU5.png)

可以看到，默认情况下有bridge，host，none三种网络类型，我们依次介绍，在这之前，我们先开一个镜像，然后把要用的搭建好：

```sh
docker run -it ubuntu
```

```sh
apt update
apt install net-tools iputils-ping curl
```

我们直接退出将其构建成一个新的镜像：

```sh
docker commit lucid_sammet ubuntu-net
```

#### none网络

这个网络除了本地回环网络之外没有其他的网络了，我们可以在创建容器时指定这个网络。

这里使用`--network`来指定网络：

```sh
docker run -it --network=none ubuntu-net
```

进入后，我们查看一下当前的网络：

```sh
ifconfig
```

可以看到只有一个本地环回`lo`网络设备：

![image-20220702170000617](https://oss.itbaima.cn/internal/markdown/2022/07/02/qL1oAkOCcIYRwZj.png)

所以现在这个容器是无法访问互联网的，单机运行，可以存点密码。

#### bridge网络

容器默认的网络类型，是桥接网络，也是应用最广泛的网络类型：

实际上，我们在宿主主机上查看网络信息，会发现一个名为docker()的网络设备：

![image-20220702172102410](https://oss.itbaima.cn/internal/markdown/2022/07/02/jDKSIriXec96uhy.png)

这个网络设备是Docker安装时自动创建的虚拟设备，我们可以来看一看默认创建的容器内部的情况：

```sh
docker run -it ubuntu-net
```

![image-20220702172532004](https://oss.itbaima.cn/internal/markdown/2022/07/02/5JdimQWMaCx7hy2.png)

可以看到，网络接口的地址为172.17.0.2，实际上这是Docker创建的虚拟网络，就像容器单独插入了一个虚拟的网线，连接到Docker创建的虚拟网络上，而docker()网络实际上作为一个桥接的角色，一头是自己的虚拟子网，另一头是宿主主机的网络。

网络拓补图类似于这样：

![image-20220702173005750](https://oss.itbaima.cn/internal/markdown/2022/07/02/xCKMIBwjq7gWOko.png)

通过添加这样的网桥，我们可以对容器的网络进行控制，我们可以使用`network inspect`命令来查看docker()网桥的配置信息：

```
docker network inspect bridge
```

![image-20220702173431530](https://oss.itbaima.cn/internal/markdown/2022/07/02/86XdZUejEuk1P3i.png)

这里分别配置了子网172.17.0.0，和子网掩码255.255.0.0，网关是172.17.0.1，也就是docker()这个虚拟网络设备，所以我们上面创建的容器就是这个子网内分配的地址172.17.0.2了。

#### host网络

当容器连接到此网络后，会共享宿主主机的网络，网络配置也是完全一样的：

```sh
docker run -it --network=host ubuntu-net
```

可以看到网络列表和宿主主主机的列表是一样的，连hostname都是和外面一样的：

![image-20220702170754656](https://oss.itbaima.cn/internal/markdown/2022/07/02/cRAQtIxV4D9byCu.png)

只要宿主主机能连接到互联网，容器内部也是可以正常使用的：

![image-20220702171041631](https://oss.itbaima.cn/internal/markdown/2022/07/02/lVsc1mpihq54Pue.png)

直接使用宿主的网络，传输性能基本没什么亏损，而且我们可以直接去开放端口，不需要做任何桥接：

```sh
apt install -y systemctl nginx
systemctl start nginx
```

安装完Nginx就可以直接访问了。

我们可以根据实际情况，来合理选择三种网络。

### 用户自定义网络

除了前面我们学习到的三种网络之外，我们也可以自定义自己的网络，让容器连接到这个网络。

Docker默认提供了三种网络驱动：bridge，overlay，macvlan，不同驱动对应着不同的网络设备驱动，实现的功能也不一样。

我们可以使用network create来试试看：

```sh
docker network create --driver bridge test
```

这里我们创建了一个桥接网络，名称为test。

可以看到，新增了一个网络设备，这个就是一会负责我们容器网络的网关了，和之前的docker()是一样的：

```sh
docker network inspect test
```

![image-20220702181150667](https://oss.itbaima.cn/internal/markdown/2022/07/02/uLwAD4YC3UFXQt7.png)

这里我们创建一个新的容器，使用和这个网络：

```sh
docker run -it --network=test ubuntu-net
```

![image-20220702181252137](https://oss.itbaima.cn/internal/markdown/2022/07/02/Iy2BwDoZsLMO8gJ.png)

成功得到分配的IP地址，是在这个网络内的，注意不同的网络之间是隔离的，我们可以再创建一个容器试试看：

![image-20220702181808792](https://oss.itbaima.cn/internal/markdown/2022/07/02/b14dflKGMunULQI.png)

可以看到不同的网络是相互隔离的，无法进行通信。

当然我们也为此容器连接到另一个容器所属的网络下：

```sh
docker network connect test 容器ID
```

![image-20220702182050204](https://oss.itbaima.cn/internal/markdown/2022/07/02/WzvhI63ydfeJStA.png)

这样就连接了一个新的网络：

![image-20220702182146049](https://oss.itbaima.cn/internal/markdown/2022/07/02/lxqrz36sVUjNdI4.png)

可以看到容器中新增了一个网络设备连接到我们自己定义的网络中，现在这两个容器在同一个网络下，就可以相互ping了：
![image-20220702182310008](https://oss.itbaima.cn/internal/markdown/2022/07/02/WBlC9PheETO64xq.png)

这里就不介绍另外两种类型的网络了，他们是用于多主机通信的，目前我们只学习单机使用。

### 容器间网络

我们首先先看容器与容器之间的网络通信，实际上刚刚我们已经看到了容器之间的ping了，现在我们创建两个Ubuntu容器：

```sh
docker run -it ubuntu-net
```

先获取其中一个容器的网络信息：

![image-20220702175353454](https://oss.itbaima.cn/internal/markdown/2022/07/02/yTEcg4l2kASBnQu.png)

我们可以直接在另一个容器中ping这个容器：

![image-20230814155603447](https://oss.itbaima.cn/internal/markdown/2023/08/14/go7peBGM6nNI38s.png)

可以看到能够直接ping通，因为这两个容器都是使用的bridge网络，在同一个子网中，所以可以互相访问。

我们可以直接通过容器的ip地址在容器之间进行通信，但是需要保证两个容器在同一个网络之下，虽然这样很方便，但是大部分情况下，容器部署后的ip地址是自动分配的（–ip也很麻烦），我们无法提前得知ip地址，能不能更灵活一些？

我们可以借助Docker提供的DNS服务器，他就像是真的DNS服务器一样，能够对域名进行解析，使用也很简单，我们只需要在容器启动时给个名字就好了，我们可以直接访问这个名称，最后会被解析成对应的idp地址，但是注意：这是在我们用户自定义的网络下生效，默认的网络是不行的：

```sh
docker run -it --name=test01 --network=test ubuntu-net
docker run -it --name=test02 --network=test ubuntu-net
```

同时接入桥接网络(test)之后，两台容器就可以互相ping了。

当然，我们也可以让两个容器同时共享一个网络，注意，这里的共享是直接共享同一个网络设备，两个容器共同使用一个IP地址，只需要在创建时指定：

```sh
docker run -it --name=test01 --network=container:test02 ubuntu-net
```

这里将网络指定为一个容器的网络，这样两个容器使用的就是同一个网络了：

![](https://oss.itbaima.cn/internal/markdown/2022/07/02/Wb6jODxFP3r1mE7.png)

可以看到，两个容器的ip地址和网卡的Mac地址完全一样，他们的网络现在是共享状态，此时在容器访问，localhost即是自己，也是别人。

我们可以在容器中，安装Nginx，然后在容器2访问：

```sh
apt install -y systemctl nginx
# systemctl 是 Linux 系统服务管理工具，它属于 systemd 这个基础系统组件包的一部分。
systemctl start nginx
```

![image-20220702201348722](https://oss.itbaima.cn/internal/markdown/2022/07/02/WTn9OMYmLZJXtBz.png)



成功访问到另一个容器中的Nginx服务器。

### 容器外部网络

前面我们学习了容器之间的网络通信，我们接着来看容器和外部网络的通信。

首先，我们来看容器是如何访问到互联网的，在默认的三种网络下，只有共享模式和桥接模式可以连接到外网，共享模式实际上就是直接使用宿主主机的网络设备连接到互联网，这里我们主要来看一下桥接模式。

通过前面的学习，我们了解到，桥接模式实际上就是创建一个单独的虚拟网络，让容器在这个虚拟网络中，然后通过桥接器来与外界相连，那么数据包是如何从容器内部的网络到达宿主主机然后发送到互联网呢？实际上这个过程中最关键的就是依靠NAT（network address translation）将地址进行转换，再利用宿主主机的ip地址发送数据包出去。

这里我们来补充一下NAT：

> 实际上NAT在我们生活中也是经常见到的，比如我们要访问互联网的某个资源，要和服务器进行通信，那么就需要将数据包发送出去，同时服务器也要将数据包发送回来，我们可以知道服务器的IP地址，也可以直接去连接，因为服务器是暴露在互联网上的：
>
> 但是我们的局域网就不一样了。它仅仅局限于我们家里，比如，我们连接了家里的路由器，可以得到一个IP地址，但是你会发现，这个IP公网是无法直接访问我们的，因为这个IP仅仅是局域网的IP，俗称内网IP，那么服务器是如何将数据包发给我们的呢？
>
> 实际上，这里就接住了NAT，通过它，可以实现将局域网的IP地址映射为公网的IP，而NAT设备一端连接外网，另一端连接内网所有设备，当我们与外界通信时，通过NAT来建立通信。（当然由于公网IP地址有限，素有板材用IP+端口结合使用的形式ANPT）。
>
> 当我们打开浏览器搜索IP,其实这个IP也不是本地的，而是NAT设备的公网地址。
>
> 实际上，我们的家用路由器一般是带有NAT功能，默认开启NAT模式，包括小区也是NAT设备进行转换，这样才保护内网的设备不会直接暴露，只有当我们主动发起连接时，别人才能知道我们。

当然，我们的Docker也是这样的，实际上内网的数据包想要发送到服务器上时，要经过这样一套流程：

![image-20220702232449520](https://oss.itbaima.cn/internal/markdown/2022/07/02/ktEA5O9BrmxXbPz.png)

但还，单纯靠NAT的话，只有我们主动与外界联系时，外界才知道我们，但是我们的容器周末那个可能会部署一些服务器，需要外界来主动连接我们，该如何呢？

我们可以直接在容器配置端口映射：

```sh
docker run -d -p 80:80 nginx
```

这里的`-p`实际上是端口映射配置，端口映射可以将容器需要对外提供服务的端口映射到宿主主机的端口上，这样，当外部访问到宿主主机对应的端口时，会直接转发到容器内部映射的端口了，规则为：`宿主端口:容器端口`。

![image-20220702233420287](https://oss.itbaima.cn/internal/markdown/2022/07/02/WQzEVTwePNaHYgG.png)

一旦监听到了宿主主机的80端口收到了数据包，那么会直接转发给对应的容器，所以配置了端口映射之后，我们才可以从外部真正正常访问到容器内的服务。

我们也可以直接输入`docker ps`查看端口映射情况。

![image-20220702233831651](https://oss.itbaima.cn/internal/markdown/2022/07/02/dyDhNRvQ7Bzixka.png)

## 容器存储管理

前面我们介绍了容器的网络管理，我们现在已经了解了如何去配置容器的网络。还有一个比较重要的部分，就是容器的存储，在这里我们深入了解容器的存储管理。

### 容器的持久化存储

我们知道，在容器被创建之后，实际上我们在容器的操作，是被分层机制保存在最顶层的容器层进行操作的，为了保护下面每一层的镜像不被修改 ，所以才有了这样的头像。但是这也会导致容器在销毁时数据的丢失，当我们销毁容器然后创建一个新的容器时，所有数据全部丢失。

因此，这里需要对数据进行持久化存储，这里要用到数据卷（Data Volume）了。

在开始之前，我们准备一下镜像：

```sh
docker run -it ubuntu
apt update && apt install -y vim
```

然后打包一会要使用的镜像：

```sh
docker commit
```

我们可以让容器将文件保存到宿主主机上，这样就算容器销毁，文件也会在宿主主机上保留，下次创建容器时，依然可以从宿主主机上读取相对应的文件，如何做到呢？只需要在容器启动时指定即可：

```sh
mkdir test
```

我们在用户目录下创建一个新的test目录，然后在里面随便写点：

```sh
vim test/hello.txt
```

接着，我们就可以将宿主主机上的目录或文件挂载到容器的某个目录上：

```sh
docker run -it -v ~/test:/root/test ubuntu-volume
```

这里用到了一个新的参数`-v`，用于指定文件挂载，这里我们将test目录挂在容器的/root/test路径上。

这样，我们就可以直接在容器中访问宿主主机的文件了，当然如果我们对挂在目录中的文件进行编辑，那么相当于编辑宿主主机的数据：

```sh
vim /root/test/test/txt
```

在宿主主机的对应目录下，可以直接访问到我们刚刚创建好的文件。

接着，我们将容器销毁，去查看当容器不存在时，挂载的数据还否保留：

![image-20220703105847329](https://oss.itbaima.cn/internal/markdown/2022/07/03/B5M6Wy8AxIoqJtC.png)

可以看到，即使我们销毁了容器，宿主主机的文件存在，不受影响。

比如我们现在部署一个Nginx服务器来代理我们的前端，就可以将前端页面保存到宿主主机上，然后通挂载的形式让容器中的Nginx访问，这样就算之后Nginx升级需要重新创建，也不会影响前端，我们先讲前端模板上传到服务器：

```sh
scp Downloads/moban5676.zip 192.168.10.10:~/
```

然后在服务器解压：

```sh
unzip moban5676.zip
```

然后我们启动容器：

```sh
docker run -it -v ~/moban5676:/user/share/nginx/html -p 80:80 -d nginx
```

这里，我们将解压出来的目录，挂载到容器中Nginx的默认站点目录，这样Nginx就直接代理了我们存放在宿主主机上的前端页面，当然别忘了把端口映射到宿主主机上，这里我们使用的镜像是官方的nginx镜像。

现在我们进入容器将Nginx启动：

```sh
systemctl start nginx
```

注意：如果这里我们使用`-v`时不指定宿主主机上的目录进行挂载的话，那么就由Docker来自动创建一个目录，并且会将容器中对应路径下的内容拷贝到这个自动创建的目录中，最后挂载到容器中，这就是由Docker管理的数据卷了（docker managed volume）：

```sh
docker run -it -v /root/abc ubuntu-volume
```

这里我们仅仅指定了挂载路径，没有指定宿主主机对应的目录：

![image-20220703112702067](https://oss.itbaima.cn/internal/markdown/2022/07/03/fXCl7IRqKBvYwxj.png)

创建后，root目录下有一个新的abc目录，那么我们查看一下它具体在什么位置：

```sh
docker inspect bold_banzai
```

![image-20220703113507320](https://oss.itbaima.cn/internal/markdown/2022/07/03/zFotAfeBpcRjKWN.png)

可以看到Sorce指的是/var/lib中的某个目录，我们可以进入这个目录创建一个新的文件，记得提升一下权限：

![image-20220703114333446](https://oss.itbaima.cn/internal/markdown/2022/07/03/2bfokiMTmdGZcUE.png)

我们来创一个新的文本文档：

![image-20220703114429831](https://oss.itbaima.cn/internal/markdown/2022/07/03/yi1hSPC3bAndMXm.png)

实际上和我们之前是一样的，也是可以在容器中看到的，当然删除容器之后，数据依然是保留的。当我们不需要使用数据卷时，可以进行删除：

![image-20220703145011638](https://oss.itbaima.cn/internal/markdown/2022/07/03/f8NPDWmhLtvw3SV.png)

当然有时候为了方便，可能并不需要直接挂载一个目录上去，仅仅是从宿主主机传递一些文件到容器中，这里我们可以使用`cp`命令来完成：

![image-20220703115648195](https://oss.itbaima.cn/internal/markdown/2022/07/03/uw7S5PobAUWBtCI.png)

这个命令支持从宿主主机复制文件到容器，或是从容器复制文件到宿主主机，使用方式类似于Linux自带的`cp`命令。

### 容器数据管理

前面，我们通过挂载的形式，将宿主主机上的文件直接挂载到容器中，这样容器就可以直接访问到宿主主机上的文件了，并且在容器删除时也不需要清理宿主主机的文件了。

我们接着来看，如何实现容器与容器之间的数据共享，实际上按照我们之前的思路，我们可以在宿主主机创建一个公共的目录，让这些需要实现共享的容器，都挂载这个公共目录：

```sh
docker run -it ~/test:/root/test ubuntu-volume
```

由于挂载的是宿主主机的目录区域，所以内容在两个容器内都可以访问。

当然，启动新容器时，可以直接引用另一个容器的挂载配置，从而共享同一个宿主目录：

```
docker run -it -v ~/test:/root/test --name=data_test ubuntu-volume
docker run -it --volumes-from data_test ubuntu-volume
```

这里使用`--volumes-from`指定另一个容器。

此时数据卷容器即使被删除，也不会影响到这边，因为这边相当于继承了数据卷容器提供的数据卷，所以本质上还是让两个容器挂载了同样的目录实现数据共享。

虽然通过上面的内容实现了数据传递，但是也不方便，可能某些时候我们仅仅希望容器之间共享，而不希望有宿主主机这个角色直接参与到共享当中，此时我们需要寻找到一种更好的方法：

其实，我们可以将数据完全放到容器中，通过构建一个容器，来直接将容器打包好的数据分享给其他容器，当然，本质上就是一个Docker管理的数据卷，虽然没有完全脱离主机，但是可移植性很高。

我们来编写一个Dockerfile：

```dockerfile
FROM ubuntu
ADD moban5676.tar.gz /usr/share/nginx/html/
VOLUME /usr/share/nginx/html/
```

`ADD`与COPY类似，将文件复制到容器中，但是可以自动对压缩文件解压，后面的`VOLUME`就像`-v`一样：

```sh
cd test
tar -zcvf moban5676.tar.gz *
mv moban5676.tar.gz ..
cd ..
```

接着我们直接构建：

```sh
docker build -t data .
```

![image-20220703153109650](https://oss.itbaima.cn/internal/markdown/2022/07/03/M7jxBUsApKtgzku.png)



现在我们运行一个容器看看：

![image-20220703153343461](https://oss.itbaima.cn/internal/markdown/2022/07/03/SUg32jlwMcY7Btp.png)



可以看到所有的文件都自动解压出来了（除了中文文件名称乱码了之外，不过无关紧要）我们退出容器，可以看到数据卷列表中新增了我们这个容器需要使用的：

![image-20220703153514730](https://oss.itbaima.cn/internal/markdown/2022/07/03/m6VCIbXyMxt3ilT.png)

 

![image-20220703153542739](https://oss.itbaima.cn/internal/markdown/2022/07/03/KyLUic5r6oW4HDx.png)



这个位置实际上就是数据存放在当前主机上的位置了，不过是由Docker进行管理而不是我们自定义的。现在我们就可以创建一个新的容器直接继承了：

```sh
docker run -p 80:80 --volumes-from=data_test -d nginx
```

这样我们就实现了将数据放在容器中进行共享，我们不需要刻意去指定宿主主机的挂载点，而是Docker自行管理，这样就算迁移主机依然可以快速部署。

## 容器资源管理

### 容器控制操作

在开始之前，我们需要补充一些前面没有涉及到的命令。

首先，我们在项目运行时，如何查看输出的日志信息呢：

```sh
docker logs test
```

也可以加入参数`-f`持续打印日志信息。

当容器启动时，我们想要进入容器监控容器的情况时：

```sh
docker attach 容器id/名称
```

运行后，就会切换到容器内的终端，如果想要退出，请使用ctrl+p然后ctrp+q，*不准**使用ctrl+c，这样会终止掉Docker运行的Java程序。

我们也可以使用`exec`命令来在容器中启动一个新的终端或是在容器中执行命令：

```sh
docker exec -it test bash
```

`-it`和`run`命令的操作是一样的，这里执行的话，会创建一个新的终端（当然原本的程序还是正常运行）我们会在一个新的终端中进行交互。

当然也可以仅仅在容器中执行一条命令：

![image-20220701220909626](https://oss.itbaima.cn/internal/markdown/2022/07/01/aVvzjuEM56JmGd7.png)

执行后会在容器中打开一个新的终端执行命令，并输出结果。

前面我们学习了容器的停止错爱做，通过输入`stop`来停止，但是这个操作并会不立刻停止，而是等待容器处理善后，那么怎么才能强制终止容器呢：使用`kill`命令，相当于给进程发送SIGKILL信号，强制结束：

```sh
docker kill test
```

有时候我们只希望容器暂停运行，那么使用`pause`：

```sh
docker pause test
```

暂停容器后，程序也会暂停，无法响应浏览器发送的请求：

恢复运行：

```sh
docker unpause test
```

恢复后，就响应成功了。

### 物理资源管理

对于一个容器，在某些情况下我们可能并不希望它占据所有的系统资源来运行，我们只希望分配一部分资源，比如只分配2G，最大只允许使用2G，此时，我们就需要对容器的资源进行限制。

```sh
docker run -m 内存限制 --memory-swap=内存和交换分区总共的内存限制 镜像名称
```

其中`-m`参数是对容器的物理内存的使用限制，而`--memory-swap`是对内存和交换分区总和的限制，他们默认都是-1，也就是说没有任何限制（如果一开始仅指定-m参数，那么交换内存的限制会与其保持一致，换句话说，内存和交换等于-m的两倍大小）默认情况在跟宿主主机一样，都是2G内存：

现在我们可以将容器的内存限制为200M试试，其中物理内存50M，交换内存50M：

```sh
docker run -it -m 50M --memory-swap=100M nagocoler/springboot-test:1.0
```

可以看到，上来就因为内存不足无法启动了：

![image-20220702104653971](https://oss.itbaima.cn/internal/markdown/2022/07/02/MrBWZKIzgxE94Ck.png)

当然除了对内存的限制之外，我们也可以对CPU资源进行限额，默认情况下，所有的容器都可以平等的使用CPU资源，我们可以调整不同CPU权重（默认1024），来按需分配资源，使用`-c`或者`--cpu-share`：

```sh
docker run -c 1024 ubuntu
docker run -c 512 ubuntu
```

这里的容器的CPU权重比例为6:8，也就是2:1（注意多个容器时才会生效），当CPU资源紧张时会按照此权重分配，如果不紧张，依然有机会使用到全部CPU资源。

这里我们使用一个压力测试工具来验证：

```sh
docker run -c 1024 --name=cpu1024 -it ubuntu
docker run -c 512 --name=cpu512 -it ubuntu
```

接着，我们分别进入容器安转`stress`压力测试工具：

```sh
apt update && pat install -y stress
```

接着，我们在两个容器中启动测试工具，产生4个进程不断计算随机数的平方根：

```sh
stress -c 4
```

接着我们进入top来看看CPU状态（看完之后记得赶紧去kill掉容器，不然CPU拉满很卡的）：

![image-20220702114126128](https://oss.itbaima.cn/internal/markdown/2022/07/02/3dHkMWnq1ZxCyKm.png)

可以看到权重高的容器中，分配到了更多的CPU资源，而权重低的容器中，只分配到一半的CPU资源。

当然我们也可以直接限制容器使用的CPU数量：

```sh
docker run -it --cpuset-cpus=1 ubuntu
```

`--cpuset-cpus`选项可以直接限定在指定的CPU上运行，比如，现在我们的宿主机是2核的CPU，那么就可以分配这两个CPU给Docker使用，限制后，只会使用CPU1的资源了。

如果要分配多个CPU，则使用逗号隔开：

```sh
docker run -it --cpuset-cpus=0,1 ubuntu
```

当然也可以直接使用`--cpus`来限制使用的CPU资源数：

```sh
docker run -it --cpus=1 ubuntu
```

限制后，只能提供一个CPU资源。

最后，我们来看一下对磁盘IO读写性能的限制，我们首先使用`dd`命令来测试磁盘的读写速度：

```sh
dd if=/dev/zero of=/tmp/1G bs=4k count=256000 oflag=direct
```

![image-20220702121839871](https://oss.itbaima.cn/internal/markdown/2022/07/02/1y3O2qbaMsxDFUJ.png)

可以看到当前的读写速度为6.4 MB/s，我们可以通过--device-read/write-bps和--device-read/write-iops参数对其进行限制。

先说一下区别：

- bps：每秒读写的数据量。
- iops：每秒IO的次数。

为了直观，这里我们直接使用BPS作为限制条件：

```sh
docker run -it --device-write-bps=/dev/sda:10MB ubuntu
```

因为容器的文件系统是/dev/sda上的，所以我们就/dev/sda:10MB来限制写入速度。

### 容器监控

最后，我们来看看如何对容器的运行状态进行实时监控，我们希望能够对容器的资源占用情况进行监控，该如何呢？

可以使用`stats`：

```sh
docker stats
```

当然，如果我们限制内存使用的话，也可以清晰看出限制情况：

![image-20220702153704729](https://oss.itbaima.cn/internal/markdown/2022/07/02/CGc6T4iYyN7PD51.png)

使用`top`命令来查看容器中的进程：

```sh
docker top 容器id/名称
```

当然也可以携带一些参数，参数自行了解吧。

但是这样的监控有没有那种网页面板可以实时监控和管理呢：

我们需要单独部署一个Docker网页管理面板应用，一般常见的有：Portainer，这里可以自行去搜搜官网，通过Docker镜像的方式去部署这个应用程序。

首先，我们需要创建一个数据卷供Portainer使用：

```sh
docker volume create portainer_data
```

接着，通过官方命令安装启动：

```
docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```

注意这里需要开放两个端口，一个是8000端口，还有一个是9443端口。

![image-20220702155450772](https://oss.itbaima.cn/internal/markdown/2022/07/02/m71ha8YWsUzPFJ4.png)

OK，开启成功，我们可以直接登录后台面板：https://IP:9443/。

![image-20220702155637366](https://oss.itbaima.cn/internal/markdown/2022/07/02/mukzgvnWZyrxeaM.png)



![image-20220702155703962](https://oss.itbaima.cn/internal/markdown/2022/07/02/E3vy1MKPAr5OJtW.png)

进入后就需要我们进行注册了，这里我们只需输入两次密码即可，默认用户名就是admin，填写完成后，我们就可以开始使用了：

![image-20220702160124676](https://oss.itbaima.cn/internal/markdown/2022/07/02/P1JIKaMCl7guYoz.png)

点击Get Started即可进入到管理页面，我们可以看到目前有一个本地的Docker服务器正在运行：

![image-20220702160328972](https://oss.itbaima.cn/internal/markdown/2022/07/02/OUTrAEmwsNoSG8Y.png)



我们可以点击进入，进行详细地管理，不过唯一缺点就是没中文，挺难受的，也可以使用非官方的汉化版本：https://hub.docker.com/r/6053537/portainer-ce。
