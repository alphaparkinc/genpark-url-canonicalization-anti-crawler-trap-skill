import sys, json
from client import UrlCanonicalizationAntiCrawlerTrap

def main():
    guard = UrlCanonicalizationAntiCrawlerTrap()
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try:
            req = json.loads(line)
            method = req.get("method")
            rid = req.get("id")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "canonicalize_url", "description": "Canonicalize URL.", "inputSchema": {"type": "object", "properties": {"raw_url": {"type": "string"}}, "required": ["raw_url"]}},
                        {"name": "detect_crawler_trap", "description": "Detect crawler traps.", "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}},
                        {"name": "run_benchmark_url_canonicalizer", "description": "Run self-test.", "inputSchema": {"type": "object"}}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "canonicalize_url":
                    out = guard.canonicalize_url(args.get("raw_url", ""))
                elif tname == "detect_crawler_trap":
                    out = guard.detect_crawler_trap(args.get("url", ""))
                elif tname == "run_benchmark_url_canonicalizer":
                    out = guard.run_benchmark_url_canonicalizer()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
