#include <iostream>

#define N 500

void fill(int arr[N][N][N]) {
    for (int k = 0; k < N; ++k) {
        for (int l = 0; l < N; ++l) {
            for (int m = 0; m < N; ++m) {
                arr[k][l][m] = k + l + m + 3;
            }
        }
    }
}

int main() {
    long int res;
    auto arr = new int[N][N][N]();

    fill(arr);

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
