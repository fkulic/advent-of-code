#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <sstream>
#include <unordered_map>
#include <vector>

std::pair<std::vector<int>, std::vector<int>> FileToTwoVectors(const std::string& filename)
{
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Could not open file: " << filename << std::endl;
        std::terminate();
    }

    std::vector<int> first;
    std::vector<int> second;

    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        int number1, number2;
        if (iss >> number1 and iss >> number2) {
            first.push_back(number1);
            second.push_back(number2);
        }
    }

    file.close();
    return { first, second };
}

std::size_t PartOne(std::vector<int>& first_list, std::vector<int>& second_list)
{
    std::ranges::sort(first_list);
    std::ranges::sort(second_list);
    std::size_t total_sum { 0 };
    for (std::size_t i { 0 }; i < first_list.size(); ++i) {
        total_sum += std::abs(first_list[i] - second_list[i]);
    }
    return total_sum;
}

std::size_t PartTwo(std::vector<int>& first_list, std::vector<int>& second_list)
{
    std::unordered_map<int, std::size_t> sec_count;
    for (auto v : second_list) {
        ++sec_count[v];
    }

    std::size_t similarity_score { 0 };
    for (auto v : first_list) {
        similarity_score += v * sec_count[v];
    }
    return similarity_score;
}

int main(int argc, char* argv[])
{
    if (argc < 2) {

        std::cerr << "Missing input file!" << std::endl;
        return 1;
    }

    std::string input_path = argv[1];
    auto [example_first_list, example_second_list] = FileToTwoVectors(input_path);

    std::cout << "Part one: " << PartOne(example_first_list, example_second_list) << '\n';
    std::cout << "Part two: " << PartTwo(example_first_list, example_second_list) << '\n';
}