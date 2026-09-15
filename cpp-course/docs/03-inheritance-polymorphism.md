# 03 继承与多态

## 课程目标

1. 理解继承概念，掌握派生类定义与三种继承方式
2. 掌握继承中的构造/析构顺序、同名成员隐藏、`final` 用法
3. 理解多继承二义性、菱形继承与虚继承
4. 掌握静态/动态多态、虚函数、虚析构与虚表原理
5. 会用抽象类与纯虚函数；区分重载、重定义、重写

---

## 核心内容

### 一、继承概念

继承：在已有类（基类/父类）基础上构造新类（派生类/子类），复用属性和方法并扩展新功能。继承是实现多态的基础。

派生类成员分两部分：从基类继承的 + 自己新增的。

**例：网页 NewsPage（不用继承 vs 用继承）**

```cpp
#include <iostream>
#include <string>
using namespace std;

class IndexPage {
public:
    void Header()          { cout << "网页头部!" << endl; }
    void LeftNavigation()  { cout << "左侧导航菜单!" << endl; }
    void MainBody()        { cout << "首页主体内容!" << endl; }
    void Footer()          { cout << "网页底部!" << endl; }
private:
    string mTitle;
};

#if 0
// 不用继承：重复抄写已有代码
class NewsPage {
public:
    void Header()         { cout << "网页头部!" << endl; }
    void LeftNavigation() { cout << "左侧导航菜单!" << endl; }
    void MainBody()       { cout << "新闻网页主体内容!" << endl; }
    void Footer()         { cout << "网页底部!" << endl; }
private:
    string mTitle;
};
#else
// 用继承：只改不同的主体部分
class NewsPage : public IndexPage {
public:
    void MainBody() { cout << "新闻网页主体内容!" << endl; }
};
#endif

int main() {
    NewsPage page;
    page.Header();
    page.MainBody();
    page.LeftNavigation();
    page.Footer();
    return 0;
}
```

### 二、派生类定义与继承方式

**格式：**

```cpp
class 派生类名 : 继承方式 基类名 {
    // 新增成员
};
```

未指定继承方式时，`class` 默认为 `private` 继承。

**单继承**：只直接继承一个基类。  
**多继承**：直接继承多个基类。

#### 三种继承方式权限表

| 基类成员 \ 继承方式 | public 继承 | protected 继承 | private 继承 |
| ------------------- | ----------- | -------------- | ------------- |
| public              | public      | protected      | private       |
| protected           | protected   | protected      | private       |
| private             | 不可访问    | 不可访问       | 不可访问      |

要点：基类 `private` 成员任何继承方式下派生类都不可直接访问；继承方式只改变基类 `public`/`protected` 成员在派生类中的可见性。

```cpp
class A {
public:    int mA;
protected: int mB;
private:   int mC;
};

// public 继承：对外仍暴露基类 public
class B : public A {
public:
    void PrintB() {
        cout << mA << endl;   // OK
        cout << mB << endl;   // OK
        // cout << mC;        // 基类 private 不可访问
    }
};
class SubB : public B {
    void Print() { cout << mA << mB; }  // 仍可访问
};

// private 继承：基类 public/protected 在本类中变为 private
class C : private A {
public:
    void PrintC() { cout << mA << mB; }  // 本类内部 OK
};
class SubC : public C {
    void Print() {
        // mA、mB 均不可访问（已成为 C 的 private）
    }
};

// protected 继承：基类 public 降为 protected，类外不可见
class D : protected A {
public:
    void PrintD() { cout << mA << mB; }
};

void test() {
    B b;  cout << b.mA;   // OK
    // cout << b.mB;      // protected，类外不可
    C c;  // cout << c.mA; // private 继承，类外不可
    D d;  // cout << d.mA; // protected 继承，类外不可
}
```

### 三、final：禁用继承 / 重写

C++11 的 `final`：

1. 标在类名后 → 禁止被继承  
2. 标在虚函数后 → 禁止再被覆盖

```cpp
class TaskManager final { /* ... */ };
// class Prioritized : public TaskManager {};  // 错误

class Base {
public:
    virtual void func() const;
};

class Derived : public Base {
public:
    void func() const override final;  // OK
};

class Derived2 : public Derived {
public:
    // void func() const;  // 错误：Derived::func 已 final
};
```

### 四、构造 / 析构与同名成员

#### 4.1 调用顺序

- 构造：先基类，后派生类（多层则自顶向下）
- 析构：与构造相反（先派生类，后基类）
- 基类构造有参数时，须在派生类初始化列表中**显式**调用

```cpp
class Base {
public:
    Base() { x = 0; y = 0; }
    Base(int a, int b) { x = a; y = b; }
private:
    int x, y;
};

class Derived : public Base {
public:
    Derived() : Base() { z = 0; }
    Derived(int a, int b, int c) : Base(a, b) { z = c; }
private:
    int z;
};
```

对象模型可理解为：派生类 = 基类成员 + 新增成员（按继承层次叠加）。可用 `sizeof` 验证成员累加（注意对齐）。

创建多层对象时：构造 `A → B → C`；析构相反 `C → B → A`。基类无默认构造时，派生类须在初始化列表显式调用带参构造。

#### 4.2 同名成员与隐藏

- 派生类与基类同名时，默认访问派生类成员（就近）
- 访问基类同名成员：用 `基类名::成员`
- 在派生类中重定义基类某个重载函数时，基类同名的**其他重载版本全部被隐藏**

```cpp
class Base {
public:
    Base() : mParam(0) {}
    void func1() { cout << "Base::func1()\n"; }
    void func1(int) { cout << "Base::func1(int)\n"; }
    void myfunc() { cout << "Base::myfunc\n"; }
    int mParam;
};

class Derived1 : public Base {
public:
    void myfunc() { cout << "Derived1::myfunc\n"; }  // 仅隐藏 myfunc
};

class Derived2 : public Base {
public:
    void func1(int, int) {}  // 隐藏 Base 的两个 func1
};

class Derived : public Base {
public:
    Derived() : mParam(10) {}
    void Print() {
        cout << Base::mParam << endl;  // 基类
        cout << mParam << endl;        // 派生类
    }
    int& getBaseParam() { return Base::mParam; }
    int mParam;
};
// Derived1 仍可调用 func1()/func1(int)；Derived2 只能调 func1(int,int)
```

#### 4.3 不可自动继承的函数

构造函数、析构函数、`operator=` **不能被继承**，须为每个派生类单独提供（未写时编译器可能自动生成）。

静态成员可被继承；重定义静态函数同样会隐藏基类同名重载。静态成员函数**不能**是虚函数。

```cpp
class Base {
public:
    static int getNum() { return sNum; }
    static int getNum(int p) { return sNum + p; }
    static int sNum;
};
int Base::sNum = 10;

class Derived : public Base {
public:
    static int sNum;  // 隐藏基类同名静态数据
    static void getNum(int a, int b) {
        cout << sNum + a + b << endl;  // 隐藏基类全部 getNum
    }
};
int Derived::sNum = 20;
```

### 五、多继承、菱形继承与虚继承

#### 5.1 多继承二义性

多个基类有同名成员时，须用作用域限定：

```cpp
class Base1 { public: void func1() { cout << "Base1\n"; } };
class Base2 {
public:
    void func1() { cout << "Base2\n"; }
    void func2() { cout << "Base2::func2\n"; }
};

class Derived : public Base1, public Base2 {};

// derived.func1();          // 二义性
derived.Base1::func1();      // OK
derived.Base2::func1();      // OK
```

#### 5.2 菱形继承

两个中间类继承同一基类，再被同一派生类继承 → 成员重复、访问二义。

**虚继承**解决：中间类虚继承公共祖先，最终对象中只保留一份虚基类子对象。

```cpp
class BigBase {
public:
    BigBase() { mParam = 0; }
    void func() { cout << "BigBase::func\n"; }
    int mParam;
};

class Base1 : virtual public BigBase {};
class Base2 : virtual public BigBase {};
class Derived : public Base1, public Base2 {};

// derived.func(); derived.mParam;  // 无二义，只一份数据
```

**原理简述：**

- 普通菱形继承：`Derived` 中有两份 `BigBase`，访问需 `Base1::mParam` 限定
- 虚继承后：对象内有 `vbptr`（虚基类指针）指向偏移表，定位**唯一**共享虚基类子对象
- 虚基类由**最终派生类**负责初始化；中间类初始化列表里对虚基类的构造不真正执行

```cpp
class BigBase {
public:
    BigBase(int x) { mParam = x; }
    int mParam;
};
class Base1 : virtual public BigBase {
public:
    Base1() : BigBase(10) {}   // 创建 Derived 时不真正调用
};
class Base2 : virtual public BigBase {
public:
    Base2() : BigBase(10) {}
};
class Derived : public Base1, public Base2 {
public:
    Derived() : BigBase(10) {} // 最终派生类初始化虚基类
};
```

> 虚继承只解决“有公共祖先”的菱形问题。工程中尽量用单继承替代多继承。

### 六、多态

#### 6.1 静态多态 vs 动态多态

| 类型     | 实现方式           | 绑定时机       |
| -------- | ------------------ | -------------- |
| 静态多态 | 函数重载、运算符重载 | 编译期（早绑定） |
| 动态多态 | 虚函数             | 运行期（晚绑定） |

静态多态示例：同名函数按参数个数/类型区分（仅返回值不同不能构成重载）。

#### 6.2 虚函数条件与用法

构成动态多态的条件：

1. 基类声明虚函数，派生类**重写**（函数名、参数、返回值一致；协变返回允许父子指针/引用）
2. 通过**基类指针或引用**调用虚函数

```cpp
class Base {
public:
    virtual void show() { cout << "I am base!\n"; }
    virtual ~Base() { cout << "~Base\n"; }
};

class Derived1 : public Base {
public:
    void show() override { cout << "I am Derived1\n"; }
};

int main() {
    Base* p = new Derived1;
    p->show();   // 调用 Derived1::show
    delete p;
    return 0;
}
```

- 派生类同名虚函数可不写 `virtual`，建议写 `override`
- 普通调用看对象静态类型；多态调用看指针/引用**实际指向的对象**

#### 6.3 虚析构的必要性

基类指针删除派生类对象时，若析构非虚，只调基类析构 → 派生类资源泄漏。

```cpp
class Base {
public:
    virtual void show() { cout << "base\n"; }
    virtual ~Base() { cout << "~Base\n"; }  // 必须为虚
};
class Derived1 : public Base {
public:
    void show() override { cout << "Derived1\n"; }
    ~Derived1() { cout << "~Derived1\n"; }
};
// Base* b = new Derived1; delete b;
// 非虚析构只打印 ~Base；虚析构打印 ~Derived1 再 ~Base
```

基类若可能被多态删除，析构应声明为 `virtual`（哪怕函数体为空）。

### 七、虚函数表原理（精简）

- 含虚函数的类有一张**虚函数表（vtable）**，存放各虚函数入口地址
- 每个对象有一个**虚表指针（vfptr）**，指向所属类的 vtable
- 派生类先拷贝基类虚表，再对重写项覆盖为派生类函数地址
- 虚函数本身在代码段；对象里存的是虚表指针，不是整张表
- 调用时：取 `vfptr` → 查表 → 跳转（晚绑定）

```cpp
class A {
public:
    virtual void Print1() {}
    virtual void Print2() {}
    void Print3() {}   // 非虚，不进虚表
    int _a;
};
// 64 位下 sizeof(A) 常为 16：8(vfptr)+4(int)+对齐

class B : public A {
public:
    void Print1() override {}  // 虚表槽位改为 B::Print1
    int _b;
};
```

多个虚函数只增加表项，不按个数倍增对象大小。

### 八、抽象类与纯虚函数

纯虚函数：`virtual 返回类型 函数名(参数) = 0;`  
含至少一个纯虚函数的类为**抽象类**，不能实例化。派生类必须实现全部纯虚函数，否则仍是抽象类。

用途：定义统一接口，强制子类实现具体行为。

**模板方法模式（饮品精简例）：**

```cpp
class AbstractDrinking {
public:
    virtual void Boil() = 0;
    virtual void Brew() = 0;
    virtual void PourInCup() = 0;
    virtual void PutSomething() = 0;

    void MakeDrink() {   // 固定流程，步骤由子类实现
        Boil();
        Brew();
        PourInCup();
        PutSomething();
    }
    virtual ~AbstractDrinking() = default;
};

class Coffee : public AbstractDrinking {
public:
    void Boil() override         { cout << "煮农夫山泉!\n"; }
    void Brew() override         { cout << "冲泡咖啡!\n"; }
    void PourInCup() override    { cout << "倒入杯中!\n"; }
    void PutSomething() override { cout << "加入牛奶!\n"; }
};

class Tea : public AbstractDrinking {
public:
    void Boil() override         { cout << "煮自来水!\n"; }
    void Brew() override         { cout << "冲泡茶叶!\n"; }
    void PourInCup() override    { cout << "倒入杯中!\n"; }
    void PutSomething() override { cout << "加入柠檬!\n"; }
};

void DoBusiness(AbstractDrinking* drink) {
    drink->MakeDrink();
    delete drink;
}
```

注意：普通函数、静态成员函数、构造函数不能是虚函数；内联也不适合做虚函数；析构可以且常应声明为虚。

### 九、重载 / 重定义 / 重写对照

| 概念           | 条件要点 |
| -------------- | -------- |
| **重载**       | 同一作用域；参数个数/类型/顺序不同；与返回值无关；`const` 可参与重载 |
| **重定义（隐藏）** | 有继承；派生类定义与基类同名的**非虚**成员（甚至只改参数也会隐藏全部同名重载） |
| **重写（覆盖）**   | 有继承；派生类重写基类 **virtual** 函数；函数名、参数、返回值一致（协变除外） |

```cpp
class A {
public:
    void func1() {}
    void func1(int) {}   // 重载
    void func2() {}
    virtual void func3() {}
};

class B : public A {
public:
    void func2() {}           // 重定义（隐藏）
    void func3() override {}  // 重写（覆盖）
};
```

---

## 课堂小结

1. 继承复用基类代码；三种继承方式用权限表记忆
2. 构造自顶向下、析构相反；同名默认就近，`::` 访问基类；构造/析构/`=` 不继承
3. 多继承注意二义性；菱形继承用虚继承共享一份基类
4. 动态多态 = 虚函数重写 + 基类指针/引用；基类析构宜为虚
5. 抽象类定义接口；区分重载、隐藏、覆盖

---

## 随堂练习

**作业：用开闭原则改造计算器**

先看不利于扩展的写法（改功能要改源码中的分支）：

```cpp
class Calculator {
public:
    void setA(int a) { mA = a; }
    void setB(int b) { mB = b; }
    void setOperator(string op) { mOperator = op; }
    int getResult() {
        if (mOperator == "+") return mA + mB;
        if (mOperator == "-") return mA - mB;
        if (mOperator == "*") return mA * mB;
        if (mOperator == "/") return mA / mB;
        return 0;
    }
private:
    int mA{}, mB{};
    string mOperator;
};
```

开闭原则（对修改关闭、对扩展开放）——用抽象基类 + 派生类：

```cpp
class AbstractCalculator {
public:
    void setA(int a) { mA = a; }
    void setB(int b) { mB = b; }
    virtual int getResult() = 0;
    virtual ~AbstractCalculator() = default;
protected:
    int mA{}, mB{};
};

class PlusCalculator : public AbstractCalculator {
public:
    int getResult() override { return mA + mB; }
};

class MinusCalculator : public AbstractCalculator {
public:
    int getResult() override { return mA - mB; }
};

class MultipliesCalculator : public AbstractCalculator {
public:
    int getResult() override { return mA * mB; }
};

void DoBusiness(AbstractCalculator* calc) {
    calc->setA(10);
    calc->setB(20);
    cout << "结果：" << calc->getResult() << endl;
    delete calc;
}

// 扩展除法：新增 DivideCalculator 即可，无需改原有类
```

要求：自行补全除法计算器，并用基类指针分别测试加减乘除。
