#include <bits/stdc++.h>
using namespace std;

template <typename T> T load() { T r; cin >> r; return r; }
template <typename T> vector<T> loadMany(int n) { vector<T> rs(n); generate(rs.begin(), rs.end(), &load<T>); return rs; }

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    auto a = load<int>();
	auto b = load<int>();
	cout << a + b << '\n';
}
