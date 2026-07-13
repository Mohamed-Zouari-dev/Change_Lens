from models import IntegrityReport

def generate_markdown_report(report: IntegrityReport) -> str:
    """
    Transforms an IntegrityReport object into a clean, formatted Markdown document
    optimized for CI/CD job summaries and log retention.
    """
    lines = [
        "# ChangeLens Integrity Audit Report",
        "",
        f"**Status:** {report.audit_metadata.status}",
        f"**Target Directory:** `{report.audit_metadata.target_directory}`",
        f"**Base Snapshot Time:** {report.audit_metadata.base_snapshot_time}",
        f"**Verification Run Time:** {report.audit_metadata.verification_time}",
        "",
        "## Summary Metrics",
        "",
        f"- Files Scanned: {report.summary.files_scanned}",
        f"- Files Matched Baseline: {report.summary.files_matched}",
        f"- Files Modified: {report.summary.files_modified}",
        f"- Files Added: {report.summary.files_added}",
        f"- Files Deleted: {report.summary.files_deleted}",
        ""
    ]

    if report.summary.is_clean:
        lines.append("### [OK] System state perfectly matches baseline.")
        return "\n".join(lines)

    lines.append("## Detected Deviations")
    lines.append("")
    lines.append("| Change Type | File Path | Cryptographic Details |")
    lines.append("| :--- | :--- | :--- |")

    for file in report.changes.modified:
        lines.append(f"| MODIFIED | `{file.path}` | Old: {file.old_hash[:16]}... <br> New: {file.new_hash[:16]}... |")

    for file in report.changes.added:
        lines.append(f"| ADDED | `{file.path}` | Current Hash: {file.current_hash[:16]}... |")

    for file in report.changes.deleted:
        lines.append(f"| DELETED | `{file.path}` | Last Known Hash: {file.last_known_hash[:16]}... |")

    return "\n".join(lines)