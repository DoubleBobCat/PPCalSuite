#include <iostream>
#include <vector>

#include "parallel_calculate.h"
using namespace std;
int main() {
  pc _pc;
  vector<double> num;
  num.push_back(1.0);
  num.push_back(1.0);
  num.push_back(17.0);
  double ans = 0.0;
  cout << "part 1\n";
  ans = _pc.parallel_calculate(num);
  cout << ans << "\n";
  cout << "part 2\n";
  return 0;
}