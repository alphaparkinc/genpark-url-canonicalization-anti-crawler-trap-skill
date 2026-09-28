from client import UrlCanonicalizationAntiCrawlerTrap
import json

def main():
    guard = UrlCanonicalizationAntiCrawlerTrap()
    res = guard.run_benchmark_url_canonicalizer()
    print("URL Canonicalizer Benchmark Result:")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
