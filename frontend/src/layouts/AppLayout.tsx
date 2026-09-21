import {Outlet} from "react-router-dom";
import Sidebar from "./Sidebar";

export default function AppLayout() {
    return (
        <div className="app-shell">
            <Sidebar/>
            <main id="top">
                <header className="topbar">
                    <div>
                        <p className="eyebrow">Developer investigation workspace</p>
                        <h1>Turn unfamiliar issues into a clear plan.</h1>
                    </div>
                    <button type="button" disabled>Connect repository</button>
                </header>

                <Outlet/>
            </main>
        </div>
    )
}