#ifndef PARALLEL_CALCULATE_H
#define PARALLEL_CALCULATE_H

#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>

struct _data {
  int count = 0;
  int timeS = 0;
  int _left, _right;
  bool in_use = false;
};

struct _group {
  int _left, _right;
};

class pc {
 public:
  bool parallel_check(double a, double b);
  _group _find_group(int a_left, int a_right, int b_left, int b_right);
  _group find_group(_data a, _data b);
  _group find_group(_group a, _group b);
  double parallel_calculate(std::vector<double> _numbers);
};

#endif
