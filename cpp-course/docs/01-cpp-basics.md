# 01 C++入门与对C的扩展

## 课程目标

1. 编写并理解简单的 C++ 程序（Hello World、头文件、命名空间、cout）
2. 区分面向过程与面向对象的基本思路
3. 掌握作用域运算符与命名空间的常用写法
4. 理解 C++ 相对 C 的扩展：更严格类型检查、struct 增强、bool、三目左值、const、引用
5. 掌握内联函数、默认/占位参数、函数重载、`extern "C"`、Lambda 表达式

---

## 一、初识 C++

### 1.1 Hello World

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "hello world" << endl;
    return 0;
}
```

| 要素 | 说明 |
|------|------|
| `#include <iostream>` | 引入标准输入输出流 |
| `using namespace std;` | 引入标准命名空间中的名字 |
| `cout` / `endl` | 标准输出；`endl` 换行并刷新缓冲区 |

### 1.2 头文件风格

| 类型 | 约定 | 示例 | 说明 |
|------|------|------|------|
| C++ 旧式 | `.h` | `iostream.h` | 可用，但不推荐 |
| C 旧式 | `.h` | `math.h` | C/C++ 都可用 |
| C++ 新式 | 无扩展名 | `iostream` | 推荐，配合 `namespace std` |
| 转换后的 C | `c` 前缀 | `cmath` | C 库的 C++ 版本 |

C++ 标准头文件通常无扩展名；源自 C 的头文件去掉 `.h` 并加前缀 `c`（如 `math.h` → `cmath`）。

### 1.3 面向过程 vs 面向对象

| | 面向过程 | 面向对象 |
|--|----------|----------|
| 基本单元 | 函数/过程 | 对象（数据 + 操作） |
| 组织方式 | 功能分解，自顶向下 | 类与对象交互 |
| 复用方式 | 模块化、函数复用 | 封装、继承、多态 |
| 核心等式 | 程序 = 数据结构 + 算法 | 对象 = 数据 + 算法；程序 = 对象协作 |

> 封装、继承、多态、抽象等 OOP 特性将在后续「类与对象」中展开，此处只建立对比印象。

---

## 二、作用域运算符 `::`

局部变量会遮蔽同名全局变量；用 `::` 可访问被遮蔽的全局名字。

```cpp
int a = 10;  // 全局

void test() {
    int a = 20;  // 局部
    cout << "局部 a: " << a << endl;   // 20
    cout << "全局 a: " << ::a << endl; // 10
}
```

`::` 也用于访问命名空间成员、类的静态成员、类外定义的成员函数等。

---

## 三、命名空间

命名空间用于控制名字的可见范围，避免大规模工程与多库协作时的名字冲突。

### 3.1 定义与访问

```cpp
namespace A { int a = 10; }
namespace B { int a = 20; }

void test() {
    cout << A::a << endl;  // 10
    cout << B::a << endl;  // 20
}
```

要点：

- **只能在全局范围定义**（不能写在函数内部）
- **可嵌套**
- **开放**：可多次向同一命名空间追加成员
- 声明与实现可分离：`void MySpace::func();`

```cpp
namespace Outer {
    int x = 10;
    namespace Inner {
        int y = 20;
    }
}
// 访问：Outer::x、Outer::Inner::y
```

```cpp
namespace A { int a = 10; }
namespace A { void func() { cout << "hello" << endl; } }  // 追加成员
```

### 3.2 匿名命名空间与别名

匿名命名空间中的名字仅本翻译单元可见（类似内部链接的 `static`）：

```cpp
namespace {
    int x = 10;
    void foo() { /* ... */ }
}
// 本文件内可直接使用 x、foo()
```

命名空间别名：

```cpp
namespace veryLongName { int a = 10; }
namespace shortName = veryLongName;
cout << shortName::a << endl;
```

### 3.3 using 声明 vs using 指令

| | using 声明 | using 指令 |
|--|------------|------------|
| 写法 | `using A::paramA;` | `using namespace A;` |
| 效果 | 引入**一个**名字 | 引入命名空间内**全部**名字 |
| 重载 | 一次引入同名重载函数的整组 | — |
| 风险 | 同作用域内注意同名冲突 | 多个命名空间同时引入易二义 |

```cpp
namespace A {
    int paramA = 20;
    void funcA() {}
}

void demo() {
    using A::paramA;   // 声明：只引入 paramA
    cout << paramA << endl;
    // cout << paramB; // 未引入，不可直接用

    using namespace A; // 指令：A 中名字均可直接用
}
```

优先用作用域限定 `A::name` 或精确的 using 声明；少用文件级 `using namespace std;`（教学示例可例外）。

---

## 四、类型与语言增强

### 4.1 更严格的类型检查

C 中可编译通过、C++ 中往往报错的例子：

```cpp
typedef enum COLOR { GREEN, RED, YELLOW } color;
color mycolor = GREEN;
// mycolor = 10;           // C++：枚举与 int 不能随意赋值
// char *p = malloc(10);   // C++：void* 不能隐式转成 char*
```

### 4.2 struct 增强

- 定义变量时可省略 `struct` 关键字
- 结构体中**既可有成员变量，也可有成员函数**

```cpp
struct Student {
    string mName;
    int mAge;
    void setName(string name) { mName = name; }
    void show() { cout << mName << " " << mAge << endl; }
};

void test() {
    Student s;  // 无需写 struct Student
    s.setName("John");
    s.mAge = 20;
    s.show();
}
```

> `struct` 与 `class` 语法几乎相同，默认访问权限不同：`struct` 默认 `public`，`class` 默认 `private`（详见下一讲）。

### 4.3 bool

`bool` 只能取 `true` / `false`；转成整型时分别为 1 / 0。C99 可通过 `<stdbool.h>` 使用类似类型；C++ 则是内建关键字。

### 4.4 三目运算符的左值增强

- **C**：`a > b ? a : b` 返回的是**值**（右值），不能对其赋值
- **C++**：两边都是左值时，表达式本身是**左值**（引用），可以赋值

```cpp
int a = 10, b = 20;
(a > b ? a : b) = 100;  // C++ 合法：给较大者赋 100，此处改的是 b
```

左值（lvalue）：可取地址、可出现在赋值左侧；右值（rvalue）：一般是临时值，可读但通常不可赋值。

---

## 五、const

### 5.1 C 与 C++ 中 const 的要点差异

| 点 | C | C++ |
|----|---|-----|
| 含义倾向 | 只读变量，通常分配存储 | 更接近编译期常量，可进符号表 |
| 作数组长度 | 局部/全局 const 通常不能作数组大小 | 编译期常量可作数组大小 |
| 默认链接 | 全局 const 默认**外部链接** | 全局 const 默认**内部链接** |
| 取地址 / `extern` | 始终有存储 | 取地址或 `extern` 声明时会分配存储 |

全局 const 若落在只读段，通过指针强行写入会在运行期出错。局部 const：

- **字面量初始化的基本类型**（如 `const int a = 10`）：C++ 常放入符号表；对其取地址时再分配内存，指针改的是这块内存，通过名字读到的仍可能是符号表中的值
- **用变量初始化**（`const int a = b`）或**类对象**：会分配内存

需要跨文件共享时显式写出：

```cpp
extern const int a = 10;
```

### 5.2 尽量用 const 替代 `#define`

```cpp
// #define MAX 1024   // 无类型、无作用域、预处理直接替换，出错信息不友好
const int max = 1024; // 有类型、有作用域、参与编译检查
```

对比：

1. **类型**：`const` 可做类型检查与重载决议；宏只是文本替换
2. **作用域**：`const` 遵循块作用域；宏从定义处到文件尾（或 `#undef`），且**不能**真正属于某个 `namespace`

---

## 六、引用

### 6.1 声明与规则

```cpp
int a = 10;
int& b = a;   // b 是 a 的别名
b = 100;      // 即修改 a
```

规则：

1. 引用必须初始化，初始化后**不能改绑**到另一个对象（`ref = b` 是赋值，不是改绑定）
2. 对引用的操作就是对原对象的操作；`&a` 与 `&b` 相同
3. 不能定义「引用的数组」；可以有指针的引用：`int*& ptr = p;`
4. **本质**：编译器内部常实现为指针常量 `Type* const`

```cpp
// int& ref = val;  ≈  int* const ref = &val;
```

### 6.2 常引用

```cpp
int a = 10;
const int& b = a;
// b = 20;  // 错误：不能通过常引用修改
a = 20;     // 可以通过原变量修改
```

常引用常用于函数形参：避免拷贝大开销，又防止意外修改实参。

### 6.3 作参数与返回值

```cpp
void swap(int& x, int& y) {
    int t = x; x = y; y = t;
}

int result = 0;
int& square(int r) {
    result = r * r;
    return result;  // 可返回全局/静态或调用方仍存活的对象
}

// 禁止：返回局部变量的引用（生命周期已结束）
```

传引用与传指针效果相近，语法更清晰。不要返回局部自动变量的引用。

### 6.4 引用 vs 指针（精简）

| | 引用 | 指针 |
|--|------|------|
| 初始化 | 必须 | 可稍后 |
| 可空 | 否 | 可以（`nullptr`） |
| 改指向 | 不可改绑 | 可改指向 |
| 语法 | 直接当对象用 | 需 `*` / `->` |
| 本质 | 别名（常实现为指针常量） | 存放地址的变量 |

---

## 七、内联函数、默认参数、占位参数

### 7.1 内联函数 `inline`

编译器在合适时把函数调用展开为函数体，减少调用开销。适合短小、频繁调用的函数；过大或含复杂控制流时收益有限，还可能增大代码体积。

`inline` 应与**函数定义**放在一起才有意义（仅写在声明上通常无效）：

```cpp
inline void swap(int& a, int& b) {
    int t = a; a = b; b = t;
}
```

类内定义的成员函数默认具有 inline 属性。

### 7.2 默认参数

```cpp
void TestFunc(int a = 10, int b = 20) {
    cout << a + b << endl;
}

TestFunc();        // 10 + 20
TestFunc(100);     // 100 + 20
TestFunc(100, 200);
```

规则：

1. 默认参数必须从**右向左**连续提供（某个参数有默认值，则其后参数都必须有）
2. 声明与定义分开时，**只在一处**设置默认参数（通常放在声明处）

### 7.3 占位参数

只有类型、没有名字；函数体内一般用不到，但调用时仍需传实参（除非也给了默认值）：

```cpp
void f(int a, int b, int) { cout << a + b << endl; }
f(10, 20, 30);  // 第三个实参必需

void g(int a, int b, int = 0) { /* ... */ }
g(10, 20);      // 占位参数用默认值
```

后置 `++` 重载会用到占位的 `int` 形参（见「类与对象」中的运算符重载）。

---

## 八、函数重载

同一作用域内，同名函数可通过**参数个数、类型或顺序**区分，实现重载。

```cpp
void MyFunc() {}
void MyFunc(int a) {}
void MyFunc(string b) {}
void MyFunc(int a, string b) {}
void MyFunc(string b, int a) {}  // 参数顺序不同也可重载
```

### 8.1 条件与禁止项

**可以作为重载条件：** 同一作用域；参数个数 / 类型 / 顺序不同。

**不能**仅靠返回值类型区分：

```cpp
void f(int);
// int f(int);  // 错误：无法仅按返回值重载
```

原因：调用方可忽略返回值，`f(10)` 时编译器无法确定该调哪一个。

### 8.2 与默认参数的二义性

```cpp
void MyFunc(string b) {}
void MyFunc(string b, int a = 10) {}

// MyFunc("hello");  // 二义：两个函数都能匹配
```

### 8.3 实现原理（name mangling）简述

C++ 编译器通过**名字修饰**把参数类型编入符号名，以支持重载。Linux/g++ 下示意：

```text
void func()           →  _Z4funcv
void func(int)        →  _Z4funci
void func(int, char)  →  _Z4funcic
```

不同编译器修饰规则可能不同；链接时按修饰后的名字匹配。

---

## 九、`extern "C"`

C 与 C++ 名字修饰规则不同：C 大致保留原名，C++ 会修饰。因此在 C++ 中直接声明并链接 C 函数会找不到符号。

用 `extern "C"` 让指定声明按 C 规则编译链接：

```c
/* MyModule.h — 可被 C/C++ 共用 */
#ifndef MYMODULE_H
#define MYMODULE_H
#ifdef __cplusplus
extern "C" {
#endif
void func1();
int func2(int a, int b);
#ifdef __cplusplus
}
#endif
#endif
```

```cpp
// 或在 .cpp 中单独声明
extern "C" void func1();
extern "C" int func2(int a, int b);
```

---

## 十、Lambda 表达式

C++11 起支持的匿名函数对象，适合作为算法回调、一次性小函数。

### 10.1 语法

```cpp
[capture](parameters) mutable -> return_type { statements; }
```

常用简化形式：

```cpp
auto sum = [](int a, int b) { return a + b; };
cout << sum(3, 4) << endl;  // 7
```

### 10.2 捕获

| 写法 | 含义 |
|------|------|
| `[]` | 不捕获 |
| `[=]` | 按值捕获所有用到的自动变量 |
| `[&]` | 按引用捕获 |
| `[=, &x]` / `[&, x]` | 默认一种，个别例外 |
| `[x, &y]` | 指定：x 按值，y 按引用 |

默认按值捕获时，函数体内一般不能修改捕获副本；需要修改时加 `mutable`。

```cpp
int test = 100;
auto fl = [test](int x, int y) { return test + x + y; };
auto f2 = [=](int x, int y) { return test + x + y; };
```

### 10.3 与 `sort` 结合

```cpp
#include <algorithm>
#include <cmath>
#include <iostream>
using namespace std;

void abssort(float* x, unsigned n) {
    sort(x, x + n, [](float a, float b) {
        return abs(a) < abs(b);
    });
}

int main() {
    float a[5] = { -2.1f, 3.5f, -4.0f, 5.2f, 3.3f };
    abssort(a, 5);
    for (auto& v : a) cout << v << endl;
}
```

---

## 课堂小结

- C++ 程序以 `<iostream>`、`std`、`cout` 起步；头文件多为无扩展名风格
- 面向过程侧重函数分解，面向对象侧重对象协作；本讲只建立对比
- `::` 与 `namespace` 解决名字冲突；分清 using 声明与 using 指令
- C++ 类型更严；`struct` 可含成员函数；`bool`、三目左值、const、引用是常用扩展
- 引用是别名（常实现为指针常量）；形参优先考虑常引用
- 内联、默认/占位参数、重载（不能靠返回值）、`extern "C"`、Lambda 是函数层面的重要能力

---

## 随堂练习

1. **引用交换**：编写 `void swap(int& a, int& b)`，在 `main` 中验证两个变量的值被交换，并打印二者地址说明引用未产生新对象。
2. **重载与默认参数**：定义一组 `print` 重载（无参 / `int` / `string`），再尝试与带默认参数的同名函数组合，观察并解释二义性错误。
3. **Lambda 排序**：给定 `vector<int>`，用 Lambda 按绝对值从小到大排序并输出；再改为按降序排序。
