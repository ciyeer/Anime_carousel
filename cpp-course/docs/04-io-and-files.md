# 04 字符串、动态内存与文件I/O

## 课程目标

1. 理解 C++ 流的概念与 iostream 类库结构
2. 熟练使用 `cin`/`cout`/`cerr`/`clog` 及常用成员函数、格式化输出
3. 掌握 `std::string` 常用操作
4. 理解 `new`/`delete` 与 `malloc`/`free` 的区别，避免内存泄漏
5. 掌握文本文件与二进制文件的读写

---

## 核心内容

### 一、流的概念与 iostream 类库

程序的输入：从外部把数据送入程序；输出：把数据从程序送出。C++ I/O 主要包括：

1. **标准 I/O**：键盘 / 显示器（`cin`/`cout` 等）
2. **文件 I/O**：磁盘文件（`ifstream`/`ofstream`/`fstream`）
3. **串 I/O**：内存中的字符序列（字符串流）

#### 常用流类（简表）

| 类名     | 作用           | 头文件   |
| -------- | -------------- | -------- |
| ios      | 抽象基类       | iostream |
| istream  | 输入流基类     | iostream |
| ostream  | 输出流基类     | iostream |
| iostream | 输入输出流基类 | iostream |
| ifstream | 文件输入流     | fstream  |
| ofstream | 文件输出流     | fstream  |
| fstream  | 文件输入输出流 | fstream  |

继承关系概要：`ios` → `istream` / `ostream` → `iostream`；文件流分别继承对应的流基类。

常用头文件：`<iostream>`（标准流）、`<fstream>`（文件）、`<iomanip>`（格式化控制符）。

`<<` / `>>` 在 iostream 中被重载为插入 / 提取运算符，用于标准类型的输入输出。

### 二、标准流

#### 2.1 四个标准流对象

| 对象 | 含义     | 设备 | 缓冲特点     |
| ---- | -------- | ---- | ------------ |
| cin  | 标准输入 | 键盘 | 有缓冲       |
| cout | 标准输出 | 屏幕 | 有缓冲       |
| cerr | 标准错误 | 屏幕 | **无缓冲**，不可重定向到文件（调试错误信息常用） |
| clog | 标准日志 | 屏幕 | 有缓冲       |

```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cout << "请输入两个整数：";
    cin >> a >> b;
    cout << "和为：" << (a + b) << endl;  // endl：换行并刷新
    cerr << "若出错，用 cerr 直接打到屏幕\n";
    return 0;
}
```

`cout` 会按类型自动选择重载；插入 `endl` 会刷新缓冲区，仅 `"\n"` 通常不强制刷新。

#### 2.2 cin 常用成员

| 成员            | 作用 |
| --------------- | ---- |
| `get()`         | 读一个字符（含空白） |
| `get(buf, n)`   | 读最多 n-1 个字符到数组 |
| `getline(buf,n)`| 读一行（遇换行结束） |
| `ignore(n)`     | 丢弃缓冲区中最多 n 个字符 |
| `peek()`        | 查看下一个字符，不取走 |
| `putback(ch)`   | 把字符放回缓冲区 |
| `fail()`/`clear()` | 检查 / 复位错误状态 |

```cpp
void demo_cin() {
    char buf[1024] = {};
    cin.ignore(2);           // 跳过前 2 个字符
    cin.getline(buf, 1024);
    cout << buf << endl;

    char ch = cin.peek();    // 偷窥，不消费
    if (ch >= '0' && ch <= '9') {
        int number;
        cin >> number;
        cout << "数字:" << number << endl;
    } else {
        cin.getline(buf, 64);
        cout << "字符串:" << buf << endl;
    }
}
```

#### 2.3 格式化输出要点

输出侧常用：`put(ch)` 写字符、`write(buf, n)` 写指定字节、`flush()` 刷新。

格式化有两种途径：

1. **控制符**（需 `<iomanip>`）：`setw`、`setprecision`、`fixed`、`hex`/`oct`/`dec`、`left`/`right` 等  
2. **成员函数**：`width()`、`precision()`、`setf()` / `unsetf()` 等

```cpp
#include <iomanip>
cout << hex << 255 << endl;                    // ff
cout << dec << fixed << setprecision(2) << 3.14159 << endl;  // 3.14
cout << setw(8) << setfill('0') << 42 << endl; // 00000042
```

### 三、std::string 常用操作

头文件：`#include <string>`。用分类示例代替完整 API 表。

#### 遍历

```cpp
string s = "Hello";
for (char c : s) cout << c << ' ';
```

#### 截取

```cpp
string str = "Hello, world!";
string part1 = str.substr(0, 5);  // "Hello"
string part2 = str.substr(7);     // "world!"
```

#### 比较

```cpp
if (str1 == str2) { /* 相等 */ }
int cmp = str1.compare(str2);     // <0 / 0 / >0
```

#### 查找与替换

```cpp
string str = "Hello, world!";
size_t pos = str.find("world");
if (pos != string::npos)
    str.replace(pos, 5, "C++");   // "Hello, C++!"
```

#### 插入与删除

```cpp
string str = "Hello, world!";
str.insert(7, "beautiful ");      // "Hello, beautiful world!"
str.erase(7, 10);                 // 从下标 7 删 10 个字符
str.clear();                      // 清空
```

#### 其他常用

- 长度：`size()` / `length()`；是否空：`empty()`
- 拼接：`+`、`+=`、`append()`
- 与 C 字符串互转：`c_str()`
- 大小写：配合 `<cctype>` 的 `toupper` / `tolower` 逐字符处理

### 四、动态内存：new / delete

#### 4.1 基本用法

```cpp
int* p = new int;       // 单个对象
*p = 42;
delete p;

int* arr = new int[10]; // 数组
delete[] arr;           // 数组必须用 delete[]
```

#### 4.2 new/delete 与 malloc/free

| 对比项     | new / delete              | malloc / free        |
| ---------- | ------------------------- | -------------------- |
| 性质       | 运算符                    | C 库函数             |
| 构造/析构  | 会调用                    | 不会                 |
| 类型       | 类型安全，自动算大小      | 需手动 `sizeof`      |
| 失败       | 抛 `std::bad_alloc`（默） | 返回 `nullptr`       |
| 推荐场景   | C++ 对象优先用 new/delete | 与 C 库交互时可能用到 |

#### 4.3 预防内存泄漏

- `new` 与 `delete`（`new[]` 与 `delete[]`）成对出现
- 所有返回路径都要释放（含异常路径）
- 遵循 RAII：资源获取即初始化
- **智能指针**（`unique_ptr` / `shared_ptr`）可自动释放——详情见第 06 课

### 五、文件流

#### 5.1 打开与关闭

```cpp
#include <fstream>

ofstream outfile;
outfile.open("f1.dat", ios::out);
// 或：ofstream outfile("f1.dat", ios::out);

if (!outfile) {
    cerr << "打开失败\n";
    return;
}
outfile.close();  // 解除关联，之后可再 open 其他文件
```

#### 5.2 常用打开模式

| 模式           | 含义           |
| -------------- | -------------- |
| `ios::in`      | 读             |
| `ios::out`     | 写（默认截断） |
| `ios::app`     | 追加           |
| `ios::ate`     | 打开后定位到末尾 |
| `ios::trunc`   | 截断已有内容   |
| `ios::binary`  | 二进制模式     |

可用 `|` 组合，例如：`ios::in | ios::binary`。互斥模式不要一起用。打开失败时流对象为假，可用 `if (!fsm)` 判断。

#### 5.3 ASCII 文本读写

文本文件按字符存储。可用 `<<` / `>>`，或 `get` / `getline` / `put`。

```cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ifstream ism("source.txt", ios::in);
    ofstream osm("target.txt", ios::out);
    if (!ism) {
        cerr << "打开失败!\n";
        return 1;
    }

    string line;
    while (getline(ism, line)) {  // 推荐：按行读到 string
        cout << line << endl;
        osm << line << endl;
    }
    ism.close();
    osm.close();
    return 0;
}
```

#### 5.4 二进制 read / write

二进制按内存映像读写字节，打开时加 `ios::binary`。

```cpp
istream& read(char* buffer, streamsize len);
ostream& write(const char* buffer, streamsize len);
```

```cpp
#include <iostream>
#include <fstream>
#include <cstring>
using namespace std;

class Person {
public:
    Person() = default;
    Person(const char* name, int age) {
        strncpy(mName, name, sizeof(mName) - 1);
        mAge = age;
    }
    char mName[64]{};
    int mAge{};
};

int main() {
    const char* fileName = "person.bin";

    {
        ofstream osm(fileName, ios::out | ios::binary);
        Person p1("Tim", 33), p2("Edward", 34);
        osm.write(reinterpret_cast<const char*>(&p1), sizeof(Person));
        osm.write(reinterpret_cast<const char*>(&p2), sizeof(Person));
    }

    {
        ifstream ism(fileName, ios::in | ios::binary);
        if (!ism) {
            cerr << "打开失败!\n";
            return 1;
        }
        Person p3, p4;
        ism.read(reinterpret_cast<char*>(&p3), sizeof(Person));
        ism.read(reinterpret_cast<char*>(&p4), sizeof(Person));
        cout << "Name:" << p3.mName << " Age:" << p3.mAge << endl;
        cout << "Name:" << p4.mName << " Age:" << p4.mAge << endl;
    }
    return 0;
}
```

注意：含虚函数、指针成员的类不宜直接按字节读写；跨平台还需考虑对齐与字节序。

---

## 课堂小结

1. 流是数据的传输抽象；标准流与文件流分属不同头文件与类
2. `cin` 的 `get`/`getline`/`ignore`/`peek`/`putback` 处理缓冲细节；格式化用 `<iomanip>`
3. `string` 用遍历、截取、比较、替换、插入、删除等分类掌握即可
4. C++ 优先 `new`/`delete`；配对释放，后续用智能指针更安全
5. 文本用 `<<`/`>>`/`getline`；二进制用 `read`/`write` 并指定 `ios::binary`

---

## 随堂练习

1. **文本读写**  
   创建含若干行字符串的文本文件；编写程序读出并打印到控制台；再追加若干行写回文件。

2. **二进制读写**  
   定义结构体或类（仅含普通数据成员），写入二进制文件后再读回并打印验证。

3. **追加与截断（选做）**  
   用 `ios::app` 向文件末尾追加；另写程序以截断方式打开并只保留部分内容（或重写前若干行）。
