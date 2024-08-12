#include "parallel_calculate.h"
using namespace std;

extern "C" __declspec(dllexport) double parallel_calculate_c(double *numbers,
                                                             size_t size) {
  std::vector<double> vec(numbers, numbers + size);
  pc obj;
  return obj.parallel_calculate(vec);
}

bool pc::parallel_check(double a, double b) {
  return (abs(a - b) / (a + b) * 2.0) > 0.1 ? false : true;
}

_group pc::_find_group(int a_left, int a_right, int b_left, int b_right) {
  _group callback;
  if (a_right < b_left) {
    callback._left = -1, callback._right = -1;
  } else {
    callback._left = max(a_left, b_left);
    callback._right = min(a_right, b_right);
  }
  return callback;
}

_group pc::find_group(_data a, _data b) {
  return _find_group(a._left, a._right, b._left, b._right);
}

_group pc::find_group(_group a, _group b) {
  return _find_group(a._left, a._right, b._left, b._right);
}

double pc::parallel_calculate(std::vector<double> _numbers) {
  map<double, _data> countMap;
  vector<double> numbers = _numbers;
  // prepare data
  for (int i = 0; i < numbers.size(); i++) {
    countMap[numbers[i]].count++;
    countMap[numbers[i]].timeS += i;
  }
  // sort keys
  int i = 0;
  for (auto &_countMap : countMap) {
    numbers[i] = _countMap.first;
    _countMap.second.timeS /= _countMap.second.count;
    i++;
  }
  // find parallel
  int num_size = countMap.size();
  for (i = 0; i < num_size; i++) {
    int left_p = i - 1, right_p = i + 1;
    while (left_p >= 0) {
      if (parallel_check(numbers[left_p], numbers[i])) {
        countMap[numbers[left_p]].in_use = true;
        left_p--;
      } else {
        countMap[numbers[i]]._left = left_p + 1;
        break;
      }
    }
    while (right_p < num_size) {
      if (parallel_check(numbers[right_p], numbers[i])) {
        countMap[numbers[right_p]].in_use = true;
        right_p++;
      } else {
        countMap[numbers[i]]._right = right_p - 1;
        break;
      }
    }
    if (left_p == -1) countMap[numbers[i]]._left = 0;
    if (right_p == num_size) countMap[numbers[i]]._right = num_size - 1;
  }
  // find group
  vector<_group> groups;
  for (i = 0; i < num_size - 1; i++) {
    _group temp =
        find_group(countMap.at(numbers[i]), countMap.at(numbers[i + 1]));
    if (temp._left != -1) {
      if (!groups.empty()) {
        if (groups.back()._left != temp._left ||
            groups.back()._right != temp._right) {
          groups.push_back(temp);
        }
      } else {
        groups.push_back(temp);
      }
    }
  }
  // special situation(return -1 or num)
  if (groups.size() == 0) {
    int real_disfind_check = 0;
    double num = 0.0;
    int count = 1, time = 0;
    for (auto pair : numbers) {
      if (countMap[pair].count > count) {
        num = pair;
        count = countMap[pair].count;
        time = countMap[pair].timeS;
        real_disfind_check = 1;
      } else if ((count != 1) && (num != pair) &&
                 (countMap[pair].count == count)) {
        if (countMap[pair].timeS > time) {
          num = pair;
          count = countMap[pair].count;
          time = countMap[pair].timeS;
          real_disfind_check = 1;
        } else if (countMap[pair].timeS == time) {
          real_disfind_check = 2;
        }
      }
    }
    if (real_disfind_check == 0) return -1;
    if (real_disfind_check == 1) return num;
    if (real_disfind_check == 2) return -2;
  }
  // deduplicate && deoverlap
  bool overlap_check = false;
  while (!overlap_check) {
    vector<_group> temp_groups;
    overlap_check = true;
    int num_size = groups.size();
    for (int j = 0; j < num_size - 1; j++) {
      _group temp = find_group(groups[j], groups[j + 1]);
      if (temp._left != -1) {
        overlap_check = false;
        temp_groups.push_back(temp);
      } else {
        temp_groups.push_back(groups[j + 1]);
      }
    }
    if (!overlap_check) {
      groups.assign(temp_groups.begin(), temp_groups.end());
    }
  }
  // calculate
  map<double, double> resMap;
  for (auto &pair : groups) {
    double sum = 0.0, timeS = 0.0;
    int counter = 0;
    for (i = pair._left; i <= pair._right; i++) {
      sum += numbers[i] * countMap[numbers[i]].count;
      timeS += countMap[numbers[i]].timeS;
      counter += countMap[numbers[i]].count;
    }
    sum /= counter;
    timeS /= counter;
    resMap[timeS] = sum;
  }
  // return
  return resMap.rbegin()->second;
}
