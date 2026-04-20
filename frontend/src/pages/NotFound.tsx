import { Link } from "react-router-dom";

export function NotFound() {
  return (
    <div className="grid place-items-center py-20 text-center">
      <p className="text-sm text-navy/70">
        This tab is scheduled for a future iteration — see docs/ROADMAP.md.
      </p>
      <Link to="/" className="mt-4 btn-ghost">
        Back to Executive Summary
      </Link>
    </div>
  );
}
