# Access Log Summary Report

An Apache-style access log is available at `/app/access.log` in the working
directory. Parse it and write a small JSON summary report to
`/app/report.json`.

The report must be a single JSON object with exactly these three keys:

- `total_requests` (integer): the total number of request lines in the log.
- `unique_ips` (integer): the number of distinct client IP addresses. The
  client IP is the first whitespace-separated field of each line.
- `top_path` (string): the request path (for example `/index.html`) that was
  requested most often. If several paths tie for the most requests, any one of
  them is acceptable.

## Success criteria

1. A file exists at `/app/report.json`.
2. Its contents are a single valid JSON object.
3. `total_requests` equals the number of request lines in `/app/access.log`.
4. `unique_ips` equals the number of distinct client IP addresses in the log.
5. `top_path` is the path that appears most frequently in the log.
