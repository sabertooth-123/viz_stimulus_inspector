import time

from inspector_ai import inspect_pair_ai

for pid, (a, b) in [
    ("sample1", ("../data/stimuli/valid_000_A.png", "../data/stimuli/valid_000_B.png")),
    ("sample2", ("../data/stimuli/valid_001_A.png", "../data/stimuli/valid_001_B.png")),
    ("sample3", ("../data/stimuli/font_confound_000_A.png", "../data/stimuli/font_confound_000_B.png")),
]:
    start = time.perf_counter()
    inspect_pair_ai(a, b)
    elapsed = time.perf_counter() - start
    print(f"{pid}: {elapsed:.2f}s")
    time.sleep(20)  # still need this between calls to avoid quota errors