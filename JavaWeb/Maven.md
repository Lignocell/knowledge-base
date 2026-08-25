# Maven

Maven被翻译为专家，是Apache下的一个纯Java开发的开源项目。基于项目对象模型概念，Maven利用一个中央信息片段能管理一个项目的构建，报告文档等步骤。Maven是一个项目管理工具，可以对Java项目进行构建，依赖管理。

通过Maven：

- 项目的自动构建，包括代码的编译、测试、打包、安装、部署等操作。
- 依赖管理，项目使用到哪些依赖，可以快速完成导入，不需要手动导入jar包。

Maven也需要安装环境，但是IDEA已经自带Maven环境，因此我们不要手动安装。

## Maven项目结构

我们之前使用的都是最原始的Java项目目录格式，其中src目录直接包含我们的包以及对应的代码：

![image-20241118220530127](https://oss.itbaima.cn/internal/markdown/2024/11/18/EaOJqQ9DdxM5lNG.png)

虽然用起来很方便，但是管理以来比较麻烦需要手动导入，因此，我们需要Maven，我们先来看看，一个Maven项目和我们普通的项目有什么区别：![img](https://oss.itbaima.cn/internal/markdown/2024/08/28/iVXseYS6kcAzCnp.jpg)

其中，src目录下存放了我们的源代码和测试代码，分别位于main和test目录下，而test目录和main下又具有java和resources目录，分别用于存放Java源代码和静态资源（如配置文件，图片等），很多JavaWeb项目下还会用到webapp目录。

而下面的pom.xml则是Maven的核心配置，也是整个项目的所有依赖、插件、以及各种配置的集合，它是使用xml格式编写的，一个标准的pom配置长这样：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>come.test</groupId>
    <artifactId>study</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>23</maven.compiler.source>
        <maven.compiler.target>23</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

</project>
```

我们可以看到，Maven的配置文件是以project为根节点，而modelVersion定义了当前模型的版本，一般是4.0.0，我们不做更改。

groudId、artifactId、version这三个元素合在一起，用于唯一区别每个项目，别人如果需要将我们编写的代码作为依赖，那么必须通过这三个元素来定位我们的项目，我们称为一个项目的基本坐标，所有的项目一般都有自己的Maven坐标，因此我们通过Maven导入其他的依赖只需要查询这三个基本坐标就可以了，我们无需下载。

我们可以用[Maven Central: Search](https://central.sonatype.com/search?q=lombok)这个网站来查询我们需要的依赖坐标。

- groudId一般用于指定组名称，命名规则一般与包名一致，比如我们这里使用org.example，一个组下面可以有多个项目。
- artifactId一般用于只当项目在当前组的唯一名称，也就是说在组种用于区分与其他项目的标记。
- version代表项目版本，随着项目的开发和改进，版本号也会不断更新。

properties中一般都是一些变量和选项的配置，这里我们指定了JDK的源码和编译版本为23，同时源代码的编码格式为UTF-8。

接着，我们导入依赖即可：

```xml
<dependencies>
    <dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.18.38</version>
</dependency>
</dependencies>
```

![img](https://oss.itbaima.cn/internal/markdown/2024/11/19/5s2HWYlJgSCOp1q.jpg)

通过流程图我们得知，一个项目依赖一般是存储在中央仓库中，也有可能存储在一些其他的远程仓库（可以自行搭建私服）几乎所有的依赖都被放到了中央仓库中，因此，Maven可以直接从中央仓库中下载大部分的依赖（因此Maven第一次导入依赖是需要联网的，否则无法下载）远程仓库中下载之后，会暂时存储在本地仓库，我们会发现我们本地存在一个`.m2`文件夹，这就是Maven本地仓库文件夹，默认建立在C盘，如果你C盘空间不足，会出现问题。

在下次导入依赖时，如果Maven发现本地仓库中就已经存在某个依赖，那么就不会再去远程仓库下载了。

## Maven依赖作用域

除了三个基本的属性用于定位坐标外，依赖还可以添加如下属性：

- type：依赖的类型，用于项目坐标定义的packaging。大部分情况下，该元素不必声明，其默认值为jar。
- scope：依赖的范围（作用域）。
- optional：标记依赖是否可选。
- exclusions：用于排除传递性依赖（一个项目有可能依赖于其他项目，所有得一起下根项目的依赖（Lombok之类））。

我们先来说scope，它决定了依赖的范围：

- compile：默认的依赖有效范围，如果在定义依赖关系的时候，没有明确指定依赖有效范围的话，则默认为它，此范围表示在编译、运行、测试均有效。
- provided：仅在编译、测试时有效，运行时无效。比如Lombok，我们只在编译阶段使用它，编译完成后，实际上已经转换成对应的代码了，因此Lombok不需要在项目运行时也存在。
- runtime：在运行、测试时有效，编译时无效。比如JDBC，我们使用的始终时JDK这种提供的接口，不需要直接使用特定驱动种的类或者方法，因此只需要在运行时包含即可。
- test：只在测试时有效。比如JUnit，我们一般只会在测试阶段使用JUnit，而项目运行时不要。

我们发现，Maven还给我们提供了一个resource目标，我们可以将一些静态资源，比如配置文件，放到这个文件夹种，项目在打包时会将资源文件夹种文件一起打包的jar中。

## Maven安装、可选和拆除

前面我们介绍了依赖的导入方式和各种作用域，现在我们来看看如何在其他项目中导入我们自己编写的Maven项目作为依赖使用。这里我们创建一个用于测试的简单项目：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.test</groupId>
    <artifactId>TestMaven</artifactId>
    <version>1.0-SNAPSHOT</version>

    ...

</project>
```

```java
public class TestUtils {
    public static void test() {
        System.out.println("抛开事实不谈，你们就没有一点错吗？");
    }
}
```

接着我们点击右上角的Maven选项，然后执行`install`或直接在命令行中输入`mvn install`来安装我们自己的项目到本地Maven仓库中。

接着我们就可以在需要使用此项目作为依赖的其他项目中使用它了，只需要填写和这边一样的坐标：

```xml
<dependency>
    <groupId>com.test</groupId>
    <artifactId>TestMaven</artifactId>
    <version>1.0-SNAPSHOT</version>
</dependency>
```

接着我们就可以在项目中直接使用了：

```java
public static void main(String[] args) {
    TestUtils.test();
}
```

![image-20241119105655739](https://oss.itbaima.cn/internal/markdown/2024/11/19/vdz8KjP2JBHayok.png)

注意：如果我们的旧项目中导入了一些其他的依赖，那么此依赖时会被一起传递的。

再某些情况下，可能我们不希望某些依赖直接被项目连带导入，因此，当项目中的某些依赖不希望被使用时，我们可以添加optional标签表示此依赖是可选的，默认再导入依赖是，不会导入可选的依赖：

```xml
<optional>true</optional>
```

现在，如果我们在导入依赖的时候，依赖本身项目没有做好可选设置，导致我们自己的项目可能会存在多余的依赖，因此我们需要手动剔除不需要的依赖，只需要添加exclusion标签即可：

```xml
<dependency>
    <groupId>com.test</groupId>
    <artifactId>TestMaven</artifactId>
    <version>1.1-SNAPSHOT</version>
    <exclusions>
        <exclusion>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
          	<!--  可以不指定版本号，只需要组名和项目名称  -->
        </exclusion>
    </exclusions>
</dependency>
```

此时我们通过这种方式手动排除了Test项目中包含的MyBatis依赖，这样项目中就不会包含此依赖了。

## Maven继承和多模块

一个Maven项目可以继承另一个Maven项目，比如多个子项目都需要父项目的依赖，我们就可以使用继承关系来快速配置。

要创建子项目很简单，我们只需要右键左侧栏，新建模块，来创建一个子项目：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>come.test</groupId>
        <artifactId>study</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>hello-user</artifactId>

    <properties>
        <maven.compiler.source>23</maven.compiler.source>
        <maven.compiler.target>23</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

</project>
```

我们可以看到，IDEA给我们提供了一个parent节点，表示子项目，子项目直接继承父项目的groupId，子项目会继承父项目的所有依赖。

我们可以让父项目统一管理素有依赖，包括版本号等等，子项目可以选取需要的作为依赖，我们可以将dependencies全部放入dependencyManagement节点，这样父项目就完全作为依赖统一管理：

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.22</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.8.1</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.27</version>
        </dependency>
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
            <version>3.5.7</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

我们发现，子项目的依赖失效了，因为现在父项目没有依赖，而是将所有的依赖进行集中管理，子项目需要什么再拿什么即可，同时子项目无需指定版本，所有的版本全部由父项目决定，子项目只需要使用即可：

```xml
<dependencies>
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <scope>provided</scope>
    </dependency>
</dependencies>
```

当然，父项目如果还存在dependencies节点的话，里面的内依赖依然是直接继承：

```xml
<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.8.1</version>
        <scope>test</scope>
    </dependency>
</dependencies>

<dependencyManagement>
    <dependencies>
      ...
```

## Maven测试和打包

我们可以看到IDEA右上角Maven板块中，每个Maven项目都有一些功能，比如：

- clean：执行后会清理整个target文件夹，在之后编写springboot项目可以解决一些缓存没更新的问题。
- validate：可以验证项目的可用性。
- complite：可以将项目编译成 class文件。
- install：可以将当前项目安装到本地仓库，以供其他项目导入作为依赖使用。
- verify：按顺序执行每个上述功能。

所有命令在执行完成后会出现BUILD SUCCESS，否则就是出现了错误。

除了上述命令以外，test命令，一键测试所有位于test目录下测试案例，但是默认test命令有以下要求：

- 测试类名称必须以Test结尾，比如MainTest。
- 测试方法必须标注@Test或者其他测试案例注解。

我们接着来看package命令，它用于将我们的项目打包成jar文件，以供其他项目作为依赖导入，或是作为一个可执行的Java应用程序执行。

注意：package命令打包之前会自动执行一次test命令，来保证项目正常运行，如果测试出现问题，打包无法完成，我们也可以手动跳过，输入`mvn package -Dmaven.test.skip=true`来跳过测试进行打包。

当然，以上方式存在一定的问题，比如这里我们并没有包含项目中用到的一些其他依赖，比如我们需要打包一个可执行文件，那么我们不仅需要将自己编写的打包到Jar中，同时还需要将依赖一并打包到Jar中，因为我么们使用了别人给我们提供的依赖，自然也要运行别人的代码，我们呢还需要使用另一个插件实现一起打包：

```xml
<plugin>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>3.1.0</version>
    <configuration>
        <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
        </descriptorRefs>
        <archive>
            <manifest>
                <addClasspath>true</addClasspath>
                <mainClass>com.test.Main</mainClass>
            </manifest>
        </archive>
    </configuration>
    <executions>
        <execution>
            <id>make-assembly</id>
            <phase>package</phase>
            <goals>
                <goal>single</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

导入插件后，我们再次打包，此时会出现两个文件，一个是之前正常打包的jar文件，另一个就是包含了所有依赖以及配置了主类的jar文件。

我们只需要执行`java -jar`命令即可运行打包好的Java程序：

![image-20241119162858366](https://oss.itbaima.cn/internal/markdown/2024/11/19/hxT1lJDQgBGOSHf.png)



我们之前还讲解了多模块项目，那么多模块下父项目存在一个`packing`打包类型标签，所有的父级项目的`packing`都为`pom`，`packing`默认是`jar`类型，如果不作配置，maven会将该项目打成jar包：

```xml
<packaging>pom</packaging>
```

作为父级项目，还有一个重要的属性，那就是modules，通过modules标签将项目的所有子项目引用进来，在`build`父级项目时，会根据子模块的相互依赖关系整理一个`build`顺序，然后依次`build`直到所有任务都完成。
