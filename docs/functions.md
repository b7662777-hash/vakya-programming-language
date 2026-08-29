# Vākya Functions & Closures

## Function Declarations (`karya`)

Functions are declared with the `karya` keyword.

### Basic Functions
```vakya
karya greet() {
    vada("Namaste!")
}

greet()
```

### Parameterized Functions with Return (`pratyavartaya`)
```vakya
karya add(a, b) {
    pratyavartaya a + b
}

chara result = add(10, 20)
vada(result) // 30
```

### Type-Annotated Signatures
```vakya
karya multiply(a: sankhya, b: sankhya) -> sankhya {
    pratyavartaya a * b
}
```

### Implicit Default Return
If execution reaches the end of a function without executing `pratyavartaya`, the function returns `shunya` (null).

## Recursion

Vākya fully supports recursive functions with call stack protection:

```vakya
karya factorial(n: sankhya) -> sankhya {
    yadi n <= 1 {
        pratyavartaya 1
    }
    pratyavartaya n * factorial(n - 1)
}

vada(factorial(5)) // 120
```

## Closures & First-Class Functions

Functions can be passed as values, returned from other functions, and capture their lexical scope:

```vakya
karya make_adder(x: sankhya) {
    karya adder(y: sankhya) -> sankhya {
        pratyavartaya x + y
    }
    pratyavartaya adder
}

chara add5 = make_adder(5)
vada(add5(10)) // 15
```
