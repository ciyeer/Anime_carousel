# 06 类型转换、智能指针与STL

## 课程目标

- 掌握四种 C++ 强制转换：`static_cast` / `dynamic_cast` / `const_cast` / `reinterpret_cast`
- 理解智能指针的必要性与 `unique_ptr` / `shared_ptr` / `weak_ptr`
- 掌握 STL 三大组件关系，会用常用容器与算法
- 能根据场景选择合适容器，并完成综合小练习

---

## 核心内容

### 一、类型转换

少用强制转换。C++ 四种命名转换比 C 风格更清晰、更可控。

#### 1.1 static_cast

- 继承体系中：上行转换（派生→基类）安全；下行转换无运行时检查，不安全
- 用于基本类型转换（如 `int`↔`char`），安全性由程序员保证
- 无关类型指针之间一般不能转换

```cpp
class Animal {};
class Dog : public Animal {};

char a = 'a';
double b = static_cast<double>(a);

Dog* d = nullptr;
Animal* an = static_cast<Animal*>(d);   // 上行，安全
Dog* d2 = static_cast<Dog*>(an);        // 下行，不安全
```

#### 1.2 dynamic_cast

- 用于多态继承体系的上下行转换（基类需有虚函数）
- 上行与 `static_cast` 类似；下行带**运行时类型检查**，更安全
- 不支持基本类型；指针失败返回 `nullptr`，引用失败抛 `bad_cast`

```cpp
class Animal {
public:
    virtual void Show() = 0;
};
class Dog : public Animal {
public:
    void Show() override { cout << "dog\n"; }
};

Dog* d = new Dog;
Animal* a = dynamic_cast<Animal*>(d);   // OK
// Dog* d2 = dynamic_cast<Dog*>(a);     // a 若实际不是 Dog，得到 nullptr
```

#### 1.3 const_cast

用于去除或添加指针/引用的 `const` 属性。不能对非指针、非引用的普通变量直接去 const。

```cpp
const int* p = nullptr;
int* np = const_cast<int*>(p);

int x = 10;
int& r = x;
const int& cr = const_cast<const int&>(r);
```

#### 1.4 reinterpret_cast

最不安全。可在无关类型间做底层位模式重解释（如指针↔整数）。仅在底层系统编程等极少数场景使用。

```cpp
int n = 42;
uintptr_t addr = reinterpret_cast<uintptr_t>(&n);
int* p = reinterpret_cast<int*>(addr);
```

---

### 二、智能指针

#### 2.1 为何需要

裸 `new`/`delete` 易泄漏、易悬空。智能指针是栈上对象，离开作用域自动析构并释放资源。

`auto_ptr`（C++98）已弃用：赋值会“偷走”所有权，留下隐患。现代 C++ 使用后三者。

#### 2.2 unique_ptr — 独占所有权

同一时间只有一个 `unique_ptr` 拥有对象；不可拷贝，可移动。

```cpp
unique_ptr<string> p1(new string("hello"));
// unique_ptr<string> p2 = p1;           // 编译错误
unique_ptr<string> p3 = move(p1);        // 转移所有权
unique_ptr<string> p4(new string("tmp")); // 临时右值可赋值
```

#### 2.3 shared_ptr — 共享所有权（引用计数）

多个 `shared_ptr` 可指向同一对象；引用计数为 0 时释放。常用：`use_count`、`unique`、`get`、`reset`、`swap`。推荐 `make_shared`。

```cpp
shared_ptr<string> ps1(new string("s1"));
shared_ptr<string> ps2 = ps1;
cout << ps1.use_count();  // 2
ps1.reset();              // 计数减一
```

原理（精简）：智能指针把裸指针封装成栈对象；`shared_ptr` 在堆上维护引用计数，复制 +1、销毁 -1，到 0 则 `delete`。

#### 2.4 weak_ptr — 打破循环引用

两个对象互相持有对方的 `shared_ptr` 会造成循环引用，计数永不为 0，泄漏。把其中一方改为 `weak_ptr`（不增加强引用计数）即可。

```cpp
class B;
class A {
public:
    weak_ptr<B> pb;   // 勿用 shared_ptr 形成环
    ~A() { cout << "A delete\n"; }
};
class B {
public:
    shared_ptr<A> pa;
    ~B() { cout << "B delete\n"; }
};
```

使用前：`expired()` 检查；`lock()` 获得临时 `shared_ptr` 再访问对象。`weak_ptr` 未重载 `*` / `->`。

---

### 三、STL 概览

STL（Standard Template Library）三大组件：

| 组件 | 作用 |
|------|------|
| 容器 container | 管理数据集合（序列式 / 关联式） |
| 算法 algorithm | 对区间做查找、排序、遍历等 |
| 迭代器 iterator | 连接容器与算法的“泛化指针” |

关系：算法通过迭代器访问容器，二者解耦，提高复用。

#### Hello vector

```cpp
#include <vector>
#include <algorithm>
#include <iostream>
using namespace std;

int main() {
    vector<int> v{1, 5, 3, 7};
    for (auto it = v.begin(); it != v.end(); ++it)
        cout << *it << " ";
    cout << "\ncount 5: " << count(v.begin(), v.end(), 5) << endl;
}
```

容器还可存对象、指针，甚至嵌套容器（如 `vector<vector<int>>`）。

---

### 四、常用容器

#### 4.1 string（与 char*）

| 对比 | char* | string |
|------|-------|--------|
| 本质 | 指针 | 类，封装并管理字符数组 |
| 内存 | 需手动管理 | 自动管理，减少越界/泄漏 |
| 能力 | 依赖 C 库 | find / replace / substr 等 |

转换：`str.c_str()` → `const char*`；`string s(cstr)` ← `char*`。

常用 API（按类精简）：

- 构造：`string()` / `string(const char*)` / `string(n, c)` / 拷贝构造
- 赋值：`=`、`assign`
- 访问：`[]`（越界未定义）、`at`（越界抛异常）
- 拼接：`+=`、`append`
- 查找替换：`find` / `rfind` / `replace`
- 子串删除：`substr` / `erase` / `insert`
- 比较：`compare`（`<` 返回 -1，`=` 返回 0，`>` 返回 1）

#### 4.2 vector

特性：

1. 动态数组，连续内存，随机访问 O(1)
2. 尾插/尾删高效；中间插入需移动元素
3. 空间不足时扩容：申请更大空间 → 拷贝 → 释放旧空间
4. 可用 `reserve` 预留容量，减少扩容次数
5. `resize` 改变大小并构造元素；`reserve` 只留空间不构造

常用 API：`push_back` / `pop_back` / `insert` / `erase` / `clear` / `size` / `empty` / `capacity` / `reserve` / `resize` / `at` / `[]` / `front` / `back`

#### 4.3 deque

特性：

1. 双端队列，分段连续空间，支持随机访问
2. 头尾插入删除均高效
3. 无“整块扩容拷贝”问题，一般不提供 `reserve`
4. 随机访问略慢于 vector
5. 适合两端进出的场景（如排队）

常用 API：`push_back` / `push_front` / `pop_back` / `pop_front` / `at` / `[]` / `size` / `empty`

#### 4.4 list

特性：

1. 双向链表，结点非连续
2. 任意位置插入删除 O(1)（已知迭代器）
3. 不支持随机访问（无 `[]`）
4. 额外指针开销，遍历较慢
5. 自带 `sort` / `reverse` / `remove`

常用 API：`push_back` / `push_front` / `insert` / `erase` / `remove` / `front` / `back` / `size` / `empty` / `sort` / `reverse`

#### 4.5 stack / queue

**stack（FILO）**：仅栈顶操作，无迭代器、不可遍历。

- API：`push` / `pop` / `top` / `empty` / `size`

**queue（FIFO）**：队尾入、队头出，无迭代器、不可遍历。

- API：`push` / `pop` / `front` / `back` / `empty` / `size`

#### 4.6 set / multiset

特性：

1. 基于红黑树，元素自动有序
2. `set` 键唯一；`multiset` 允许重复
3. 查找/插入/删除平均 O(log n)
4. 迭代器不可改键值（会破坏有序结构）
5. 关联式容器，按值（键）组织

常用 API：`insert` / `erase` / `find` / `count` / `lower_bound` / `upper_bound` / `equal_range` / `size` / `empty`

#### 4.7 map / multimap

特性：

1. 存键值对 `pair<const Key, T>`，按键自动排序
2. `map` 键唯一；`multimap` 允许相同键
3. 可改实值，不可改键
4. `operator[]`：键不存在会**插入**默认值（取值时需注意）
5. 插入可用 `insert(make_pair(...))` 或 `insert({k,v})`

对组：

```cpp
pair<string, int> p1("name", 20);
auto p2 = make_pair("name", 30);
cout << p2.first << " " << p2.second;
```

常用 API：`insert` / `erase` / `find` / `count` / `[]` / `at` / `size` / `empty`

#### 4.8 容器选择对照（精简）

|          | vector | deque | list | set/multiset | map/multimap |
|----------|--------|-------|------|--------------|--------------|
| 结构     | 单端数组 | 双端分段数组 | 双向链表 | 红黑树 | 红黑树 |
| 随机访问 | 是 | 是 | 否 | 否 | 按 key：是 |
| 查找     | 慢 | 慢 | 很慢 | 快 | 按 key：快 |
| 插入删除 | 尾端优 | 头尾优 | 任意位置优 | — | — |

选用提示：

- 历史记录、随机读多 → **vector**
- 两端进出（排队）→ **deque**
- 频繁任意位置插删 → **list**
- 有序唯一集合 / 排行榜 → **set**
- 按 ID 快速查用户 → **map**

#### 4.9 值语义与深拷贝

STL 容器存的是元素的**拷贝**（值语义），不是引用。若类内持有堆内存，必须正确实现拷贝构造与 `operator=`（深拷贝），否则浅拷贝会导致双重释放。

```cpp
class MyClass {
    char* data;
public:
    MyClass(const char* s) {
        data = new char[strlen(s) + 1];
        strcpy(data, s);
    }
    MyClass(const MyClass& o) {
        data = new char[strlen(o.data) + 1];
        strcpy(data, o.data);
    }
    MyClass& operator=(const MyClass& o) {
        if (this == &o) return *this;
        delete[] data;
        data = new char[strlen(o.data) + 1];
        strcpy(data, o.data);
        return *this;
    }
    ~MyClass() { delete[] data; }
};
// vector<MyClass> 才能安全 push_back
```

---

### 五、常用算法

头文件：`<algorithm>`（主体）、`<numeric>`（累计等）、`<functional>`（函数对象）。

算法作用于迭代器区间 `[first, last)`。质变算法会改元素（如 `sort`/`replace`）；非质变不改（如 `find`/`count`）。

#### 5.1 遍历

- `for_each(beg, end, func)`
- `transform(beg, end, dest, func)` — 目标容器需先 `resize`

```cpp
vector<int> v{1, 2, 3, 4};
for_each(v.begin(), v.end(), [](int x) { cout << x << " "; });

vector<int> dest(v.size());
transform(v.begin(), v.end(), dest.begin(), [](int x) { return x + 10; });
```

#### 5.2 查找

| 算法 | 作用 |
|------|------|
| `find` | 找等于 value 的元素，失败返回 `end()` |
| `find_if` | 按条件查找 |
| `adjacent_find` | 找相邻重复 |
| `binary_search` | 二分查找（要求有序） |
| `count` / `count_if` | 计数 |

```cpp
auto it = find(v.begin(), v.end(), 3);
if (it != v.end()) cout << *it;
```

自定义类型用 `find` 需重载 `operator==`。

#### 5.3 排序

- `sort(beg, end)` / `sort(beg, end, cmp)`
- `random_shuffle`（C++14 及以前）/ `shuffle`（C++17）
- `reverse`
- `merge`（合并两个**有序**区间到目标）

#### 5.4 拷贝与替换

- `copy` / `replace` / `replace_if` / `swap`（交换两容器）

#### 5.5 数值

- `accumulate(beg, end, init)` — 求和
- `fill(beg, end, val)` — 填充

#### 5.6 集合（要求有序）

- `set_intersection` 交集
- `set_union` 并集
- `set_difference` 差集

目标区间需预留足够空间；返回写入结束位置的迭代器。

---

### 六、综合小练习

#### 练习 1：邮箱格式校验（string）

要求：含 `@` 与 `.`，且 `.` 在 `@` 之后；`@` 前用户名仅小写字母。

```cpp
bool CheckValid(const string& email) {
    auto at = email.find('@');
    auto dot = email.find('.', at == string::npos ? 0 : at);
    return at != string::npos && dot != string::npos && at < dot;
}

bool CheckUsername(const string& email) {
    auto at = email.find('@');
    if (at == string::npos) return false;
    string user = email.substr(0, at);
    for (char c : user)
        if (c < 'a' || c > 'z') return false;
    return !user.empty();
}
```

#### 练习 2：单词统计（map + string）

输入一段文本，统计每个单词出现次数并输出。

```cpp
#include <map>
#include <sstream>
#include <string>
#include <iostream>
using namespace std;

int main() {
    string line, word;
    getline(cin, line);
    istringstream iss(line);
    map<string, int> freq;
    while (iss >> word) ++freq[word];
    for (const auto& p : freq)
        cout << p.first << ": " << p.second << endl;
}
```

---

## 课堂小结

- 四种转换各有职责：`static` 编译期、`dynamic` 运行期检查、`const` 去/加常量、`reinterpret` 底层重解释
- 智能指针：`unique_ptr` 独占，`shared_ptr` 引用计数共享，`weak_ptr` 解决循环引用；`auto_ptr` 已弃用
- STL：容器存数据、迭代器搭桥、算法做事
- 按访问模式与插删位置选容器；注意值语义与深拷贝
- 算法按遍历/查找/排序/拷贝/数值/集合分类记忆，配合迭代器区间使用

---

## 随堂练习

1. 用 `shared_ptr` + `weak_ptr` 演示并解决 A/B 互相引用导致的泄漏。
2. 完成「邮箱校验」或「单词统计」中至少一题，并额外用 `vector` + `sort` + `unique` 对一组整数去重排序输出。
