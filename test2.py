import os
import subprocess
import time

def measure_execution_time(executable_path, input_size):
    start_time = time.time()
    subprocess.run([executable_path, str(input_size)], capture_output=True, text=True)
    end_time = time.time()
    return end_time - start_time

def get_time_complexity(executable_path, input_sizes=[10, 100, 1000]):
    try:
        execution_times = [measure_execution_time(executable_path, input_size) for input_size in input_sizes]
        ratios = [execution_times[i] / execution_times[i-1] for i in range(1, len(execution_times))]
        if all(ratio == ratios[0] for ratio in ratios):
            return "O(1)"
        elif ratios[-1] > 2:
            return "O(2^N)"
        elif ratios[-1] > 1:
            return "O(N^k)"
        else:
            return "O(N)"
    except Exception as e:
        print("Error:", e)
        return "Unknown"

def save_c_code_to_file(c_code):
    with open("user_code.c", "w") as file:
        file.write(c_code)

# Example usage:
user_c_code = """
#include <stdio.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <input_size>\n", argv[0]);
        return 1;
    }
    
    int n;
    sscanf(argv[1], "%d", &n);
    int i, sum = 0;
    for (i = 0; i < n; i++) {
        sum += i;
    }
    printf("Sum: %d\n", sum);
    return 0;
}
"""
save_c_code_to_file(user_c_code)

c_code_path = "./user_code"  # Adjust as needed

time_complexity = get_time_complexity(c_code_path)
print("Estimated time complexity:", time_complexity)
