import { useEffect, useState } from "react";
import { getOverview, type Overview } from "./api";

const fallbackWorkflow = [
  "Select repository",
  "Choose issue",
  "Run investigation",
  "Review evidence",
  "Create tasks",
];

export default function App() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getOverview().then(setOverview).catch((reason: unknown) => {
      setError(reason instanceof Error ? reason.message : "Unable to reach the API");
    });
  }, []);

  const workflow = overview?.workflow ?? fallbackWorkflow;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#top" aria-label="DevPilot home">
          <span className="brand-mark">D</span>
          <span>DevPilot</span>
        </a>
        <nav aria-label="Primary navigation">
          <a className="nav-item active" href="#overview">Overview</a>
          <a className="nav-item" href="#projects">Projects</a>
          <a className="nav-item" href="#issues">Issues</a>
          <a className="nav-item" href="#investigations">Investigations</a>
          <a className="nav-item" href="#tasks">Tasks</a>
        </nav>
        <div className="sidebar-note">
          <span className="status-dot" /> V1 skeleton
        </div>
      </aside>

      <main id="top">
        <header className="topbar">
          <div>
            <p className="eyebrow">Developer investigation workspace</p>
            <h1>Turn unfamiliar issues into a clear plan.</h1>
          </div>
          <button type="button" disabled>Connect repository</button>
        </header>

        <section className="hero-card" id="overview">
          <div>
            <span className="pill">Portfolio MVP · V1</span>
            <h2>Start with the issue. Follow the evidence.</h2>
            <p>
              DevPilot combines repository context and structured AI reasoning to suggest
              possible causes, investigation steps, and targeted tests.
            </p>
          </div>
          <div className="connection-card" aria-live="polite">
            <span>Application API</span>
            <strong>{overview ? "Connected" : error ? "Unavailable" : "Checking…"}</strong>
            <small>{error ?? overview?.status ?? "Contacting the backend"}</small>
          </div>
        </section>

        <section className="content-grid">
          <article className="panel workflow-panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Core workflow</p>
                <h2>From issue to action</h2>
              </div>
              <span>{overview?.version ?? "0.1"}</span>
            </div>
            <ol className="workflow">
              {workflow.map((step, index) => (
                <li key={step}>
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <div>
                    <strong>{step}</strong>
                    <small>{index === 0 ? "GitHub integration arrives in V1.3" : "Planned V1 capability"}</small>
                  </div>
                </li>
              ))}
            </ol>
          </article>

          <aside className="panel next-panel">
            <p className="eyebrow">Next milestone</p>
            <h2>Core backend foundation</h2>
            <p>Add PostgreSQL, migrations, structured errors, logging, and automated tests.</p>
            <div className="progress-track"><span /></div>
            <div className="progress-label"><span>V1.0 complete</span><span>1 of 8</span></div>
          </aside>
        </section>
      </main>
    </div>
  );
}

