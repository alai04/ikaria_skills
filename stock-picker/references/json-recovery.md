# JSON Recovery from Mixed stdout/stderr Output

## Problem

When multi-step Python scripts use `print()` for progress (sent to stderr) and
`json.dumps()` for data output (sent to stdout), running the script with
`> file 2>&1` merges both streams into a single file. The resulting file is
NOT valid JSON — progress messages and JSON are interleaved.

This is especially common in cron mode where `execute_code` is blocked and
you must use `write_file` → `terminal(command) > file 2>&1` to capture output.

## Solution: Clean Output Files

```python
# BAD — JSON mixed with stderr
print(json.dumps(results))

# GOOD — save clean JSON to a separate file
with open("/tmp/step_results.json", "w") as f:
    json.dump(results, f)
# Only print a summary line that callers don't need to parse
print(json.dumps({"n_passed": len(passed), "n_total": len(all)}))
```

## Recovery: load_json_from_mixed()

When you've already written a file with mixed content, recover the JSON:

```python
def load_json_from_mixed(path):
    """Extract JSON from a file where stderr is interleaved with stdout JSON."""
    with open(path) as f:
        text = f.read()
    # Find the outermost { ... }
    start = text.find('{')
    if start < 0:
        raise ValueError("No JSON found")
    # Match braces to find the complete JSON object
    depth = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i+1])
    raise ValueError("Unmatched braces")
```

This works because JSON objects are balanced brace structures — even when
surrounded by log lines, the outermost `{...}` pair is self-contained.

## Alternative: Search for known keys

```python
# Find JSON by searching for known opening key
idx = text.find('{"voo_change"')
if idx >= 0:
    json.loads(text[idx:])  # may need brace matching if truncated
```

## Prevention Checklist

For every multi-step script in the stock-picker pipeline:
1. **Always** save full results with `json.dump()` to a clean file (e.g., `/tmp/step_N_results.json`)
2. **Never** rely on parsing stdout/stderr redirected output
3. Output only a one-line JSON summary to stdout (for the caller to check exit)
4. Subsequent steps read the clean saved file, not the merged redirect output
