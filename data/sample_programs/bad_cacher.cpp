#include <iostream>

#define N 8192

void fill(int **arr) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            arr[j][i] = 1;
        }
    }
}

int main() {
    int res;
    int **arr = new int*[N];

    for (int i = 0 ; i < N ; i++)
        arr[i] = new int[N];

    fill(arr);

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            res += arr[j][i];
        }
    }

    std::cout << res << std::endl;

    return 0;
}
