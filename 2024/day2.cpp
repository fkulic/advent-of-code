#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

std::vector<std::vector<int>> FileToVector(const std::string& filename)
{
    std::vector<std::vector<int>> result;
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Could not open file: " << filename << std::endl;
        std::terminate();
    }

    std::string line;
    while (std::getline(file, line)) {
        std::vector<int> row;
        std::istringstream iss(line);
        int number;
        while (iss >> number) {
            row.push_back(number);
        }
        result.push_back(row);
    }

    file.close();
    return result;
}

bool IsLevelSafe(const std::vector<int>& level)
{
    bool increasing { level[1] > level[0] };
    for (std::size_t i { 1 }; i < level.size(); ++i) {
        int diff = level[i] - level[i - 1];
        if (std::abs(diff) < 1 || std::abs(diff) > 3 || (diff > 0) != increasing) {
            return false;
        }
    }
    return true;
}

std::size_t PartOne(std::vector<std::vector<int>>& report)
{
    return std::ranges::count_if(report, IsLevelSafe);
}

std::size_t PartTwo(std::vector<std::vector<int>>& report)
{
    return std::ranges::count_if(report, [&report](auto&& level) {
        if (IsLevelSafe(level)) {
            return true;
        }

        for (size_t i { 0 }; i < level.size(); i++) {
            std::vector<int> dampened(level);
            dampened.erase(dampened.begin() + i);
            if (IsLevelSafe(dampened)) {
                return true;
            }
        }
        return false;
    });
}

int main(int argc, char* argv[])
{
    if (argc < 2) {

        std::cerr << "Missing input file!" << std::endl;
        return 1;
    }

    std::string input_path = argv[1];
    auto data = FileToVector(input_path);
    
    std::cout << "Part one: " << PartOne(data) << '\n';
    std::cout << "Part two: " << PartTwo(data) << '\n';
}
