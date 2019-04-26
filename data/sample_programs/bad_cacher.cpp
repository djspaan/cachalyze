#include <iostream>

#define N 500

void fill(int arr[N][N][N]) {
    for (int k = 0; k < N; ++k) {
        for (int l = N - 1; l >= 0; --l) {
            for (int m = N - 1; m >= 0; --m) {
                arr[m][l][k] = m + l + k + 3;
            }
        }
    }
}

int main() {
    long int res;
    auto arr = new int[N][N][N]();

    fill(arr);

    for (int k = 0; k < N; ++k) {
        for (int l = N - 1; l >= 0; --l) {
            for (int m = N - 1; m >= 0; --m) {
                res += arr[m][l][k];
            }
        }
    }

    std::cout << res << std::endl;

    return 0;
}
