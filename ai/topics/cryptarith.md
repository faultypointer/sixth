# How to Solve Crypt-Arithmatic problems

- Crypt-Arithmatic problems are a type of [Constraints Satisfaction Problem] where out goal is to assign the digits 0-9 to
    each letter iin the problem such that the result sum is arithmetically correct.
- so all the distinct letters in the problem are variables.
- the domain for each variable is 0-9 with a constraint that no leading zero is allowed
- all the variables have to follow `alldiff` constraint
- and other constraints that make the sum valid

## Initial Thoughts

### Algorithm

- all the variables start out uninitialized and with some domains of value they can be assigned. Since leading zeros are not allowed, domains
- of some variables are more limited than the others.
- while there is still variables unassigned
  - take the variable with most restricted domain
  - if there are not values in the domain, `take back the last assignment`; if there are no assignments to take back the problem cannot be solved
  - assign a random value to the variable
  - `readjust the domains` of all other unassigned variables to fit the constraints

### For Example

for the following Crypt-Arithmatic problem:

```plaintext
    T W O
  + T W O
   ------
  F O U R
```

The variables are `{T, W, O, F, U, R}`.
The Domains are:

```python
domain = {
    'T': (0..9), 
    'F': (0..9), 
    'W': (0..9), 
    'O': (0..9), 
    'U': (0..9), 
    'R': (0..9) 
}
```

The constraints are:

```python
ALLDIFF(T, W, O, F, U, R)
T != 0, F != 0 # No leading zeros
O + O = R + 10 * C1
W + W + C1 = U + 10 * C10
T + T + C10 = O + 10 * C100
F = C100
```

Well shit!
The additional carry variables also needs to be stored (I think)
So revised variables are `{T, W, O, F, U, R, C1, C10, C100}`.
and the revised domain

```python
domain = {
    'T': (0..9), 
    'F': (0..9), 
    'W': (0..9), 
    'O': (0..9), 
    'U': (0..9), 
    'R': (0..9),
    'C1': (0, 1),
    'C10': (0, 1),
    'C100': (0, 1),
}
```

The carry digits can only be 0 or 1 since each letter can only be 0-9 and we are only adding two letters at a time and a carry (0 or 1).
Also the alldiff constrains doesn't apply to carry variables.

applying the constrains the domain of the values reduce to following:

```python
domain = {
    'F': (1), 
    'C1': (0, 1),
    'C10': (0, 1),
    'C100': (0, 1),
    'T': (1..9), 
    'W': (0..9), 
    'O': (0..9), 
    'U': (0..9), 
    'R': (0..9),
}
```

The variable with the most restricted domain is `F` with only one value so we assign `1` to `F`.
This changes the domain of `C100` to just `(1)` and after assigning `1` to `C100`.
the constrain `T + T + C10 = O + 10 * C100` now reduces to `T + T + C10 = O + 10`
So the only values for `T` that satisfies the constrait are ones greater than 4.
So the next variable with most restricted domain is `C10`, we choose a random value (1, 0) for it then apply the constrains again and continue
If the above algorithm is followed, I think it should give the solution to the problem

## Afterthoughts

I asked chatgpt what it thought about the above procedure and it did give me some pointers.

### Forward Checking

Instead of checking if the domain for some variable is empty after selecting it, I can check in advance during
  this step in [algorithm](#algorithm): `readjust the domains` of all other unassigned variables to fit the constraints
If the domain for any variable becomes empty we can discard the selected value for current variable and choose another (if available)
