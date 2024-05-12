Yet another implementation of a lox interpreter

# pylox

To fire it up:
```
$python3 lox.py 
> var num = 4;
> print num;
4

python3 lox.py <program>
```
You can find some examples in the examples folder

## Arrays

```
var a[5] = 10;
print(a[2] * a[3]);
100

var b = 2;

a[b] = b + 5;
print(a[b]);
7

for(var i = 0; i < 5; i = i + 1)
{
 a[i] = i * 2;
 print(a[i])
}
0
2
4
6
8
```

## Variables
```
var a = 4;
var b = 5;
print a + b;
9

var c = "Hello";
var d = "World!";
print c + " " + d;
Hello World!

var e = true;
print e;
true 

var f = nil;
print f;
nil
```

## Control Flow
```
var a = 1;

if (a > 0){
    print "Positive Number";
  }
  else {
      print "Negative Number";
    }
"Positive Number"
```

## Loops
```
var i = 0;
while (i < 10) {
    print i;
    i = i + 1;
  }

for (var i = 0; i < 10; i = i + 1) {
    print i;
  }
```

## Functions
```
fun square(a) {
    print a * a;
  }

square(5); // 25
```

## Recursion
```
fun isEven(n) {
  if (n == 0) return true;
  return isOdd(n - 1);
}

fun isOdd(n) {
  if (n == 0) return false;
  return isEven(n - 1);
}

print isEven(4); true
print isOdd(2); false
```

## Classes
```
class Rectangle {
  init(h, w) {
    this.h  = h;
    this.w   = w;
  }
  perimeter()    { return 2 * (this.h + this.w); }
  area() { return this.h * this.w; }
}

var r = Rectangle(2, 4);
print(r.perimeter());
print(r.area());

class Square < Rectangle{
  init(w) {
    super.init(w,w);
  }
  perimeter()    { return super.perimeter(); }
  area() { return this.w * this.w; }
}

var s = Square(2);
print(s.perimeter());
print(s.area());
```
