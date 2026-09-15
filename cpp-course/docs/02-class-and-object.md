# 02 类与对象

## 课程目标

1. 理解数据抽象与封装，能用 class 隐藏实现、暴露接口
2. 掌握类的声明/定义、作用域、访问控制
3. 掌握默认成员函数、构造/析构/拷贝构造、this、初始化列表、explicit
4. 理解浅拷贝与深拷贝，正确处理含指针成员的类
5. 掌握静态成员、友元、类中 const / mutable
6. 掌握常用运算符重载（成员 vs 全局/友元）及必须作为成员的运算符

> 标准 I/O 详解、`string` API、`new`/`delete` 专章见后续文档；本讲仅在示例中必要时使用。

---

## 一、数据抽象与封装

**抽象**：抽出共同特征，对外只暴露必要接口。  
**封装**：把数据与操作绑成整体，并通过访问控制限制外部直接碰内部状态。

### 1.1 Circle 示例

```cpp
class Circle {
private:
    double radius;
public:
    Circle(double r) : radius(r) {}
    double getRadius() const { return radius; }
    void setRadius(double r) { radius = r; }
    double getArea() const { return 3.14 * radius * radius; }
};
```

外部只通过构造、`get`/`set`、`getArea` 使用圆，半径如何存储对外不可见。

### 1.2 为何需要封装：Bear / Animal

C 里常用「结构体存数据 + 全局函数表示行为」，属性和行为分离：

```cpp
typedef struct Bear {
    char name[64];
    int age;
} Bear;

typedef struct Animal {
    char name[64];
    int age;
    int type;
} Animal;

void BearEat(Bear* bear);
void AnimalEat(Animal* animal);

int main() {
    Bear bear;
    strcpy(bear.name, "维尼");
    bear.age = 30;
    AnimalEat((Animal*)&bear);  // 类型/语义易用错，编译器帮不上多少忙
}
```

把属性和行为放进同一个类，并设为 private + 公开接口，可减少误用、统一访问路径，并支持「只读 / 读写 / 不可访问」等细粒度控制。

---

## 二、类的声明与定义

### 2.1 声明与定义

```cpp
class Screen;  // 仅声明：尚不知成员

void f(Screen&);   // OK：引用
void g(Screen*);   // OK：指针
// void h(Screen); // 错误：需要完整类型
```

创建对象前必须有**完整定义**。类不能含自身类型的成员对象，但可以含本类指针/引用：

```cpp
class LinkScreen {
    LinkScreen* next;  // OK
    // LinkScreen window;  // 错误：不完整的自身对象成员
};
```

定义以分号结束：`class Foo { /* ... */ };`

### 2.2 类作用域与类型别名

每个类有独立作用域与类型。类外定义成员时，`ClassName::` **之后**属于类作用域；返回类型若是类内 typedef，须加类名限定：

```cpp
class Screen {
public:
    typedef std::string::size_type index;
    index get_cursor() const;
};

Screen::index Screen::get_cursor() const {
    return cursor;
}
```

用类型别名简化意图：

```cpp
class People {
public:
    typedef std::string phonenum;
    phonenum phonePub;
private:
    phonenum phonePri;
};
```

### 2.3 struct 与 class

语法基本相同；**默认访问权限**：`struct` 为 `public`，`class` 为 `private`。习惯上用 `class` 做封装实体，`struct` 做偏数据聚合。

空类对象大小至少为 1 字节（保证不同对象地址不同）。

---

## 三、访问控制

```cpp
class Person {
public:
    void show() { /* ... */ }
    int mTall;       // 对外可见
protected:
    int mMoney;      // 派生类可访问（继承章节详述）
private:
    int mAge;        // 仅本类（及友元）可访问
};
```

- **类内**：成员之间无访问限制
- **类外**：通常只能访问 `public`；无继承时 `private` 与 `protected` 对外效果相同

### 为何成员变量应 private

1. **统一访问入口**：外部只通过成员函数，接口一致、易维护  
2. **细粒度控制**：只读 / 读写 / 只写 / 不可访问，并可加校验

```cpp
class AccessLevels {
public:
    int getReadOnly() const { return readOnly; }
    void setReadWrite(int v) { readWrite = v; }
    int getReadWrite() const { return readWrite; }
    void setWriteOnly(int v) { writeOnly = v; }
private:
    int readOnly;
    int noAccess;
    int readWrite;
    int writeOnly;
};
```

---

## 四、默认成员函数、构造与 this

编译器为类准备（在需要且用户未定义时合成）的常见成员包括：

1. 默认构造函数  
2. 析构函数  
3. 拷贝构造函数  
4. 拷贝赋值 `operator=`  
5. 取址 `operator&`（const / 非 const）

构造可重载、可带参；析构只有一个、无参、不可重载。

### 4.1 构造函数

与类同名、无返回类型，在创建对象时自动调用。

```cpp
class Sales_item {
public:
    Sales_item();
    Sales_item(const std::string&);
    explicit Sales_item(std::istream&);
};
```

要点：

| 概念 | 说明 |
|------|------|
| 默认构造 | 无参，或全部参数都有默认值 |
| 合成默认构造 | **仅当类未定义任何构造函数时**才可能由编译器生成 |
| 初始化列表 | `: mem(arg), ...`，先于函数体执行；**初始化顺序 = 成员声明顺序**，与列表书写顺序无关 |
| const / 引用成员 | **必须**在初始化列表中初始化 |
| `explicit` | 抑制单参构造的隐式转换，单参构造默认建议加 |
| 禁止复制 | 可将拷贝构造 / 赋值声明为 `private`（或 C++11 `= delete`） |

```cpp
class ConstRef {
public:
    ConstRef(int ii) : i(ii), ci(ii), ri(i) {}
private:
    int i;
    const int ci;
    int& ri;
};

class A {
public:
    explicit A(int x) : ia(x) {}
    bool equalTo(const A& other) const { return ia == other.ia; }
private:
    int ia;
};
// A a(1); a.equalTo(1);  // 若无 explicit，1 会隐式转成 A，易埋隐患
```

构造分两阶段：① 初始化（列表）② 函数体中的赋值/计算。优先用初始化列表，尤其对类类型成员。

### 4.2 this 指针

非静态成员函数隐含 `this`，指向当前对象；不占对象 `sizeof`。

```cpp
class Screen {
public:
    Screen& set(char c) {
        contents[cursor] = c;
        return *this;  // 支持链式调用
    }
};
```

形参与成员同名时可用 `this->mem` 区分。**静态成员函数没有 this**，不能直接访问非静态成员。

---

## 五、拷贝构造：浅拷贝与深拷贝

拷贝构造形参一般为 `const Class&`。在下列情况会调用：用同类型对象初始化、按值传参、按值返回等。

含指针成员时，编译器合成的拷贝往往是**浅拷贝**（只复制指针值），多个对象指向同一块堆内存，析构时会**重复释放**。

```cpp
class Student {
public:
    Student() { name = new char[20]; }
    Student(const Student& s) {          // 深拷贝
        name = new char[20];
        memcpy(name, s.name, 20);
        num = s.num;
    }
    ~Student() {
        delete[] name;
        name = nullptr;
    }
private:
    int num;
    char* name;
};

Student s1;
Student s2(s1);  // 走自定义拷贝构造，各自持有独立缓冲区
```

**浅拷贝**：复制指针 → 共享堆块。  
**深拷贝**：再分配并复制内容 → 独立所有权。

规则经验：有指针/资源成员时，通常需同时考虑**拷贝构造、拷贝赋值、析构**（三者一致管理资源）。

---

## 六、析构函数

名字为 `~类名`，无返回值、无参数，在对象销毁时自动调用，用于释放资源。

调用时机（常见）：

- 自动对象离开作用域  
- `delete` 动态对象  
- 容器/数组销毁时，按元素从后往前调用析构  

未自定义析构时，编译器合成的析构会析构类类型成员；**不会**自动 `delete` 你用 `new` 得到的裸指针，需自己写。

---

## 七、静态成员

静态成员属于**类**，不属于某个对象；程序期间一份存储，所有对象共享。

```cpp
class Point {
public:
    Point() { ++count; }
    ~Point() { --count; }
    static int getCount() { return count; }  // 无 this
private:
    static int count;  // 声明
};

int Point::count = 0;  // 类外定义并初始化（不要再写 static）

// 调用：Point::getCount(); 或 pt.getCount();
```

关键结论：

1. 静态数据成员须在类外**定义一次**并初始化；不能靠构造初始化列表初始化静态成员  
2. 可通过 `类名::` 或对象访问（受 public/private 约束）  
3. 静态函数无 this → **不能**访问非静态成员；非静态函数可以调用静态成员  
4. 不能通过类名调用非静态成员函数  

---

## 八、友元

`friend` 授予指定函数或类访问本类非公有成员的权限。友元**不是**该类的成员，无 this，不受出现位置的访问区段影响。

```cpp
class Husband {
    friend class Wife;           // 友元类
    friend void audit(Husband&); // 友元函数
private:
    double money;
};

class Wife {
public:
    void consume(Husband& h) { h.money -= 10000; }
};
```

成员函数作友元时，注意声明顺序：先声明被访问类 → 定义提供友元函数的类（只声明该函数）→ 定义被访问类并写 `friend` → 再定义该成员函数。

**务必记住：**

1. **单向**：A 是 B 的友元，不代表 B 是 A 的友元  
2. **不继承**：友元关系不能传给派生类  
3. **不传递**：B 是 A 的友元、C 是 B 的友元，不代表 C 是 A 的友元  

友元破坏封装边界，应控制范围，常用于运算符重载（如 `operator<<`）等确有需要的场景。

---

## 九、类中的 const

（全局 const / `#define` 对比见上一讲；此处只谈类相关。）

### 9.1 const 对象与常成员函数

```cpp
class Temp {
public:
    void func1();
    void func2() const;  // 承诺不修改对象逻辑状态
};

const Temp t;
// t.func1();  // 错误：const 对象只能调 const 成员函数
t.func2();     // OK
```

常成员函数不能修改非 mutable 的成员，也不能调用非 const 成员函数。不修改状态的查询函数应标 `const`。

### 9.2 const 成员变量

只能在**初始化列表**中初始化，之后不可改。

```cpp
class Temp {
public:
    explicit Temp(int x) : val(x) {}
    const int val;
};
```

### 9.3 mutable

允许在 const 成员函数中修改「不影响对象抽象状态」的成员（如缓存计数）：

```cpp
class ST {
public:
    void show() const { ++showCount; /* a = 1; 错误 */ }
    int a = 0;
    mutable int showCount = 0;
};
```

`mutable` 只能修饰非静态数据成员。

---

## 十、运算符重载

运算符重载是语法糖：把 `a @ b` 变成函数调用，使自定义类型用起来更自然。不能发明新运算符，不能改优先级和操作数个数。

```cpp
返回类型 operator@(参数表) { /* ... */ }
```

### 10.1 成员 vs 全局 / 友元

| 方式 | 特点 |
|------|------|
| 成员函数 | 左操作数必须是类对象（即 `this`）；二元运算少一个显式参数 |
| 全局函数 | 参数个数 = 操作数个数；至少有一个类类型参数 |
| 友元全局 | 同全局，但可直接访问私有成员，适合 `<<` / `>>` |

成员形式下，`c1 + 2` 可能借助单参构造转换右侧；`2 + c1` 则不会调成员 `operator+`。全局/友元形式配合转换构造，两侧都更易对称。

### 10.2 常用重载示例要点

**输出 `<<`（必须全局，常配合友元）：**

```cpp
class Person {
    friend ostream& operator<<(ostream& os, const Person& p);
public:
    Person(int id, int age) : mID(id), mAge(age) {}
private:
    int mID, mAge;
};

ostream& operator<<(ostream& os, const Person& p) {
    os << "ID:" << p.mID << " Age:" << p.mAge;
    return os;  // 支持链式 cout << a << b;
}
```

**加法 `+`（成员示意）：**

```cpp
Complex operator+(const Complex& rhs) const {
    return Complex(real + rhs.real, imag + rhs.imag);
}
```

**前置 / 后置 `++` `--`：**

```cpp
Complex& operator++() {    // 前置：++c
    ++mA; ++mB;
    return *this;
}
Complex operator++(int) {  // 后置：c++（int 为占位）
    Complex tmp(*this);
    ++(*this);
    return tmp;
}
```

优先实现前置；后置通过前置实现，并返回旧值。

**赋值 `=`：**

```cpp
Person& operator=(const Person& other) {
    if (this == &other) return *this;  // 自赋值防护
    // 释放自身资源 → 深拷贝 other → return *this
    return *this;
}
```

注意：`Person a = b;` 是**拷贝构造**；`a = b;`（a 已存在）才是 `operator=`。

**相等 `==` / 函数调用 `()`：**

```cpp
bool operator==(const Complex& rhs) const { /* 比较各字段 */ }
int operator()(int x, int y) { return x + y; }  // 函数对象：obj(1, 2)
```

### 10.3 哪些必须是成员函数

| 运算符 | 要求 |
|--------|------|
| `=` `[]` `()` `->` | **必须**成员函数 |
| `<<` `>>` | 通常为**全局**（常 + friend），以便左侧为流对象 |
| `&&` `\|\|` | **不要重载**（无法保留内置短路语义） |

---

## 十一、综合练习（要点 + 接口）

任选其一实现即可，重在封装与接口设计，不必追求超长完整工程代码。

### 练习 A：立方体 Cube

需求：长宽高私有；提供 set/get；求表面积与体积；成员函数与全局函数两种方式判断两立方体是否相等。

```cpp
class Cube {
public:
    void setL(int l); void setW(int w); void setH(int h);
    int getL() const; int getW() const; int getH() const;
    int area() const;    // 2*(lw+lh+wh)
    int volume() const;  // l*w*h
    bool equalTo(const Cube& other) const;
private:
    int mL = 0, mW = 0, mH = 0;
};
bool equal(const Cube& a, const Cube& b);  // 全局版
```

### 练习 B：点与圆的关系

```cpp
class Point {
public:
    void setX(int x); void setY(int y);
    int getX() const; int getY() const;
private:
    int mX = 0, mY = 0;
};

class Circle {
public:
    void setCenter(int x, int y); void setR(int r);
    // 比较 (x1-x0)^2+(y1-y0)^2 与 r^2：内 / 上 / 外
    void relation(const Point& p) const;
private:
    Point mCenter;
    int mR = 0;
};
```

### 练习 C：MyString 思路（选做）

自行管理 `char*` 堆内存，练习深拷贝与运算符：

```cpp
class MyString {
    friend ostream& operator<<(ostream&, const MyString&);
    friend istream& operator>>(istream&, MyString&);
public:
    MyString(const char* = "");
    MyString(const MyString&);
    ~MyString();
    MyString& operator=(const MyString&);
    MyString& operator=(const char*);
    MyString operator+(const MyString&) const;
    bool operator==(const MyString&) const;
    char& operator[](int index);
private:
    char* pString;
    int mSize;  // 不含 '\0'
};
```

实现要点：构造分配；拷贝/赋值深拷贝；赋值先释放旧内存并处理自赋值；析构 `delete[]`；`+` 分配新缓冲拼接后返回新对象。

---

## 课堂小结

- 封装 = 数据与操作合一 + 访问控制；成员变量默认应 private  
- 构造负责初始化（优先初始化列表），析构负责释放；含资源时配套拷贝构造与赋值（深拷贝）  
- this 绑定当前对象；静态成员属类；友元单向、不继承、不传递  
- const 对象只能调常成员函数；mutable 放宽“逻辑常量”下的计数等字段  
- 运算符重载提升可读性；`=` `[]` `()` `->` 必须为成员；`<<` 宜为友元全局函数  

---

## 随堂练习

1. 实现 `Person`：私有 `name`、`age`；提供构造与 set/get；`setAge` 仅接受 0–100，越界拒绝修改；提供 `print()`。  
2. 为含 `char* name` 的类写出拷贝构造与 `operator=`，用两个对象验证析构不会 double-free。  
3. 为某类重载 `operator<<` 与前置/后置 `++`，在 `main` 中演示链式输出与 `++c` / `c++` 的差异。
