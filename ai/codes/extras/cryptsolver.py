def is_valid_assignment(assignment, words, result):
    # Calculate the numerical values of the words based on the current assignment
    def word_value(word):
        return sum(assignment[char] * (10 ** i) for i, char in enumerate(reversed(word)))

    # Calculate the values of the two words and the result
    left_sum = sum(word_value(word) for word in words)
    right_value = word_value(result)

    return left_sum == right_value

def backtrack(assignment, letters, domain, words, result):
    if len(assignment) == len(letters):
        # All letters are assigned, check if the solution is valid
        if is_valid_assignment(assignment, words, result):
            return assignment
        return None

    # Select the next variable with the most restricted domain
    unassigned = [l for l in letters if l not in assignment]
    variable = min(unassigned, key=lambda x: len(domain[x]))

    for value in domain[variable]:
        # Assign the value
        assignment[variable] = value

        new_domain = {k: [v for v in domain[k] if v not in assignment.values()] for k in letters}
        found_solution = backtrack(assignment, letters, new_domain, words, result)
        if found_solution is not None:
            return found_solution
        
        # remove assignment
        del assignment[variable]

    return None

def solve_cryptarithmetic(words, result):
    # Extract unique letters from the words
    letters = set(''.join(words) + result)
    domain = {letter: list(range(0, 10)) for letter in letters}

    # Set leading letters' domains to not include 0
    for word in words:
        domain[word[0]] = list(range(1, 10))  # First letter cannot be 0
    if len(result) == max(len(words[0]), len(words[1])) + 1:
        domain[result[0]] = [1]    
    else:    
        domain[result[0]] = list(range(1, 10))  # First letter of result cannot be 0
    # domain[result[0]] = list(range(1, 10))  # First letter of result cannot be 0


    assignment = {}
    solution = backtrack(assignment, letters, domain, words, result)
    return solution if solution else "No solution found"

# Example usage
words = ["APPLE", "GRAPE"]
result = "CHERRY"
solution = solve_cryptarithmetic(words, result)
print(solution)
