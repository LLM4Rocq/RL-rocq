from dataclasses import dataclass
from datasets import load_dataset, Dataset

@dataclass
class TheoremData():
    """ Class for storing information about a theorem. """
    name: str
    code: str
    goal: str
    context: str = None

code1 = """Require Import Coq.Reals.Reals.

Open Scope R_scope.

Theorem aime_1983_p1 :
  forall (x y z w : R),
    1 < x ->
    1 < y ->
    1 < z ->
    0 < w ->
    ln w / ln x = 24 ->
    ln w / ln y = 40 ->
    ln w / ln (x * y * z) = 12 ->
    ln w / ln z = 60.

Proof."""
goal1 = """|- forall x y z w : R,
1 < x ->
1 < y ->
1 < z ->
0 < w ->
ln w / ln x = 24 ->
ln w / ln y = 40 ->
ln w / ln (x * y * z) = 12 -> ln w / ln z = 60"""
theorem1 = TheoremData(
    name = "aime_1983_p1",
    code = code1,
    goal = goal1
)

code2 = """Require Import Reals.
Open Scope R_scope.

Theorem aime_1983_p9 :
  forall (x : R), 0 < x -> x < PI ->
  12 <= (9 * (x^2 * sin x^2) + 4) / (x * sin x).
Proof."""
goal2 = """|- forall x : R,
0 < x ->
x < PI ->
12 <= (9 * (x ^ 2 * sin x ^ 2) + 4) / (x * sin x)"""
theorem2 = TheoremData(
    name = "aime_1983_p9",
    code = code2,
    goal = goal2
)

dataset = [theorem1, theorem2]
