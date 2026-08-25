# Linux操作系统

操作系统不清楚的自己去查资料，由于大部分人手边都是Windows，所以我们这里装虚拟机来运行。

## 安装Ubuntu系统

官网：https://cn.ubuntu.com/download/server/step1

注意下载的是服务器版本。

### 安装虚拟机

这里我们使用VMware进行安装。

官网下载：https://www.vmware.com/cn/products/workstation-pro/workstation-pro-evaluation.html

安装完成后，会出现一个类似于CMD的命令窗口，而我们就是通过输入命令来操作我们的操作系统。

### 使用SSH远程连接

如果你使用的是云服务器，那么会得到一个公网的ip地址，以及默认的用户名和密码，由于服务器安装的Ubuntu并不是在我们电脑上运行的，那么我们该如何远程操纵呢？

比如，如果我们要远程操作一台电脑，我们完全可以使用向日葵之类的远程连接软件即可，但是Ubuntu上来就是命令行，这种情况下要实现远程连接只能使用ssh终端。

ssh是一种网络安全协议，用于计算机之间的加密登录。如果一台计算机通过ssh协议登录另一台计算机，那么我们就会认为这样的连接是安全的，即使被中途截获，密码也不会泄露。

最早的时候，互联网通信都是明文通信，一旦被截获，内容就暴露无疑。995年，芬兰学者Tatu Ylonen设计了SSH协议，将登录信息全部加密，成为互联网安全的一个基本解决方案，迅速在全世界获得推广，目前已经成为Linux系统的标准配置。

云服务器安装的Ubuntu默认是自带了OpenSSH服务端的，我们可以直接连接。

### 文件系统介绍

在Win下，我们的硬盘被分为多个磁盘驱动器，比如C盘，D盘，E盘等等。

我们一般习惯将软件装到D盘，文件数据存到E盘，C盘存储系统等环境，根据不同的盘符进行划分，并且每个盘都有各自的容量大小。而在Linux中，没有这个概念，所有的文件都位于根目录下。

![img](https://oss.itbaima.cn/internal/markdown/2023/03/06/eWtpKil8khIUE1D.png)

我们可以看到根目录下有很多个文件夹，它们都有各自的划分：

- /bin 可执行二进制文件的目录，如常用的命令ls，tar，mv都实际上是一些小的应用程序。
- /home 普通文件的主目录，对应Win下的C:/User/用户名
- /root root用户的主目录（root用户是具有最高权限的用户）
- /boot 内核文件的引导目录，放置Linux系统启动时的一些文件。
- /sbing 超级用户使用的指令文件。
- /tmp 临时文件目录，一般用户或正在执行的程序临时存放文件的目录，任何人都可以访问。
- /dev 设备文件目录，就是相当于插入U盘后生成的文件夹，我们可以方便的通过IO的方式来操纵外设。
- /lib 共享库，系统使用的函数库目录，程序在执行的过程中，需要调动一些额外的参数需要函数库的协助。
- /usr 第三方程序目录
- /etc 配置程序目录，系统配置文件存放的目录
- /var 可变文件，放置系统执行过程中经常变化的文件
- /opt 用户使用目录，给主机额外安装软件所摆放的目录。

我们可以直接输入命令行来查看目录下的所有文件：

```sh
#只显示文件名称，不显示隐藏文件。
ls
#显示隐藏文件和文件的详细信息。
ll
```

ll的真实“全称”展开来通常是**`ls -alF`**，我们拆开看：

- **`ls`**：核心命令（列出目录内容）。
- **`la`**，*显示所有文件*（包括以`.` 开头的隐藏文件）。
- **`ll`**，*使用长格式显示*（展示权限、大小、修改时间、所属用户等详细信息）。
- **`lf`**，*加上类型标识**（在目录名后面加 `/`，在可执行文件后面加 `*`）。

## 用户和用户组

整个Linux中，除了最基础的定义和概念外，我们要学习的到的就是大量的命令。

Linux系统是一个多用户多任务的分时操作系统，任何一个要使用系统的用户，都必须申请一个账号，然后以这个账号的身份来进入系统。一般的普通用户只能做一些基本的操作，并且只能在自己的目录下（如home/test）中进行文件的创建删除操作。

我们可以看到，当前的状态信息分为三段：

```sh
test@ubuntu-server:~$
```

格式为：用户名@服务器名:当前所处的目录$。

其中~代表用户目录，如果不是用户目录，会显示当前的绝对路径地址。我们可以使用pwd（print working directory）命令来直接查看当前所处的目录。

在Linux中默认存在一个超级用户root，而此用户拥有最高执行权限，它能修改任何的内容，甚至可以直接将系统删除，正常情况下不会用root来进行登录，而是其他的用户身份。

我们可以使用`sudo -s`并输入当前用户的密码切换到root用户，可以看出一些变化：

```sh
test@ubuntu-server:~$
root@ubuntu-server:/home/test#
```

我们发现$ 变成 #，注意，此时的符号用来表示用户等级，并且test变成了root，在此用户下，我们可以随意修改test用户文件夹以外的内容，而test用户下的则无法更改，如果需要退出root用户，直接输入exit即可。

接着，我们来看如何进行用户的管理操作，进行用户管理，包括添加用户和删除用户都需要root权限，但是现在我们是test用户，我们可以在命令前面加入sudo来暂时以管理员的身份来执行此命令，比如我们现在想添加一个新的用户：

```sh
sudo useradd test2
```

删除用户：

```sh
sudo userdel test2
```

同时，我们可以携带一些参数来进行，我们可以在创建用户时来添加：

- -d<登录目录> 　指定用户登录时的起始目录。
- -g<群组> 　指定用户所属的群组。
- -G<群组> 　指定用户所属的附加群组。
- -m 　自动建立用户的登入目录。
- -M 　不要自动建立用户的登入目录。
- -s 指定Shell，一般指定为/bin/bash

如果还想查询更多命令，可以直接man（manual）来查看命令的详细参数列表：

```sh
man usradd
```

比如我们现在想要在创建用户的同时创建用户文件夹，并指定一个shell（如果不指定，那么系统会采用默认配置，可以用但是不好用）

```sh
sudo useradd study -m -s /bin/bash
# -m:--create-home 自动在home目录下创建用户专属目录
# -s，-shell
```

此时执行完可以看到，已经自动在home目录下创建了study文件夹（..表示返回上一级目录，.表示当前目录）：

```she
test@ubuntu-server:~$ ls ..
test
```

用户创建完成后，我们可以为此用户设定密码（如果不指定用户，那么会设置成当前用户）：

```she
sudo passwd test
```

我们可以使用命令来切换用户，并且要输入密码：

```sh
test@ubuntu-server:~$ su - study
Password: 
study@ubuntu-server:~$ 
```

使用exit可以退出到test用户。

输入who可以查看所有的用户（不包括root）的情况，输入whoami只会查到当前用户名。

```sh
test@ubuntu-server:~$ su study
Password: 
study@ubuntu-server:/home/test$ cd ~
study@ubuntu-server:~$ who
test     pts/0        2022-01-24 03:57 (192.168.10.3)
study@ubuntu-server:~$ whoami
study
study@ubuntu-server:~$ 
```

### 用户组

每个用户都有一个用户组，系统可以对一个用户组中的用户进行集中管理。我们可以输入`groups`来查看当前用户的所有用户组：

```sh
test@ubuntu-server:~$ groups
test adm cdrom sudo dip plugdev lxd
```

我们可以输入id来查看用户所属的用户相关信息：

```sh
test@ubuntu-server:~$ id
uid=1000(test) gid=1000(test) groups=1000(test),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lxd)
```

我们可以看到，test用户默认情况下的用户组是以test为名字的主组，并且test用户还有一些处于一些附加组（权限组，通过加入组中可以使用权限命令，比如sudo组），我们发现我们新创建的study没有权限：

```sh
study@ubuntu-server:~$ sudo -s
[sudo] password for study: 
study is not in the sudoers file.  This incident will be reported.
```

现在我们将study用户添加到sudo组中：

```sh
test@ubuntu-server:~$ id study
uid=1001(study) gid=1001(study) groups=1001(study)
```

使用`usermod`命令来对用户参数进行修改，参数大致和useradd大致相同：

```sh
test@ubuntu-server:~$ sudo usermod study -G sudo # 第一个sudo是命令，第二个sudo是群组
test@ubuntu-server:~$ id study
uid=1001(study) gid=1001(study) groups=1001(study),27(sudo)
```

接着切换到study命令就可以使用sudo命令了。

实际上，我们的用户配置信息一般都存储在配置文件中，我们之前说了，配置文件一般都放在etc目录下，而用户和用户组的相关配置文件，存放在`/etc/passwd`和`/etc/group`中，我们可以使用cat（concatenate）来打印到控制台：

```sh
test@ubuntu-server:~$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
```

格式为：`注册名口令:用户标识号组标识号:用户描述用户主目录命令解释程序 `，而我们的密码则存放在`/etc/shadow`中，是以加密形式存储的，并且需要root权限才能查看。

## 常用命令

### 文件操作

#### 权限

文件是最基本的内容，我们可以使用ls来列出目录下的所有文件，参数-a表示包含所有的隐藏文件，l表示列出详细信息：

```sh
test@ubuntu-server:~$ ls -al
total 44
drwxr-xr-x 4 test test 4096 Jan 24 08:55 .
drwxr-xr-x 4 root root 4096 Jan 24 04:24 ..
-rw------- 1 test test 2124 Jan 24 04:29 .bash_history
-rw-r--r-- 1 test test  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 test test 3771 Feb 25  2020 .bashrc
drwx------ 2 test test 4096 Jan 21 15:48 .cache
drwx------ 3 test test 4096 Jan 23 14:49 .config
-rw-r--r-- 1 test test  807 Feb 25  2020 .profile
-rw------- 1 test test   34 Jan 24 04:17 .python_history
-rw-r--r-- 1 test test    0 Jan 21 15:52 .sudo_as_admin_successful
-rw------- 1 test test 7201 Jan 24 08:55 .viminfo
```

那么`drwxr-xr-x`表示什么意思呢：

它表示文件的属性，

- 其中第一个字符表示此文件的类型：`-`表示普通文件，`l`为链接文件，`d`表示目录（文件夹），`c`表示字符设备、`b`表示块设备，还有`p`有名管道、`f`堆栈文件、`s`套接字等，这些一般都是用于进程之间通信使用的。
- 第2-4个字符表示文件拥有者对该文件的权限。
- 第5-7个字符表示文件所属用户组内的用户对该文件的权限。
- 第8-10个字符表示其他用户对该文件的权限。

`r`为读权限，`w`为写权限，`x`为执行权限。

第二栏数字我们可以看到是个数字，它表示文件创建的快捷方式数量，一般只有1表示当前文件，我们可以创建一个快捷方式（链接文件）：

```sh
test@ubuntu-server:~$ ln .bash_logout kk
```

创建后，会生成一个名为kk的文件，我们对此文件的操作相当于直接操作.bash_logout，跟Windows中的快捷方式比较类似，了解一下即可。再次执行`ll`命令，可以看到bash_logout的链接数变成2。

第三栏数据是该文件的拥有者。

第四栏表示文件所属组。

第五栏表示文件大小，字节为单位。

第六栏为该文件最后一次的修改时间。

最后一栏表示文件名称。

..表示上级目录，表示当前目录，最前面有以“.”开头的文件为隐藏文件。可以看到上级目录（也就是 home目录）所有者为root，并且非root用户无法进行写操作，只能执行读操作，而当前目录以及目录下所有文件则属于test用户，test用户可以随意进行修改。

那么，如果我想对文件的属性修改，比如我们对文件的操作权限修改，将写权限关闭，可以使用`chmod`，我们先创建一个test文件，然后使用`touch`命令来创建文件，使用`mkdir`(make directory)命令来创建目录：

```sh
test@ubuntu-server:~$ touch test
test@ubuntu-server:~$ ll test
-rw-rw-r-- 1 test test 0 Jan 24 09:32 test
```

默认权限是可读可写，现在我们修改权限为可读，chmod的使用方法如下：

- chmod        u(g/o/a)      +/-  r（w/x）  文件名

第一个参数，u表示user，g表示group，o表示owner，a表示all。

+表示增加权限，-表示删除权限。

最后我们这里的场景是移除写权限：

```sh
test@ubuntu-server:~$ chmod a-w test
test@ubuntu-server:~$ ll test
-r--r--r-- 1 test test 0 Jan 24 09:32 test
```

我们也可以让数字来代替，比如我要给前两个添加读权限：

约定，r=4，w=2，x=1，那么如果修改权限为`-rw-rw-r--`表示为数字相加，`664`，命令为：

```sh
test@ubuntu-server:~$ chmod 664 test
test@ubuntu-server:~$ ll test
-rw-rw-r-- 1 test test 0 Jan 24 09:32 test
```

如果我们想修改文件的拥有者或者所属组，可以使用`chown`和`chgrp`命令：

```sh
test@ubuntu-server:~$ sudo chown root test 
#把test文件的所有权改给root
test@ubuntu-server:~$ ls -l
total 0
-rw-rw-r-- 1 root test 0 Jan 24 10:43 test
test@ubuntu-server:~$ sudo chgrp root test 
#把test文件的所有组改给root
test@ubuntu-server:~$ ls -l
total 0
-rw-rw-r-- 1 root root 0 Jan 24 10:43 test
```

再次操作，会发现没有权限：

```sh
test@ubuntu-server:~$ chmod 777 test 
chmod: changing permissions of 'test': Operation not permitted
```

#### 复制移动和删除

这里我们先创建一个目录：

```sh
test@ubuntu-server:~$ mkdir study
test@ubuntu-server:~$ cd study
test@ubuntu-server:~/study$
```

首先先看复制，文件的复制使用`cp`，比如我现在想把上一级目录的test文件复制到当前目录中：

```sh
test@ubuntu-server:~/study$ cp ../test test
test@ubuntu-server:~/study$ ls
test
```

那么我们如果想把某复制整个文件夹下的所有文件呢，加入`-r`参数表示将目录中的文件进行递归复制：

```sh
test@ubuntu-server:~/study$ cd ~
test@ubuntu-server:~$ cp -r study study_copied
test@ubuntu-server:~$ ls -l
total 8
drwxrwxr-x 2 test test 4096 Jan 24 10:16 study
drwxrwxr-x 2 test test 4096 Jan 24 10:20 study_copied
-rw-rw-r-- 1 test test    0 Jan 24 09:32 test
```

接着，我们来看移动，使用mv来移动：

```sh
test@ubuntu-server:~$ mkdir study2
test@ubuntu-server:~$ mv test study2
test@ubuntu-server:~$ ls
study  study2  study_copied
test@ubuntu-server:~$ cd study2
test@ubuntu-server:~/study2$ ls
test
```

现在我们想要移动个目录到另一个目录中，比如我们想将study目录移动到study2目录中：

```sh
test@ubuntu-server:~$ mv study study2
test@ubuntu-server:~$ ls
study2  study_copied
test@ubuntu-server:~$ cd study2
test@ubuntu-server:~/study2$ ls
study  test
```

mv也可以将文件进行重命名：

```sh
test@ubuntu-server:~/study2$ ls
study  test
test@ubuntu-server:~/study2$ mv test yyds
test@ubuntu-server:~/study2$ ls
study  yyds
```

使用`rm`进行删除操作，比如现在我们想删除study2目录（注意需要添加-r参数表示递归删除文件夹中的内容）：

```sh
test@ubuntu-server:~$ rm -r study2
test@ubuntu-server:~$ ls
study_copied
```

而最常提到的`rm -rf /*`正是删除根目录下所有的文件（非常危险的操作），-f表示忽略不存在的文件，不进行任何提示，是一个通配符，表示任意文件。这里我们演示一下删除所有以txt结尾的文件：

```sh
test@ubuntu-server:~$ touch 1.txt 2.txt 3.txt
test@ubuntu-server:~$ ls
1.txt  2.txt  3.txt
test@ubuntu-server:~$ rm *.txt
test@ubuntu-server:~$ ls
test@ubuntu-server:~$ 
```

#### 搜索

用`find`来搜索，比如我想搜索/etc目录下名为passwd的文件：

```sh
test@ubuntu-server:~$ sudo find /etc -name passwd
[sudo] password for test: 
/etc/pam.d/passwd
/etc/passwd
```

它还支持通配符，比如搜索以s开头的文件：

```sh
test@ubuntu-server:~$ sudo find /etc -name s*
/etc/subuid
/etc/screenrc
/etc/sensors3.conf
/etc/sysctl.conf
/etc/sudoers
/etc/shadow
/etc/skel
/etc/pam.d/su
/etc/pam.d/sshd
/etc/pam.d/sudo
...
```

### 系统管理

win的任务管理器，我们可以使用`top`命令来打开：

```
top - 10:48:46 up  5:52,  1 user,  load average: 0.00, 0.00, 0.00
Tasks: 191 total,   2 running, 189 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.2 sy,  0.0 ni, 99.8 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   3919.1 total,   2704.2 free,    215.0 used,    999.9 buff/cache
MiB Swap:   3923.0 total,   3923.0 free,      0.0 used.   3521.4 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND                       
  10528 test      20   0    8944   3072   2652 R   0.7   0.1   0:00.07 top                           
   9847 root      20   0       0      0      0 I   0.3   0.0   0:00.87 kworker/0:0-events            
      1 root      20   0  102760  10456   7120 S   0.0   0.3   0:02.02 systemd                       
      2 root      20   0       0      0      0 S   0.0   0.0   0:00.01 kthreadd                      
      3 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_gp                        
      4 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_par_gp                    
      6 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker/0:0H-kblockd          
      8 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 mm_percpu_wq                  
      9 root      20   0       0      0      0 S   0.0   0.0   0:00.15 ksoftirqd/0                   
     10 root      20   0       0      0      0 R   0.0   0.0   0:01.49 rcu_sched                     
     11 root      rt   0       0      0      0 S   0.0   0.0   0:00.24 migration/0                   
     12 root     -51   0       0      0      0 S   0.0   0.0   0:00.00 idle_inject/0                 
     14 root      20   0       0      0      0 S   0.0   0.0   0:00.00 cpuhp/0                       
     15 root      20   0       0      0      0 S   0.0   0.0   0:00.00 cpuhp/1                       
     16 root     -51   0       0      0      0 S   0.0   0.0   0:00.00 idle_inject/1                 
     17 root      rt   0       0      0      0 S   0.0   0.0   0:00.30 migration/1                   
     18 root      20   0       0      0      0 S   0.0   0.0   0:00.07 ksoftirqd/1                   
     20 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kworker/1:0H-kblockd  
```

可以清晰看到当前CPU的使用情况和内存的占用情况。

按下数字键，可以展示当前CPU核心的使用情况：

```
%Cpu0  :  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
%Cpu1  :  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
```

按下f键，可以设置以哪一列进行排序或显示那些参数：

```
Fields Management for window 1:Def, whose current sort field is %MEM
   Navigate with Up/Dn, Right selects for move then <Enter> or Left commits,
   'd' or <Space> toggles display, 's' sets sort.  Use 'q' or <Esc> to end!
```

按下q键退出监控界面。

我们可以直接输入free命令来查看当前系统的内存使用情况：

```
test@ubuntu-server:~$ free -m
              total        used        free      shared  buff/cache   available
Mem:           3919         212        2706           1         999        3523
Swap:          3922           0        3922
```

其中-m表示以M为单位，也可以以-g表示以G为单位，默认是以kB为单位。

最后就是磁盘容量，我们可以使用`lsblk`来查看所有块设备的信息，其中就包括我们的硬盘，光驱等等。

```
test@ubuntu-server:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                       7:0    0 48.9M  1 loop /snap/core18/2127
loop1                       7:1    0 28.1M  1 loop /snap/snapd/12707
loop2                       7:2    0   62M  1 loop /snap/lxd/21032
sr0                        11:0    1 1024M  0 rom  
nvme0n1                   259:0    0   20G  0 disk 
├─nvme0n1p1               259:1    0  512M  0 part /boot/efi
├─nvme0n1p2               259:2    0    1G  0 part /boot
└─nvme0n1p3               259:3    0 18.5G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0 18.5G  0 lvm  /
```

可以看到nvme开头的就是我们的硬盘（这个因人而异，可能你们的是sda，磁盘类型不同名称就不同）可以看到`nvme0n1 `容量20G，并有512M用作存放EFI文件，1G存放启动文件，剩余容量就是存放系统文件和我们的用户目录。

这里需要提到一个挂载的概念：

> 挂载，指的是将设备文件中的顶级目录连接到Linux根目录下的某一目录（最好是空目录），访问此目录就等同于访问设备文件。

比如我们的主硬盘，挂载点被设为`/`根目录，而我们所有保存的文件都会存储在硬盘中，如果你有U盘（最好将U盘的文件格式改为ExFat，可以直接在Windows中进行格式化，然后随便放入一些文件即可）之类的东西，我们可以演示一下对U盘进行挂载：

```sh
test@ubuntu-server:~$ sudo fdisk -l
...
Disk /dev/sda: 60 GiB, 64424509440 bytes, 125829120 sectors
Disk model: USB DISK        
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x4a416279

Device     Boot     Start       End   Sectors  Size Id Type
/dev/sda1  *       614400 125214719 124600320 59.4G  7 HPFS/NTFS/exFAT
/dev/sda2       125214720 125825022    610303  298M  6 FAT16
```

将U盘插入电脑，连接选择到Linux，输入`sudo fdisk -1`命令来查看硬盘的使用情况，我们可以看到有一个USB DISK设备，注意观察一下是不是和自己的U盘容量一致，可以看到设备名称为`/dev/sda1`。

接着，我们将设备挂载到同一目录下：

```sh
test@ubuntu-server:~$ mkdir u-test
test@ubuntu-server:~$ sudo mount /dev/sda1 u-test/
test@ubuntu-server:~$ cd u-test/
test@ubuntu-server:~/u-test$ ls
 CGI
 cn_windows_10_enterprise_ltsc_2019_x64_dvd_9c09ff24.iso
 cn_windows_7_professional_x64_dvd_x15-65791.iso
 cn_windows_8.1_enterprise_with_update_x64_dvd_6050374.iso
 cn_windows_8.1_professional_vl_with_update_x64_dvd_4050293.iso
 cn_windows_server_2019_updated_july_2020_x64_dvd_2c9b67da.iso
'System Volume Information'
 zh-cn_windows_10_consumer_editions_version_21h1_updated_sep_2021_x64_dvd_991b822f.iso
 zh-cn_windows_11_consumer_editions_x64_dvd_904f13e4.iso
```

最后进入到此目录下，就能看到你U盘中的文件了，如果不想使用U盘了，那么直接取消挂载。

```sh
test@ubuntu-server:~/u-test$ cd ..
test@ubuntu-server:~$ sudo umount /dev/sda1
```

最后我们可以通过`df`命令查看当前磁盘使用情况：

```
test@ubuntu-server:~$ df -m
Filesystem                        1M-blocks  Used Available Use% Mounted on
udev                                   1900     0      1900   0% /dev
tmpfs                                   392     2       391   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv     18515  6544     11009  38% /
tmpfs                                  1960     0      1960   0% /dev/shm
tmpfs                                     5     0         5   0% /run/lock
tmpfs                                  1960     0      1960   0% /sys/fs/cgroup
/dev/nvme0n1p2                          976   109       800  12% /boot
/dev/nvme0n1p1                          511     4       508   1% /boot/efi
/dev/loop0                               49    49         0 100% /snap/core18/2127
/dev/loop1                               29    29         0 100% /snap/snapd/12707
/dev/loop2                               62    62         0 100% /snap/lxd/21032
tmpfs                                   392     0       392   0% /run/user/1000
```

输入`ps`可以查看当前运行的一些进程，其实和top有点类似，但是没有监控功能，只能显示当前的。

```
test@ubuntu-server:~$ ps
    PID TTY          TIME CMD
  11438 pts/0    00:00:00 bash
  11453 pts/0    00:00:00 ps
```

添加-ef查看所有的进程：

```
test@ubuntu-server:~$ ps -ef
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 04:55 ?        00:00:02 /sbin/init
root           2       0  0 04:55 ?        00:00:00 [kthreadd]
root           3       2  0 04:55 ?        00:00:00 [rcu_gp]
root           4       2  0 04:55 ?        00:00:00 [rcu_par_gp]
root           6       2  0 04:55 ?        00:00:00 [kworker/0:0H-kblockd]
...
```

我们可以找到对应的进程ID（PID），使用kill命令将其强制终止：

```
test@ubuntu-server:~$ ps
    PID TTY          TIME CMD
  11438 pts/0    00:00:00 bash
  11455 pts/0    00:00:00 ps
test@ubuntu-server:~$ kill -9 11438
Connection to 192.168.10.6 closed.
```

比如我们可以将当前会话的bash给杀死，那么会导致我们的连接直接断开，其中9是一个信号，表示杀死进程：

- 1 (HUP)：重新加载进程。
- 9 (KILL)：杀死一个进程。
- 15 (TERM)：正常停止一个进程。

最后如果我们想要正常关机，只需要输入shutdown即可，系统会创建一个关机计划，并在指定时间关机，或是添加now表示立即关机：

```
test@ubuntu-server:~$ sudo shutdown
[sudo] password for test: 
Shutdown scheduled for Mon 2022-01-24 11:46:18 UTC, use 'shutdown -c' to cancel.
test@ubuntu-server:~$ sudo shutdown now
Connection to 192.168.10.6 closed by remote host.
Connection to 192.168.10.6 closed.
```

### 压缩解压

比较常见的压缩和解压也是一个重点。

这里我们使用`tar`命令来完成文件的压缩和解压操作，在Linux中比较常见的是gzip格式，后缀名一般是.gz，tar的命令参数-c(create)表示对文件进行压缩，创建新的压缩文件，x(extract)先表示解压操作，-z表示对gzip格式进行操作，v(verbose)表示可以在处理过程中输出一些日志信息，-f(file)表示对普通文件进行操作，这里我们创建三个文件并进行打包：

```sh
test@ubuntu-server:~$ tar -zcvf test.tar.gz *.txt
1.txt
2.txt
3.txt
test@ubuntu-server:~$ ls
1.txt  2.txt  3.txt  test.tar.gz
test@ubuntu-server:~$ 
```

接着，我们删除刚刚三个文件，再执行解压缩操作，得到压缩包中的文件：

```sh
test@ubuntu-server:~$ rm *.txt
test@ubuntu-server:~$ ls
test.tar.gz
test@ubuntu-server:~$ tar -zxvf test.tar.gz 
1.txt
2.txt
3.txt
test@ubuntu-server:~$ ls
1.txt  2.txt  3.txt  test.tar.gz
```

同理，我们可以对一个文件夹进行打包：

```sh
test@ubuntu-server:~$ mv *.txt test
test@ubuntu-server:~$ tar -zcvf test.tar.gz test/
test/
test/1.txt
test/2.txt
test/3.txt
test@ubuntu-server:~$ rm -r test
test@ubuntu-server:~$ ls
test.tar.gz 
test@ubuntu-server:~$ tar -zxvf test.tar.gz 
test/
test/1.txt
test/2.txt
test/3.txt
test@ubuntu-server:~$ ls
test  test.tar.gz
test@ubuntu-server:~$ ls test
1.txt  2.txt  3.txt
```

## vim文本编辑器

和Windows记事本一样，Linux中也有文本编辑器，我们这里学习vim文本编辑器的使用。

我们可以直接输入`vim 文件名称`来使用vim编辑器对文本文件进行编辑：

```sh
test@ubuntu-server:~$ vim hello.txt
```

进入编辑器后，我们发现界面变成了：

```
~                                                                                                                                                                                         
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
"hello.txt" [New File]                                                            0,0-1         All
```

这时我们输入指令发现无法操作，因为进入之后默认为命令模式，Vim编辑器默认有三种模式：

![img](https://oss.itbaima.cn/internal/markdown/2023/03/06/b3EQehwpU51TBsa.jpg)

- 命令模式：此模式下可以输入任意指令进行操作，所有的输入都被看做命令输入，而不是文本编辑输入。
- 编辑模式：此模式下输入任何内容都会以文本编辑方式写入文件中，就像win的记事本。
- 末行模式：此模式下用户输入一些复杂指令，会在最后一行进行复杂命令的输入。

在命令模式下，我们可以直接按下`i`，此命令为插入操作，会自动切换为编辑模式，这时：

```
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
~                                                                                                   
-- INSERT --                                                                      1,1           All
```

而这时我们所有的输入内容都可以直接写到文件中，如果我们想回到命令模式，按下`Esc`即可。

除了`i`之外，我们可以按下`a`表示从当前光标所在位置之后继续写，`i`会在光标之前继续写，`o`会直接跳到下一行，而`A`表示在当前行的最后继续写入，`I`表示在当前行的最前面继续写入。

这里我们随便粘贴一段文本信息进去：

```
I was hard on people sometimes, probably harder than I needed to be. 
I remember the time when Reed was six years old, coming home, and I had just fired somebody that day.
And I imagined what it was like for that person to tell his family and his young son that he had lost his job. 
It was hard. 
But　somebody’s got to do it. 
I figured that it was always my job to make sure that the team was excellent, and if I didn’t do it, nobody was going to do it.
You always have to keep pushing to innovate.
Dylan could have sung protest songs forever and probably made a lot of money, but he didn’t. 
He had to move on, and when he did, by going electric in 1965, he alienated a lot of people.
```

在我们编辑完成之后，需要进入到末行模式进行文件的保存并退出，按下`:`进入末行模式，再输入wq即可保存退出。

接着我们来看一些比较常用的命令，首先是命令模式下的光标移动命令：

- ^ 直接调到本行最前面
- $ 直接跳到本行最后面
- gg 直接跳到第一行
- [N]G 跳转到第N行
- [N]方向键向一个方向跳转N个字符

在末行模式下，常用的复杂命令有：

- :set number 开启行号
- :w 保存
- :wq或x 保存并关闭
- :q 关闭
- :q! 强制关闭

我们可以输入`/`或是`?`在末行模式中使用搜索功能，比如我们要搜索单词`it`：

```
/it  
```

接着会在文本中出现高亮，按`n`跳转到下一个搜索结果，?是从后向前搜索，/是从前向后搜索。

它还支持替换功能，但是使用起来稍微比较复杂，语法如下：

```
:[addr]s/源字符串/目的字符串[option]
```

addr表示第几行或是一个范围，option表示操作类型：

- g: globe,表示全局替换
- c: confirm,表示进行确认
- p: 表示替代结果逐行显示(Ctrl + L恢复屏幕)
- i: ignore,不区分大小写

比如我们要将当前行中的`it`全部替换为`he`，那么可以这样写：

```
:s/it/he/g
```

实际上除了以上三种模式外，还有一种模式叫做可视化模式，按下键盘上的`v`即可进入，它能够支持选取一段文本，选取后，我们可以对指定段落的文本内容快速进行复制、剪切、删除、插入等操作，非常方便。在此模式下，我们可以通过上下左右键进行选取，以进入可视化模式时的位置作为基本位置，通过移动另一端来进行选取。

我们可以使用以下命令来对选中区域进行各种操作：

- y 复制选中区域
- d/x 剪切（删除）选中区域
- p 绮樿创
- u 撤销一步

当然，这些命令在命令模式下也可以使用，但是可视化模式下使用更适合一些。
