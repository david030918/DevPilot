import {NavLink} from "react-router-dom";

export default function Sidebar() {
    return (
        <aside className="sidebar">
            <a className="brand" href="#top" aria-label="DevPilot home">
                <span className="brand-mark">D</span>
                <span>DevPilot</span>
            </a>

            <nav aria-label="Primary navigation">
                <NavLink className="nav-item active" to="/" end>Overview</NavLink>
                <NavLink className="nav-item" to="projects" end>Projects</NavLink>
                <NavLink className="nav-item" to="issues" end>Issues</NavLink>
                <NavLink className="nav-item" to="investigations" end>Investigations</NavLink>
                <NavLink className="nav-item" to="tasks" end>Tasks</NavLink>
            </nav>
            <div className="sidebar-note">
                <span className="status-dot"/> V1 skeleton
            </div>
        </aside>)
}
