# MSc Notes
Notes and remarks for my research in heuristic search for HTN planning.

---

## Master's TODO

- [ ] **Mark** the presentation as "ongoing work"
- [ ] **Enroll** in the master's last semester
- [ ] **Get** the LaTeX format for the Dissertation

---

## Summary

This document summarizes the current research tasks and experiments related to:

1. [Novelty heuristic](#novelty-heuristic)  
2. [Work on landmarks](#work-on-landmarks)  
3. [Usage of bidirectional landmarks in a state-of-the-art planner (PANDA)](#usage-of-bidirectional-landmarks-in-state-of-the-art-panda)  
4. [Organizational tasks](#organization)

---

# Novelty Heuristic

- [ ] **Read** the paper [A Novelty-based Heuristic for Problem Solving](https://ojs.aaai.org/index.php/AAAI/article/view/11027).
- [ ] **Implement** novelty in Pytrich using `<(h,t,f), h>`.
- [ ] **Compare** novelty with the original heuristic `h`.
- [ ] **Implement** the novelty approach in **PANDA**.

**Expectations**  
Find out if novelty can:
- Contribute to solving more problems in general, or  
- At least provide an advantage in specific domains.

---

# Work on Landmarks

## Experiments on Mandatory Tasks

Isolate the set of mandatory tasks found by the bottom-up approach and see differences in performance of:
- MT
- BU
- IBU (isolated bottom-up)

## Experiments on Landmark Updates

Test if landmark updates can be effective, running an extended version in PANDA.

**Expectations**  
Landmark updates are a fast way to generate more landmarks without the need for full recomputation, thus this approach could add information without compromising the heuristic’s role.

---

## Usage of Bidirectional Landmarks in State-of-the-Art PANDA

- [x] **Implement** bidirectional landmarks in **PANDA-lama**.
- [ ] **Run** experiments comparing bidirectional landmarks with LM-Cut and bottom-up approaches.

**Expectations**  
Determine if bidirectional landmarks enhance the performance of state-of-the-art planners.

---

# Organization

## Merge the PANDA Projects

- [ ] Merge **panda-lama** and **Dealer** into a single GitHub repository.
- [ ] Organize files and scripts in a coherent structure.
- [ ] Standardize the parser and grounder so they can work in both.

---
