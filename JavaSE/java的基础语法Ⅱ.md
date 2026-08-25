# java的基础语法

---

## 一、隐式转换（从小到大）

1. 取值范围

	```
	byte<short<int<long<float<double
	```

2. 转换规则

	- 取值范围小的，和取值范围大的进行运算，==小的先转换成大的==，再运算。

	+ byte，short，char三种类型在运算时，都==先提升==为int，再进行运算。

## 二、强制转换（从大到小）

```c
double x=(int)5/2;
```

注意：大转小可能会发生栈溢出的情况（1L水倒入100ml的杯子，水会洒出）。

## 三、数组的动态初始化与静态初始化

### 静态初始化

```java
int []arr={1,2,3,4,5};
```

### 动态初始化

```java
int []arr=new int[数组长度];
```

只知道长度，不知道具体值使用动态初始化，反之使用静态初始化。

以下数组内容，如果看不懂，请先阅读面向对象的相关内容

因为数组本身也是一个对象，数组对象也是具有属性的，比如长度：                

```java
public static void main(String[] args) {
    int[] array = new int[10];
    System.out.println("当前数组长度为："+array.length);   //length属性是int类型的值，表示当前数组长度，长度是在一开始创建数组的时候就确定好的
}
```

注意，这个`length`是在一开始就确定的，而且是`final`类型的，不允许进行修改，也就是说数组的长度一旦确定，不能随便进行修改，如果需要使用更大的数组，只能重新创建。

当然，既然是类型，那么肯定也是继承自Object类的：                         

```java
public static void main(String[] args) {
    int[] array = new int[10];
    System.out.println(array.toString());
    System.out.println(array.equals(array));
}
```

但是，很遗憾，除了clone()之外，这些方法并没有被重写，也就是说依然是采用的Object中的默认实现：

![image-20220922220403391](https://oss.itbaima.cn/internal/markdown/2022/09/22/UfTGu9sZheW21jB.png)

所以说通过`toString()`打印出来的结果，好丑，只不过我们可以发现，数组类型的类名很奇怪，是`[`开头的。

因此，如果我们要打印整个数组中所有的元素，得一个一个访问：                      

```java
public static void main(String[] args) {
    int[] array = new int[10];
    for (int i = 0; i < array.length; i++) {
        System.out.print(array[i] + " ");
    }
}
```

有时候为了方便，我们可以使用简化版的for语句`foreach`语法来遍历数组中的每一个元素：                       

```java
public static void main(String[] args) {
    int[] array = new int[10];
    for (int i : array) {    //int i就是每一个数组中的元素，array就是我们要遍历的数组
        System.out.print(i+" ");   //每一轮循环，i都会更新成数组中下一个元素
    }
}
```

## 四、数组的内存布局

- 当开辟数组时，会在堆区建立一个数组，其他的数据类型则建立在栈区。

- 将第二个数组赋值给第一个数组时，第二个数字的指针会指向第一个数组的地址，那么，当修改第二个数字的某个元素时，会将第一个数组的元素也给修改。

## 五、方法的重载

```java
public static void fn(int a)
public static int fn(int a)    
```

不构成重载

```java
public static void fn(int a)
public static int fn(int a,int b)
```

构成重载

```java
public static void fn(int a)
public static int fn(double a)
```

构成重载

如果二者在==不同的方法内，则不构成重载。

```java
public static void fn(int a,double b)
public static void fn(double a,int b)
```

构成重载（不建议这样使用后）

## 六、基本数据类型与引用数据类型

#### 基本数据类型:

包含int，double等，变量中存储的是真实的数据，赋值给其他变量的是真实的地址值。

#### 引用数据类型：

任何将数据开辟到堆区的，都是引用数据类型，自己空间中存储的是地址值。赋值给其他变量的是地址值。

