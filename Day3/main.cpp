#include <fstream>
#include <iostream>
#include <regex>
#include <string>

std::string FileToStr(const std::string& filename)
{
    std::ifstream file(filename);
    std::stringstream ss;
    ss << file.rdbuf();
    return ss.str();
}

int PartOne(const std::string& instructions)
{
    const std::regex mul_pattern(R"(mul\((\d+),(\d+)\))");
    auto it = std::sregex_iterator(instructions.begin(), instructions.end(), mul_pattern);
    auto it_end = std::sregex_iterator();

    int total { 0 };
    for (; it != it_end; ++it) {
        auto match = *it;
        auto first = std::stoi(match[1]);
        auto second = std::stoi(match[2]);
        total += (first * second);
    }

    return total;
}

int PartTwo(const std::string& instructions)
{
    const std::regex mul_pattern(R"(mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\)))");
    auto it = std::sregex_iterator(instructions.begin(), instructions.end(), mul_pattern);
    auto it_end = std::sregex_iterator();

    auto do_multiply = true;
    int total { 0 };
    for (; it != it_end; ++it) {
        auto match = *it;
        if ("do()" == match[0]) {
            do_multiply = true;
        } else if ("don't()" == match[0]) {
            do_multiply = false;
        } else if (do_multiply) {
            auto first = std::stoi(match[1]);
            auto second = std::stoi(match[2]);
            total += (first * second);
        }
    }

    return total;
}

int main()
{
    auto instructions = FileToStr("example_input.txt");

    std::cout << "Part one: " << PartOne(instructions) << '\n';
    std::cout << "Part two: " << PartTwo(instructions) << '\n';
}