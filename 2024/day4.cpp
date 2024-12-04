#include <fstream>
#include <iostream>
#include <numeric>
#include <ranges>
#include <string>
#include <vector>

std::vector<std::string> FileToStrLines(const std::string& filename)
{
    std::vector<std::string> result;
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Could not open file: " << filename << std::endl;
        std::terminate();
    }

    std::string line;
    while (std::getline(file, line)) {
        result.push_back(line);
    }

    file.close();
    return result;
}

std::vector<std::string> GetAllDiagonalStrings(std::vector<std::string> puzzle_input)
{
    const std::size_t len { puzzle_input.size() };
    auto diagonal_count = 2 * len - 1;
    std::vector<std::string> diagonal_strings(2 * diagonal_count);
    for (std::size_t i { 0 }; i < len; ++i) {
        for (std::size_t j = 0; j < len; ++j) {
            diagonal_strings[i + j] += puzzle_input[i][j];
            diagonal_strings[diagonal_count + i + j] += puzzle_input[i][len - 1 - j];
        }
    }

    return diagonal_strings;
}

std::vector<std::string> GetVerticalStrings(const std::vector<std::string>& puzzle_input)
{
    const std::size_t len { puzzle_input.size() };
    std::vector<std::string> vertical_strings(len);
    for (std::size_t i { 0 }; i < len; ++i) {
        for (std::size_t j = 0; j < len; ++j) {
            vertical_strings[i] += puzzle_input[j][i];
        }
    }

    return vertical_strings;
}

std::size_t CountSubstrings(const std::string& input, const std::string& substring)
{
    std::size_t count { 0 };
    std::size_t pos = input.find(substring, 0);
    while (pos != std::string::npos) {
        pos = input.find(substring, pos + 1);
        ++count;
    }
    return count;
}

std::size_t CountSubstringsInLines(const std::vector<std::string>& lines, const std::string& substring)
{
    return std::accumulate(lines.cbegin(), lines.cend(), 0,
        [&substring](std::size_t acc, const std::string& line) {
            return acc + CountSubstrings(line, substring);
        });
}

int PartOne(const std::vector<std::string>& puzzle_input)
{
    std::size_t count { 0 };

    const std::string substring { "XMAS" };
    count += CountSubstringsInLines(puzzle_input, substring);
    count += CountSubstringsInLines(GetVerticalStrings(puzzle_input), substring);
    count += CountSubstringsInLines(GetAllDiagonalStrings(puzzle_input), substring);

    const std::string reversed(substring.rbegin(), substring.rend());
    count += CountSubstringsInLines(puzzle_input, reversed);
    count += CountSubstringsInLines(GetVerticalStrings(puzzle_input), reversed);
    count += CountSubstringsInLines(GetAllDiagonalStrings(puzzle_input), reversed);

    return count;
}

int PartTwo(const std::vector<std::string>& puzzle_input)
{
    const std::size_t len { puzzle_input.size() };

    std::size_t count { 0 };
    for (size_t i = 1; i < len - 1; ++i) {
        for (size_t j = 1; j < len - 1; ++j) {
            if (puzzle_input[i][j] == 'A') {
                std::vector<std::string> diag {
                    { puzzle_input[i - 1][j - 1], puzzle_input[i][j], puzzle_input[i + 1][j + 1] },
                    { puzzle_input[i + 1][j - 1], puzzle_input[i][j], puzzle_input[i - 1][j + 1] },
                };
                if (2 == CountSubstringsInLines(diag, "MAS") + CountSubstringsInLines(diag, "SAM")) {
                    ++count;
                }
            }
        }
    }

    return count;
}

int main(int argc, char* argv[])
{
    if (argc < 2) {

        std::cerr << "Missing input file!" << std::endl;
        return 1;
    }

    const std::string input_path = argv[1];
    auto puzzle_input = FileToStrLines(input_path);

    std::cout << "Part one: " << PartOne(puzzle_input) << '\n';
    std::cout << "Part two: " << PartTwo(puzzle_input) << '\n';
}