# I/O

所谓IO，其实就是输入和输出。
首先，我们先来学习读取文件。
## 文件字节流
第一步，我们先来学习`FileInputStream`，我们可以通过它来获取文件的输入流：
```java
public static void main(String[] args){
    try{  //注意，对于IO的使用很有可能会引起异常，所以我们将其放入trycatch中，以便处理
        FileInputStream fis=new FileInputStream("路径");
        //路径支持相对路径和绝对路径    }catch(FileNotFoundException e){
        e.printStackTrace();
    }
}
```

相对路径是在当前运行目录下的路径（即哪个目录运行java程序）下寻找文件，而绝对路径是在根目录下寻找文件。
路径分割符为`/` `\\`，在windows下
```
C://Users/lbw/nb  //这个是绝对路径test/test  //这个是相对路径```

在使用了流之后，必须要关闭这个流来完成对于流的释放，否则资源会被占用。
```java
public static void main(String[] args){
    FileInputStream fis=null;  //将定义放在外部，将关闭流的操作放在final中。    try{
        fis=new FileInputException("路径");
    }catch(FileNotFoundException e){
        e.printStackTrace();
    }final{  //建议在final中执行，因为关闭流的操作必须执行
        try{
            if(fis!=null) fis.close();
        }catch(IOException e){
            e.printStackTrace();
        }
    }
}
```

虽然如此，但事实上太过于繁琐，因此在Java1.8中新增加了一种语法来简化这种写法：

```java
public static void main(String[] args){
    try(FileInputStream fis=new FileInputStream("路径")){  //直接在try()中定义要在之后释放的资源        
    }catch(IOException e){  //这里变成IOException是因为调用和close()要用到，而FileNotFoundException()是IOException的子类        e.printStackTrace();
    }
    //无需再编写finally语句块，因为在最后自动帮我们调用了close()
}
```

现在，我们拿到了文件的输入流，那么我们如何读取文件里的内容呢？我们可以使用`read`方法：
```java
public static void main(String[] args){
    try(FileInputStream fis=new FileInputStream("test.txt")){
        System.out.println((char)fis.read());  //读取一个字节的数据，英文占一个字节，中文占两个字节        System.out.println(fis.read());  //如果内容已经被读完了，那么读取后会返回-1
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

使用read可以直接读取一个字节的数据，注意，流的内容是有限的，读一个少一个；可以用while循环来完成：

```java
public static void main(String[] args){
    //test.txt:abcd
    try(FileInputStream fis=new FileInputStream("test.txt")){
        int temp;
        while((temp=fis.read())!=-1){
            System.out.println((char)temp);
        }
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

使用`available`方法可以查看当前可读的剩余字节数量：（返回值是读取的字节数）
```java
public static void main(String[] args){
    try(FileInputStream fis=new FileInputStream("test.txt")){
        System.out.println(fis.available);
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

使用read方法读取时一个一个读取效率太低了，是否能够一次性全部读取：

```java
public static void main(String[] args){
    //test.txt:abcd
    try(FileInputStream fis=new FileInputStream("test.txt")){
        byte[]bb=new byte[fis.available()]; //提前制作一个数组，准备好合适的容量
        System.out.println(fis.read(bb));  //一次性读取全部内容（返回值时读取的字节数）        System.out.println(new String(bb));  //通过String的构造方法得到字符串
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

也可以控制读取的数量:

```java
System.out.println(fis.read(bb,1,2));  //第二个参数是从给定数组的哪个位置存放内容，第三个参数是读取流中的字节数```

注意：一次性读取与单个读取一样，当没有数据可读时，返回-1.

通过`skip()`可以跳过指定数量的字节：

```java
public static void main(String[] args){
    //test.txt:abcd
    try(FileInputStream fis=new FileInputStream("test.txt")){
        System.out.println(fis.skip(1));
        System.out.println((char)fis.read());  //跳过了一个字节    }catch(IOException e){
        e.printStackTrace();
    }
}
```

注意：FileInputStream是不支持`reset()`的，虽然有这个方法，但是这里先不提及。
输入流讲完了，接下来，我们来讲解一下输出流。
```java
public static void main(String[] args){
    //输出流也需要在最后使用close()
    try(FileOutputStream fos=new FileOutputStream("test.txt")){
        //注意：若没有这个文件，会直接创建
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

输出流没有`read()`，只有`write()`，变成了我们向文件里写内容，用法不变：
```java
public static void main(String[] args){
    try(FileOutputStream fos=new FileOutputStream("test.txt")){
        fos.write("C");  //同read一样，直接向文件中写入内容
        fos.write("lbwnb".getBytes());  //将字符串转为byte数组然后写入文件
        fos.write("lbwnb".getBytes(),0,1);  //同上（输入流）        fos.flush();  //由于内部的缓存机制，write不会立刻写入所有数据，如果想要立刻看到效果，那么可以使用flush进行刷新来保证已经全部写入    }catch(IOException e){
        e.printStackTrace();
    }
}
```

如果我们想要在原文件加东西呢？这里可以调用另一个构造方法：

```java
public static void main(String[] args){
    try(FileOutputStream fos=new FileOutputStream("test.txt",true)){  //true表示开启追加模式        fos.write("lb".getBytes());  //现在就是追加东西，而不是覆盖        fos.flush();
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

利用输入流和输出流，我们可以轻松实现文件拷贝了：

```java
public static void main(String[] args){
    try(FileInputStream fis=new FileInputStream("input.txt");
       FileOutputStream fos=new FileOutputStream("output.txt")){  //可以写入多个，用分号隔开
        byte[] bb=new byte[10];  //使用长度为10的byte做传输媒介        int temp;  //存储本地读取的字节数
        while(temp=fis.read("input.text")!=-1){
            fos.write(bb,0,temp);
        }
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

## 文件字符流
字符流不同于字节，字符流只适用于以一个具体的字符进行读取，因此，它只适合读取纯文本的文件，其他类型的文件可能不适用：
```java
public static void main(String[] args){
    try(FileReader fr=new FileReader("test.txt")){
        fr.skip(1);  //现在跳过的是一个字符，而不是一个字节        System.out.println((char)fr.read());  //现在读取的是字符，因此，中文也可以读到    }catch(IOException e){
        e.printStackTrace();
    }
}
```

同理，字符串类型只支持`char[]`类型存储：
```java
public static void main(String[] args){
    try(FileReader fr=new FileReader("test.txt")){
        char[] str=new char[10];
        fr.read(str);
        System.out.println(str);
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

既然有Reader了，那么肯定有Writer：
```java
public static void main(String[] args){
    try(FileWriter fw=new FileWriter("test.txt")){
        fw.getEncoding();  //获取编码（比如说UTF-8）等信息        fw.write('a');        fw.append('b');  //和write一样        fw.flush();
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

我们发现不仅有`write()`方法，还有一个`append()`方法，但是实际上他们效果是一样的，看源码：
```java
public Writer append(char c) throws IOException {
    write(c);
    return this;
}
```

append支持像StringBuilder那样的链式调用，返回的是Writer对象本身。
接下来，我们来学习一下File类：

它是专门用于表示一个文件或者一个文件夹，它不是文件本身，只是代表这个文件：

```java
public static void main(String[] args){
    File ff=new File("tes.txt");  
    System.out.println(ff.exit());  //文件是否存在
    System.out.println(ff.length());  //获取文件大小
    System.out.println(ff.isDirectory());  //是否为一个文件夹
    System.out.println(ff.canRead());  //是否可读
    System.out.println(ff.canWrite);  //是否可写
    System.out.println(ff.canExecute());  //是否可执行}
```

通过File，我们能够快速获取文件下的所有信息，还可以获取文件夹下的所有文件：

```java
File ff=new File("/");
System.out.println(Arrays.toString(ff.list()));  //快速获取文件夹下的所有文件列表for(File f:ff.listFiles()){  //所有子文件的File对象
   System.out.println(f.getAbsoluatePath());  //获取文件的绝对路径}
```

如果我们需要读取某个文件的内容，我们可以直接将File作为参数传入字符流或者字节流：
```java
File ff=new File("test.txt");
try(FileInputStream fis=new FileInputStream(ff)){
    System.out.println(fis.available());
}catch(IOException e){
    e.printStackTrace();
}
```

## 缓冲流
使用普通的文件流虽然快捷，但是每次都需要从外部的I/O设备去读取数据，速度不快，此时我们可以使用缓存流来进行传输。
所谓缓冲流，就是先将一部分数据提前存入缓冲区，下次读取时，如果缓冲区存在该数据，无需请求外部设备，同理，当向外部设备写入数据时，也是由缓冲区先进行处理：![image-20221004125755217](https://oss.itbaima.cn/internal/markdown/2022/10/04/S8O61JP2lqKTzjd.png)

想要创建一个缓冲字节流，只需要将原本的流作为构造函数传入BufferedInputStream即可：
```java
public static void main(String[] args){
    try(BufferedInputStream bis=new BufferedInputStream(new FileInputStream("test.txt"))){
        System.out.println((char)bis.read());  //操作和原来的流一样    }catch(IOException e){
        e.printStackTrace();
    }
}
```

实际上，进行I/O处理时，并不是BufferedInputStream，而是FileInputStream，而BufferedInputStream虽然有同样的方法，但实际上先是做了一些处理，才调用了FileInputStream来进行IO操作，这种方式被称为**装饰者模式*，在学习设计模式时会具体讲解；我们可以观察一下它的close源码：
```java
public void close() throws IOException {
    byte[] buffer;
    while ( (buffer = buf) != null) {
        if (bufUpdater.compareAndSet(this, buffer, null)) {  //CAS无锁算法，并发会用到，暂时不需要了            InputStream input = in;
            in = null;
            if (input != null)
                input.close();
            return;
        }
        // Else retry in case a new buf was CASed in fill()
    }
}
```

实际上这种模式是父类FilterInputStream提供的规范，后面我们还会讲到更多FilterInputStream的子类。
我们可以发现在BufferedInputStream中还存在一个专门用于缓存的数组：                   

```java
/**
 * The internal buffer array where the data is stored. When necessary,
 * it may be replaced by another array of
 * a different size.
 */
protected volatile byte buf[];
```

I/O操作一般不能重复读取内容，而缓冲流提供了缓冲机制，使得一部分内容可以被暂时保存，BufferedInputStream支持`reset()`和`mark()`操作，首先我们来看看`mark()`方法的介绍：                      

```java
/**
 * Marks the current position in this input stream. A subsequent
 * call to the <code>reset</code> method repositions this stream at
 * the last marked position so that subsequent reads re-read the same bytes.
 * <p>
 * The <code>readlimit</code> argument tells this input stream to
 * allow that many bytes to be read before the mark position gets
 * invalidated.
 * <p>
 * This method simply performs <code>in.mark(readlimit)</code>.
 *
 * @param   readlimit   the maximum limit of bytes that can be read before
 *                      the mark position becomes invalid.
 * @see     java.io.FilterInputStream#in
 * @see     java.io.FilterInputStream#reset()
 */
public synchronized void mark(int readlimit) {
    in.mark(readlimit);
}
```

先存放如mark，相当于在当前字节做了一个标记，当调用reset之后，会使得当前读取的位置返回mark调用时的位置。
```java
public static void main(String[] args) {
    try (BufferedInputStream bufferedInputStream = new BufferedInputStream(new FileInputStream("test.txt"))){
        bufferedInputStream.mark(0);   
        System.out.println((char) bufferedInputStream.read());
        System.out.println((char) bufferedInputStream.read());
        bufferedInputStream.reset();   //回到mark时的位置
        System.out.println((char) bufferedInputStream.read());
        System.out.println((char) bufferedInputStream.read());
    }catch (IOException e) {
        e.printStackTrace();
    }
}
```

而`mark()`的括号中，是readlimit，即对于读取长度的限制，比如说，当readlimit为2时，那么只能向后读取两个字节，超过以后，标记自动失效。
当然，我们也可以限制缓冲区的大小，当mark中的数超出缓冲区的大小，同样也会失效：
```java
try (BufferedInputStream bufferedInputStream = new BufferedInputStream(new FileInputStream("test.txt")),3)  //限制缓冲区为3
```

接下来，我们来看`BufferedOutputStream`，原理相似：

```java
public static void main(String[] args) {
    try (BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream("output.txt"))){
        bos.write("lbwnb".getBytes());
        bos.flush();
    }catch (IOException e) {
        e.printStackTrace();
    }
}
```

既然有缓冲字节流，那么肯定有缓冲字符流，与缓冲字节流相似：
```java
public static void mian(String[] args){
    try(BufferedReader br=new BufferedReader(new FileReader("test.txt"))){
        System.out.println((char)br.read());
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

内部同样也包含一个缓冲数据

```java
private char cb[];
```

相比较FileReader，它支持按行获取：
```java
public static void main(String[] args) {
    try (BufferedReader br = new BufferedReader(new FileReader("test.txt"))){
        System.out.println(br.readLine());   //按行读取
    }catch (IOException e) {
        e.printStackTrace();
    }
}
```

读取后直接得到一个字符串，当然，它还能把每一行内容依次转换为集合类提到的Stream流：                        

```java
public static void main(String[] args) {
    try (BufferedReader reader = new BufferedReader(new FileReader("test.txt"))){
        reader
                .lines()
                .limit(2)
                .distinct()
                .sorted()
                .forEach(System.out::println);
    }catch (IOException e) {
        e.printStackTrace();
    }
}
```

它同样也支持`mark()`和`reset()`操作：             

```java
public static void main(String[] args) {
    try (BufferedReader reader = new BufferedReader(new FileReader("test.txt"))){
        reader.mark(1);
        System.out.println((char) reader.read());
        reader.reset();
        System.out.println((char) reader.read());
    }catch (IOException e) {
        e.printStackTrace();
    }
}
```

BufferedReader处理纯文本文件时就更加方便了，BufferedWriter在处理时也同样方便：           

```java
public static void main(String[] args) {
    try (BufferedWriter reader = new BufferedWriter(new FileWriter("output.txt"))){
        reader.newLine();   //使用newLine进行换行
        reader.write("汉堡做滴彳亍不彳亍);   //可以直接写入一个字符串
      	reader.flush();   //清空缓冲区    }catch (IOException e) {
        e.printStackTrace();
    }
}
```

合理使用缓冲流，可以大大提高我们程序的运行效率，只不过现在初学阶段，很少会有机会接触到实际的应用场景。
## 转换流
有时我们会遇到一个麻烦的问题，我们在读取时是一个个字符串或者字符，但是在向OutputStream中输出时，它只支持byte类型，进行数据转换会很麻烦，那么我们该如何解决这个问题：

```java
public static void main(String[] args){
    try(OutputStreamWriter osw=new OutputStreamWriter(new FileOutputStream("test.txt"))){
        osw.write("lbwnb");
    }catch(IOException e){
        e.printStackTrace();
    }
}
```

同样的，我们现在只拿到了一个InputStream，但是我们希望能够按字符的方式读取，我们就可以使用InputStreamReader来帮助我们实现                

```java
public static void main(String[] args) {
    try(InputStreamReader reader = new InputStreamReader(new FileInputStream("test.txt"))){  //虽然给定的是FileInputStream，但是现在支持以Reader的方式进行读取        System.out.println((char) reader.read());
    }catch (IOException e){
        e.printStackTrace();
    }
}
```

InputStreamReader和OutputStreamWriter本质也是Reader和Writer，因此可以直接放入BufferedReader来实现更加方便的操作。
## 打印流
- 打印流其实我们一开始就在使用`System.out`就是一个打印流，PrintStream也继承自FilterOutputStream(同缓冲流一样
- 它存在自动刷新机制，也就是说在导入数据和自动调用flush()。- PrintStream也永远不会抛出异常，而是使用内部检查机制`checkError()`方法进行错误检查。- 最方便的是，他能以格式化任意形式，将数据以字符串的形式写入到输出流。
```java
public final static PrintStream out = null;
```

可以看到`System.out`也是PrintStream，不过默认是向控制台打印，我们也可以让它向文件中打印：         

```java
public static void main(String[] args) {
    try(PrintStream stream = new PrintStream(new FileOutputStream("test.txt"))){
        stream.println("lbwnb");   //其实System.out就是一个PrintStream
    }catch (IOException e){
        e.printStackTrace();
    }
}
```

我们平时使用的`println`方法就是PrintStream中的方法，它会直接打印基本数据类型或是调用对象的`toString()`方法得到一个字符串，并将字符串转换为字符，放入缓冲区再经过转换流输出到给定的输出流上。
![img](https://oss.itbaima.cn/internal/markdown/2022/10/04/w8RKJxLm6Ik5usn.png)

因此实际上内部还包含这两个内容：                    

```java
/**
 * Track both the text- and character-output streams, so that their buffers
 * can be flushed without flushing the entire stream.
 */
private BufferedWriter textOut;
private OutputStreamWriter charOut;
```

与此相同的还有一个PrintWriter，不过他们的功能基本一致，PrintWriter的构造方法可以接受一个Writer作为参数，这里就不再做过多阐述了。
而我们之前使用的Scanner，使用的是系统提供的输入流：               

```java
public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);   //系统输入流，默认是接收控制台输入
}
```

我们也可以使用Scanner来扫描其他的输入流：

```java
public static void main(String[] args) throws FileNotFoundException {
    Scanner scanner = new Scanner(new FileInputStream("秘制小汉堡.txt"));  //将文件内容作为输入流进行扫描
}
```

## 数据流
数据流DataInputStream同样是FilterInputStream的子类，同样采用装饰者模式，最大的不同是它支持基本数据类型的直接读取：

```java
public static void main(String[] args) {
    try (DataInputStream dis= new DataInputStream(new FileInputStream("test.txt"))){
        System.out.println(dis.readBoolean());   //直接将数据读取为任意基本数据类型
    }catch (IOException e) {
        e.printStackTrace();
    }
}
```

用于写入基本数据类型：                      

```java
public static void main(String[] args) {
    try (DataOutputStream dos = new DataOutputStream(new FileOutputStream("output.txt"))){
        dos.writeBoolean(false);
    }catch (IOException e) {
        e.printStackTrace();
    }
}
```

注意，写入的是二进制数据，并不是写入的字符串，使用DataInputStream可以读取，一般他们是配合一起使用的。
## 对象流
既然基本数据类型能够读取和写入基本数据类型，那么能否将对象也支持呢？ObjectOutputStream不仅支持基本数据类型，通过对对象的序列化操作，以某种格式保存对象，来支持对象类型的IO，注意：它不是继承自FilterInputStream的。                       

```java
public static void main(String[] args) {
    try (ObjectOutputStream outputStream = new ObjectOutputStream(new FileOutputStream("output.txt"));
         ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream("output.txt"))){
        People people = new People("lbw");
        outputStream.writeObject(people);
      	outputStream.flush();
        people = (People) inputStream.readObject();
        System.out.println(people.name);
    }catch (IOException | ClassNotFoundException e) {
        e.printStackTrace();
    }
}

static class People implements Serializable{   //必须实现Serializable接口才能被序列化
    String name;

    public People(String name){
        this.name = name;
    }
}
```

在我们后续的操作中，有可能会使得这个类的一些结构发生变化，而原来保存的数据只适用于之前版本的这个类，因此我们需要一种方法来区分类的不同版本：            

```java
static class People implements Serializable{
    private static final long serialVersionUID = 123456;   //在序列化时，会被自动添加这个属性，它代表当前类的版本，我们也可以手动指定版本。
    String name;

    public People(String name){
        this.name = name;
    }
}
```

当发生版本不匹配时，会无法反序列化为对象：                    

```java
java.io.InvalidClassException: com.test.Main$People; local class incompatible: stream classdesc serialVersionUID = 123456, local class serialVersionUID = 1234567
	at java.io.ObjectStreamClass.initNonProxy(ObjectStreamClass.java:699)
	at java.io.ObjectInputStream.readNonProxyDesc(ObjectInputStream.java:2003)
	at java.io.ObjectInputStream.readClassDesc(ObjectInputStream.java:1850)
	at java.io.ObjectInputStream.readOrdinaryObject(ObjectInputStream.java:2160)
	at java.io.ObjectInputStream.readObject0(ObjectInputStream.java:1667)
	at java.io.ObjectInputStream.readObject(ObjectInputStream.java:503)
	at java.io.ObjectInputStream.readObject(ObjectInputStream.java:461)
	at com.test.Main.main(Main.java:27)
```

如果我们不希望某些属性参与到序列化中进行保存，我们可以添加`transient`关键字：                   

```java
public static void main(String[] args) {
    try (ObjectOutputStream outputStream = new ObjectOutputStream(new FileOutputStream("output.txt"));
         ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream("output.txt"))){
        People people = new People("lbw");
        outputStream.writeObject(people);
        outputStream.flush();
        people = (People) inputStream.readObject();
        System.out.println(people.name);  //虽然能得到对象，但是name属性并没有保存，因此为null
    }catch (IOException | ClassNotFoundException e) {
        e.printStackTrace();
    }
}

static class People implements Serializable{
    private static final long serialVersionUID = 1234567;

    transient String name;

    public People(String name){
        this.name = name;
    }
}
```

其实我们可以看到，在一些JDK内部的源码中，也存在大量的transient关键字，使得某些属性不参与序列化，取消这些不必要保存的属性，可以节省数据空间占用以及减少序列化时间。

