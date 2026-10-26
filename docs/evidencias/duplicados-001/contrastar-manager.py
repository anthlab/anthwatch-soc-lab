"""Cuenta los IDs del índice en los originales del manager, sin modificarlos.

Desde esta carpeta: python3 contrastar-manager.py > comparacion-manager.json
Solo retira prefijos NUL en memoria; cualquier otro error detiene el análisis.
"""
import collections
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    indexed = json.loads((BASE / "comparacion-ampliada.json").read_text())
    pairs = {pair["id"]: pair for pair in indexed["pairs"]}
    # El hash canónico del índice incluye input y @timestamp, añadidos en ingesta.
    import re
    console = (BASE / "duplicados-ampliados.console.txt").read_text()
    normalized = re.sub(r'"""(.*?)"""', lambda m: json.dumps(m[1], ensure_ascii=False),
                        console, flags=re.S)
    buckets = json.loads(normalized)["aggregations"]["repetidos"]["buckets"]
    sources = {b["key"]: b["documentos"]["hits"]["hits"] for b in buckets}
    matches = collections.defaultdict(list)
    files = []
    for path in sorted((BASE / "manager").glob("ossec-alerts-*.json")):
        raw = path.read_bytes()
        nul_blocks = []
        records = []
        offset = 0
        for line_no, line in enumerate(raw.splitlines(keepends=True), 1):
            clean = line.lstrip(b"\x00")
            prefix = len(line) - len(clean)
            if prefix:
                nul_blocks.append({"line": line_no, "offset_zero_based": offset,
                                   "bytes": prefix})
            if clean.strip():
                obj = json.loads(clean)
                records.append(obj)
                alert_id = obj.get("id")
                if alert_id in pairs:
                    copies = sources[alert_id]
                    comparisons = []
                    for copy in copies:
                        source = copy["_source"]
                        comparisons.append({
                            "document_id": copy["_id"],
                            "all_manager_fields_equal": all(
                                key in source and source[key] == value
                                for key, value in obj.items()),
                            "index_only_fields": sorted(set(source) - set(obj)),
                        })
                    matches[alert_id].append({"file": path.name, "line": line_no,
                                             "nul_prefix_bytes": prefix,
                                             "index_comparisons": comparisons})
            offset += len(line)
        files.append({"file": path.name, "sha256": sha256(raw), "bytes": len(raw),
                      "records": len(records), "nul_bytes": raw.count(b"\x00"),
                      "nul_prefixes": nul_blocks,
                      "first_timestamp": min(o["timestamp"] for o in records),
                      "last_timestamp": max(o["timestamp"] for o in records)})
    result = {
        "scope": "Exact alert IDs in the two supplied manager files; not all historical emissions",
        "method": "Parse every nonempty JSON line after removing only leading NUL bytes in memory; compare all manager fields with both indexed copies",
        "files": files,
        "target_ids": len(pairs),
        "ids_with_one_occurrence": sum(len(matches[k]) == 1 for k in pairs),
        "ids_missing": [k for k in pairs if not matches[k]],
        "ids_with_multiple_occurrences": [k for k in pairs if len(matches[k]) > 1],
        "all_manager_fields_equal_in_both_index_copies": all(
            len(matches[k]) == 1 and len(matches[k][0]["index_comparisons"]) == 2
            and all(c["all_manager_fields_equal"] for c in matches[k][0]["index_comparisons"])
            for k in pairs),
        "ids": [{"id": k, "occurrences": len(matches[k]), "matches": matches[k]}
                for k in pairs],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
