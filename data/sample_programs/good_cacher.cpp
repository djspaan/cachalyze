#include <iostream>

#define N 500

void fill(int arr[N][N]) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            arr[i][j] = i+j+2;
        }
    }
}

int main() {
    long int res;

    auto arr = new int[N][N][N]();

    for (int i = 0; i < N; ++i) {
       fill(arr[i]);
    }


    for (int k = 0; k < N; ++k) {
        for (int l = 0; l < N; ++l) {
            for (int m = 0; m < N; ++m) {
                res += arr[k][l][m];
            }
        }
    }

    std::cout << res << std::endl;

    return 0;
}

