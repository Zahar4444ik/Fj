# Testing Protocol for Formal Languages Assessment

## 1. Purpose of the Protocol

This document defines a formal testing protocol for assessing students’ knowledge of **formal languages and automata theory**. The protocol is designed for a bachelor-level project and focuses on verifying **correctness of language recognition**, rather than syntactic or implementation-specific details.

The protocol supports automated evaluation of two independent tasks:

1. **Automaton construction from a regular expression** (structural correctness)
2. **Implementation of automaton behavior in code** (behavioral correctness)

The protocol ensures fairness, objectivity, and reproducibility of evaluation.

---

## 2. General Principles

* The primary evaluation criterion is **language equivalence**.
* Different representations (state names, ordering, DFA vs NFA) are allowed.
* Students are not penalized for alternative correct constructions.
* Evaluation is fully automated.

---

## 3. Task 1: Isomorphism Testing of `.fsa` Files

### 3.1 Task Description

Students are given a regular expression `R` and are required to construct a finite automaton saved in a `.fsa` file format. The automaton may be:

* Deterministic (DFA)
* Nondeterministic (NFA)
* Contain ε-transitions

The system independently generates a reference automaton from the same regular expression.

The task is to determine whether the student automaton recognizes the same language as the reference automaton.

---

### 3.2 Inputs

* Regular expression `R`
* Student automaton `A_s` (from `.fsa` file)
* Reference automaton `A_r` (system-generated)

---

### 3.3 Parsing and Internal Representation

Both automata are parsed into a unified internal representation consisting of:

* Set of states
* Alphabet
* Transition relation (including ε-transitions)
* Start state
* Set of accepting states

State identifiers from the input are mapped to internal IDs.

---

### 3.4 Normalization

The following normalization steps are applied:

* Removal of unreachable states
* Alphabet consistency check
* Explicit handling of ε-transitions

These steps do not change the recognized language.

---

### 3.5 Automaton Type Alignment

Because students may submit NFAs or DFAs, both automata are converted to a **common canonical form**:

1. Convert NFA → DFA using subset construction
2. Minimize resulting DFAs

After minimization, both automata are guaranteed to be:

* Deterministic
* ε-free
* Minimal

---

### 3.6 DFA Isomorphism Check

Two minimal DFAs are considered **isomorphic** if there exists a bijection between their states that preserves:

* Start state
* Accepting states
* Transitions for every symbol in the alphabet

Formally, for a bijection `f`:

* `f(q_start_s) = q_start_r`
* `q ∈ F_s ⇔ f(q) ∈ F_r`
* `f(δ_s(q, a)) = δ_r(f(q), a)` for all states `q` and symbols `a`

The check is performed using a synchronized BFS traversal starting from the start states.

---

### 3.7 Decision Criteria

| Condition               | Result |
| ----------------------- | ------ |
| DFAs are isomorphic     | PASS   |
| DFAs are not isomorphic | FAIL   |

---

### 3.8 Optional Partial Evaluation (Optional)

The system may optionally record:

* Language equivalence without minimality
* Structural warnings (unused states, redundant transitions)

These may be used for partial credit or feedback but do not affect the binary pass/fail result unless required.

---

## 4. Task 2: Behavioral Testing of Automaton Code

### 4.1 Task Description

Students are given:

* A regular expression `R`
* A skeleton of code implementing a DFA or NFA (iterative or recursive)

Their task is to complete the implementation so that the automaton correctly recognizes the language defined by `R`.

---

### 4.2 Inputs

* Student implementation `M_s`
* Reference automaton `M_r`
* Test word set `T`

---

### 4.3 Interface Requirements

The student implementation must provide a method:

```python
check(string: str) -> bool
```

The method returns:

* `True` if the string is accepted
* `False` otherwise

Failure to meet the interface or runtime errors result in immediate failure of the task.

---

### 4.4 Test Word Generation

The test set `T` is composed of two parts:

#### 4.4.1 Exhaustive Test Set

* Empty string ε
* All strings over the alphabet Σ of length ≤ `k` (typically `k = 3` or `4`)

#### 4.4.2 Randomized Test Set

* Randomly generated strings over Σ
* Variable length up to `n` (e.g. `n = 10`)
* Fixed number of samples (e.g. 50)

This combination ensures coverage of edge cases and general behavior.

---

### 4.5 Behavioral Comparison

For each test string `w ∈ T`:

1. Evaluate `M_s.check(w)`
2. Evaluate `M_r.check(w)`
3. Compare results

A mismatch indicates incorrect behavior.

---

### 4.6 Decision Criteria

| Condition              | Result |
| ---------------------- | ------ |
| All test results match | PASS   |
| Any mismatch detected  | FAIL   |

The first mismatching input is stored as a counterexample.

---

### 4.7 Feedback Generation

If a mismatch occurs, the system reports:

* The input string `w`
* Expected result (reference automaton)
* Student result

Example:

```
Input: "1010"
Expected: ACCEPT
Your result: REJECT
```

---

## 5. Scoring Model (Recommended)

| Component                    | Weight |
| ---------------------------- | ------ |
| Task 1 – Automaton structure | 50%    |
| Task 2 – Automaton behavior  | 50%    |

Optional sub-scoring:

* Language correctness: 70%
* Structural quality: 30%

---

## 6. Validity and Academic Justification

The protocol evaluates student solutions based on **formal language equivalence**, which is the mathematically correct criterion in automata theory. Structural differences that do not affect the recognized language are explicitly allowed.

The combination of automaton isomorphism testing and systematic behavioral testing ensures:

* Correctness
* Fairness
* Resistance to hard-coded solutions

This protocol is suitable for automated assessment in formal languages and automata courses.

---

## 7. Conclusion

This testing protocol provides a rigorous and extensible framework for evaluating automata-based student assignments. It aligns theoretical foundations with practical implementation and supports reliable automated grading.
