def main():
    v = [0, 1, 2, ]
    w = [0, 2, 3, ]
    s = [0, 2, 2, ]
    n = 2
    V = 7
    f = []
    for i in range(0, 10):
        f.append([0, ] * 10)

    for i in range(1, n + 1, 1):
        for j in range(0, V + 1, 1):
            for k in range(0, s[i] + 1, 1):
                if k * v[i] <= j:
                    f[i][j] = max(f[i][j], f[i - 1][j - k * v[i]] + k * w[i])

    for o_r in f:
        print(o_r)
    print(f[n][V])


if __name__ == '__main__':
    main()
