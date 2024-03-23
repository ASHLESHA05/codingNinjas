import re

def find_input_size_and_operations(c_code):
    # Regular expression patterns to match common input size indicators
    input_patterns = [
        r'\bint\s+([a-zA-Z_][a-zA-Z0-9_])\s=\s*(\d+);',  # Integer variable initialization
        r'\bint\s+([a-zA-Z_][a-zA-Z0-9_])\s;\s*scanf\s*\(\s*"%s"\s,\s*&?([a-zA-Z_][a-zA-Z0-9_])\s\);',  # scanf for integer input
        r'\bint\s+([a-zA-Z_][a-zA-Z0-9_])\s;\s*fscanf\s*\(\s*stdin\s*,\s*"%d"\s*,\s*&?([a-zA-Z_][a-zA-Z0-9_])\s\);',  # fscanf for integer input
        # Add more patterns as needed for other types of input
    ]
    
    input_size = None
    operations = []
    loop_complexities = []

    for pattern in input_patterns:
        match = re.search(pattern, c_code)
        if match:
            input_size = match.group(2)  # Extract the input size from the matched pattern
            break
    
    # Regular expression pattern to match common basic operations
    basic_operation_pattern = r'(\b[\w\s]+\b)\s*([+\-/%]|==|!=|<=|>=|<|>|\|\||&&)\s([\w\s]+)\s*;'
    operation_matches = re.findall(basic_operation_pattern, c_code)
    
    for match in operation_matches:
        operations.append(match)
    
    # Regular expression pattern to match versatile loop constructs
    loop_pattern = r'for\s*\(\s*(?:int|unsigned|int\s*const|long|long\s*long)?\s*([\w]+)\s*=\s*([\w]+)\s*;\s*\1\s*([<>]=?)\s*([\w]+)\s*;\s*\1\s*(?:\+\+|--|\+=|-=)?\s*\)\s*{([^{}])\s}'
    loop_matches = re.finditer(loop_pattern, c_code)
    
    for match in loop_matches:
        loop_code = match.group(5)  # Extract loop code
        loop_complexities.append(analyze_loop_complexity(loop_code))

    return input_size, operations, loop_complexities

def analyze_loop_complexity(loop_code):
    # Regular expression pattern to match common basic operations inside the loop
    basic_operation_pattern = r'(\b[\w\s]+\b)\s*([+\-/%]|==|!=|<=|>=|<|>|\|\||&&)\s([\w\s]+)\s*;'
    operation_matches = re.findall(basic_operation_pattern, loop_code)
    return len(operation_matches)

def sum_up_operations(operations, loop_complexities):
    total_operations = len(operations)
    total_operations += sum(loop_complexities)
    return total_operations

def express_complexity(total_operations):
    # Express the total number of operations as a function of the input size using Big O notation
    return f"O({total_operations})"

# Example usage:
c_code = """
#include <stdio.h>

int main() {
    int n;
    printf("Enter the size: ");
    scanf("%d", &n);
    int i, sum = 0;
    for (i = 0; i < n; i++) {
        sum += i;
    }
    printf("Sum: %d\n", sum);
    return 0;
}
"""

input_size, operations, loop_complexities = find_input_size_and_operations(c_code)
if input_size:
    print("Input size:", input_size)
else:   
    print("Input size not found.")

if operations:
    print("Basic operations found:")
    for op in operations:
        print(op)
else:
    print("No basic operations found.")

if loop_complexities:
    print("Loop complexities:")
    for complexity in loop_complexities:
        print(complexity)
else:
    print("No loops found.")

# Sum up operations
total_operations = sum_up_operations(operations, loop_complexities)
print("Total operations:", total_operations)

# Express complexity using Big O notation
complexity_expression = express_complexity(total_operations)
print("Complexity:", complexity_expression)