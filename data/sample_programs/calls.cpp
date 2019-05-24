#include <iostream>

int func2() {
    for (int i = 0; i < 1000; ++i) {
        std::cout << ' ';
    }

    return 1;
}

int func1() {
    int c = 1;

    for (int i = 0; i < 1000; ++i) {
        c++;
    }

    return c + func2();
}


int main() {
    int a = 1;

    int b = a + func1() + func2() + func2();

    for (int i = 0; i < 1000; ++i) {
        b++;
    }

    std::cout << b << std::endl;

    return b;
}

