# 05 函数模板与类模板

## 课程目标

- 理解模板与泛型编程的目的
- 掌握函数模板的定义、重载与调用规则
- 理解模板实现机制与局限性，会写显式具体化
- 掌握类模板、成员函数模板、非类型参数与派生关系
- 了解类模板的友元与静态成员
- 能用类模板实现简易动态数组 `MyArray`

---

## 核心内容

### 一、模板与泛型

C++ 提高代码复用主要靠 **继承** 与 **模板**。模板是对**类型参数化**的工具，用来编写与具体类型无关的通用代码（泛型编程）。

要点：

1. 模板对类型进行参数化
2. 两种机制：函数模板、类模板
3. 函数模板：参数类型不同、函数体相同
4. 类模板：数据成员/成员函数类型不同、结构相同
5. 模板声明/定义只能在全局、命名空间或类范围内，不能在函数内定义模板

---

### 二、函数模板

#### 2.1 通式

```cpp
template <class T>          // 或 typename T，二者等价
返回类型 函数名(参数列表) {
    // 函数体
}
```

`< >` 中是模板形参，不能为空。调用时由编译器根据实参推演类型并实例化。

#### 2.2 交换与求最大值

```cpp
template <class T>
void mySwap(T& a, T& b) {
    T tmp = a;
    a = b;
    b = tmp;
}

template <typename T>
T MaxElement(T a[], int size) {
    T tmpMax = a[0];
    for (int i = 1; i < size; ++i) {
        if (tmpMax < a[i]) tmpMax = a[i];
    }
    return tmpMax;
}

int main() {
    int n = 1, m = 2;
    mySwap(n, m);           // 推演为 int
    mySwap<double>(1.2, 2.3); // 显式指定类型也可
    int arr[] = {3, 1, 9, 4};
    cout << MaxElement(arr, 4) << endl;
}
```

#### 2.3 多类型参数

```cpp
template <class T1, class T2>
T2 MyFun(T1 arg1, T2 arg2) {
    cout << arg1 << " " << arg2 << endl;
    return arg2;
}
```

#### 2.4 函数模板重载

形参表或类型参数表不同即可重载：

```cpp
template <class T1, class T2>
void print(T1 a, T2 b) { cout << a << " " << b << endl; }

template <class T>
void print(T a, T b) { cout << a << " " << b << endl; }
```

#### 2.5 与普通函数的匹配优先级

同名时，编译器按以下顺序匹配：

1. 参数完全匹配的**普通函数**
2. 参数完全匹配的**模板函数**
3. 经隐式转换后可匹配的普通函数
4. 都找不到则报错

```cpp
template <class T>
T Max(T a, T b) { cout << "TemplateMax\n"; return a; }

template <class T, class T2>
T Max(T a, T2 b) { cout << "TemplateMax2\n"; return a; }

double Max(double a, double b) { cout << "MyMax\n"; return a; }

int main() {
    int i = 4, j = 5;
    Max(1.2, 3.4);  // MyMax（普通函数）
    Max(i, j);      // TemplateMax
    Max(1.2, 3);    // TemplateMax2
}
```

补充规则：

- 普通函数与模板都能匹配时，**优先普通函数**
- `MyPlus<>(a, b)` 空模板实参列表可强制走模板
- 若模板能产生更好匹配，则选模板

#### 2.6 模板不允许隐式转换

函数模板要求类型严格匹配；普通函数可以进行隐式转换。

```cpp
template <class T>
T myFunction(T a, T b) { return a; }

myFunction(5, 7);      // OK → int
myFunction(5.8, 8.4);  // OK → double
// myFunction(5, 8.4); // 错误：无法推演出统一的 T
```

---

### 三、模板实现机制（精简）

编译器**不是**生成一个“能处理任意类型”的函数，而是：

- 按具体类型生成不同实例
- 对模板进行**两次编译**：声明处编译模板本身；调用处对替换类型后的代码再编译

---

### 四、局限性与显式具体化

通用模板假设 `=`、`<` 等运算符对 `T` 有意义。若 `T` 是数组、自定义类等，可能不成立。解决办法：为特定类型提供**显式具体化**（优先于常规模板）。

```cpp
class Person {
public:
    Person(string name, int age) : mName(name), mAge(age) {}
    string mName;
    int mAge;
};

template <class T>
void mySwap(T& a, T& b) {
    T temp = a; a = b; b = temp;
}

// 显式具体化：以 template<> 开头
template <>
void mySwap<Person>(Person& p1, Person& p2) {
    swap(p1.mName, p2.mName);
    swap(p1.mAge, p2.mAge);
}
```

---

### 五、类模板

#### 5.1 Pair 例子

```cpp
template <class T1, class T2>
class Pair {
public:
    Pair(T1 k, T2 v) : m_key(k), m_value(v) {}
    bool operator<(const Pair<T1, T2>& p) const;
private:
    T1 m_key;
    T2 m_value;
};

template <class T1, class T2>
bool Pair<T1, T2>::operator<(const Pair<T1, T2>& p) const {
    return m_value < p.m_value;
}

int main() {
    Pair<string, int> a("Jay", 20);
    Pair<string, int> b("Tom", 21);
    cout << (a < b) << endl;  // 1
}
```

定义对象：`类模板名<真实类型...> 对象名(构造实参...);`

注意：`Pair<string, int>` 与 `Pair<string, double>` 是**不同的类**，互不兼容。

#### 5.2 成员函数模板

```cpp
template <class T>
class A {
public:
    template <class T2>
    void Func(T2 t) { cout << t; }

    template <class T3>
    void Func2(T3 t);
};

template <class T>
template <class T3>
void A<T>::Func2(T3 t) { /* ... */ }

int main() {
    A<int> a;
    a.Func('K');
    a.Func("hello");  // 按实参分别实例化
}
```

#### 5.3 非类型参数

```cpp
template <class T, int size>
class CArray {
public:
    void Print() {
        for (int i = 0; i < size; ++i) cout << array[i] << endl;
    }
private:
    T array[size];
};

CArray<double, 40> a2;
CArray<int, 50> a3;  // 与 a2 属于不同的类
```

#### 5.4 类模板与派生（四种情况）

**① 类模板从类模板派生**

```cpp
template <class T1, class T2>
class Base { T1 v1; T2 v2; };

template <class T1, class T2>
class Derived : public Base<T2, T1> { T1 v3; T2 v4; };

Derived<int, double> obj;
```

**② 类模板从模板类（已实例化）派生**

```cpp
template <class T1, class T2>
class A { T1 v1; T2 v2; };

template <class T>
class B : public A<int, double> { T v; };

B<char> obj;
```

**③ 类模板从普通类派生**

```cpp
class A { int v1; };

template <class T>
class B : public A { T v; };

B<char> obj;
```

**④ 普通类从模板类派生**

```cpp
template <class T>
class A { T v1; };

class B : public A<int> { double v; };

B obj;
```

---

### 六、类模板与友元、静态成员

#### 6.1 友元（要点 + 短例）

- 普通函数、普通类、类的成员函数都可作为类模板的友元；对所有实例生效
- 函数模板也可作为类模板的友元（常用于重载 `<<`）

```cpp
template <class T1, class T2>
class Pair {
    T1 key;
    T2 value;
public:
    Pair(T1 k, T2 v) : key(k), value(v) {}
    template <class T3, class T4>
    friend ostream& operator<<(ostream& o, const Pair<T3, T4>& p);
};

template <class T3, class T4>
ostream& operator<<(ostream& o, const Pair<T3, T4>& p) {
    return o << "(" << p.key << "---" << p.value << ")";
}
```

类模板也可作为另一个类模板的友元：`template <class T2> friend class A;`

#### 6.2 静态成员（要点 + 短例）

每个**模板实例类**拥有自己独立的一份静态成员（`A<int>` 与 `A<double>` 的 `count` 互不影响）。

```cpp
template <class T>
class A {
    static int count;
public:
    A() { ++count; }
    ~A() { --count; }
    static void PrintCount() { cout << count << endl; }
};

template <> int A<int>::count = 0;
template <> int A<double>::count = 0;

int main() {
    A<int> ia;
    A<double> da;
    ia.PrintCount();  // 1
    da.PrintCount();  // 1
}
```

---

### 七、应用：MyArray 类模板

```cpp
template <class T>
class MyArray {
public:
    explicit MyArray(int capacity)
        : m_Capacity(capacity), m_Size(0), pAddress(new T[capacity]) {}

    MyArray(const MyArray& arr)
        : m_Capacity(arr.m_Capacity), m_Size(arr.m_Size),
          pAddress(new T[arr.m_Capacity]) {
        for (int i = 0; i < m_Size; ++i)
            pAddress[i] = arr.pAddress[i];
    }

    T& operator[](int index) { return pAddress[index]; }

    void Push_back(const T& val) {
        if (m_Size == m_Capacity) return;
        pAddress[m_Size++] = val;
    }

    void Pop_back() {
        if (m_Size == 0) return;
        --m_Size;
    }

    int getSize() const { return m_Size; }

    ~MyArray() {
        delete[] pAddress;
        pAddress = nullptr;
        m_Capacity = m_Size = 0;
    }

private:
    T* pAddress;
    int m_Capacity;
    int m_Size;
};
```

测试（精简）：

```cpp
MyArray<int> a(10);
for (int i = 0; i < 5; ++i) a.Push_back(i);
for (int i = 0; i < a.getSize(); ++i) cout << a[i] << " ";

MyArray<Person> pa(5);
pa.Push_back(Person("Tom", 20));
pa.Push_back(Person("Jerry", 18));
```

说明：`new T[n]` 要求 `T` 提供默认构造函数。

---

## 课堂小结

- 模板实现类型参数化，支持泛型编程
- 函数模板：通式、多参数、重载；匹配优先普通函数；不允许隐式转换
- 机制：按类型生成实例，两次编译
- 局限性可用显式具体化解决
- 类模板：成员函数模板、非类型参数、四种派生、友元与静态成员
- `MyArray` 展示类模板管理动态数组的典型写法

---

## 随堂练习

**作业：用函数模板对 `char` / `int` 数组排序**

```cpp
template <class T>
void PrintArray(T arr[], int len) {
    for (int i = 0; i < len; ++i) cout << arr[i] << " ";
    cout << endl;
}

template <class T>
void MySort(T arr[], int len) {
    for (int i = 0; i < len; ++i)
        for (int j = len - 1; j > i; --j)
            if (arr[j] > arr[j - 1])
                swap(arr[j], arr[j - 1]);
}

void test() {
    char cs[] = "aojtifysn";
    int  is[] = {7, 4, 2, 9, 8, 1};
    MySort(cs, (int)strlen(cs));
    MySort(is, 6);
    PrintArray(cs, (int)strlen(cs));
    PrintArray(is, 6);
}
```
