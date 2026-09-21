import {BrowserRouter, Route, Routes} from "react-router-dom";
import OverviewPage from "./pages/OverviewPage";
import AppLayout from "./layouts/AppLayout";
import ProjectsPage from "./pages/ProjectsPage";

export default function App() {
    return (
        <div>
            <BrowserRouter>
                <Routes>
                    <Route element={<AppLayout/>}>
                        <Route index element={<OverviewPage/>}/>
                        <Route path="/projects" element={<ProjectsPage/>}/>
                    </Route>
                </Routes>
            </BrowserRouter>
        </div>
    );
}


