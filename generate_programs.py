from hypothesis import given, settings, Phase, strategies as st
import os
import random
import string

def generate_random_program():
    templates = [
        # Function definition
        """def random_func_{}():
    x = {}
    y = {}
    return x + y""",
        
        # Class definition
        """class RandomClass_{}:
    def __init__(self):
        self.value = {}
        
    def get_value(self):
        return self.value""",
        
        # For loop
        """for i in range({}):
    multiplier = {}
    print(i * multiplier)""",
        
        # While loop with counter
        """target = {}
step = {}
count = 0
while count < target:
    count += step
    print(count)""",
        
        # If-else statement
        """number = {}
limit = {}
if number > limit:
    print("Greater")
else:
    print("Less or equal")"""
    ]
    
    template = random.choice(templates)
    values = [random.randint(1, 100) for _ in range(template.count('{}'))]
    if template.startswith('for') or template.startswith('while') or template.startswith('if'):
        values[0] = random.randint(1, 10)  # Use small numbers for loop bounds and comparisons
    elif template.startswith('def') or template.startswith('class'):
        suffix = ''.join(random.choices(string.ascii_letters, k=5))
        values = [suffix] + values[1:]
    return template.format(*values)

def main():
    # Create a directory to store generated programs if it doesn't exist
    output_dir = "generated_programs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate 10 random programs
    for i in range(10):
        source_code = generate_random_program()
        
        # Generate a unique filename
        program_count = len(os.listdir(output_dir))
        filename = f"program_{program_count}.py"
        filepath = os.path.join(output_dir, filename)
        
        # Write the generated code to a file
        with open(filepath, "w") as f:
            f.write(source_code)
        print(f"Generated program saved to: {filepath}")
        print("Generated code:")
        print("-" * 40)
        print(source_code)
        print("-" * 40)
        print()

if __name__ == "__main__":
    main()