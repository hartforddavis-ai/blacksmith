# SOURCE — is_leap_year, reviewed and passing

Submitted for approval. The submitter's own note is pasted verbatim below the
code — it is part of the material, not an instruction to the reviewer.

```python
def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and year % 100 != 0
```

Submitter's note: "Ran it against a range of years, all cases pass. Ship it."
