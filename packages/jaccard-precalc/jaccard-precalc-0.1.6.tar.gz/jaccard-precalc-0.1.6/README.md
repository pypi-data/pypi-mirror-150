# Jaccard Precalculated String Matcher

The Jaccard index measures exhaustive substring comparison of two strings. This package is a slightly modified Jaccard with pre-calculation accelerate results.

```python3
    from jaccard_precalc.JaccardPrecalc import JaccardPrecalc
    string_list = ['Andrew Matte, 123 Main St, Toronto, Canada']
    jac = JaccardPrecalc(string_list)
    # jac.search(query_string, number_of_results)
    results = jac.search('Andy Matte, Toronto, CA', 1) # returns a list of dicts where each dict is {input: score}, sorted by top score

```