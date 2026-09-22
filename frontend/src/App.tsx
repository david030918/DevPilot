import {BrowserRouter, Route, Routes} from "react-router-dom";
import OverviewPage from "./pages/OverviewPage";
import AppLayout from "./layouts/AppLayout";
import ProjectsPage from "./pages/ProjectsPage";
import ProjectDetailPage from "./pages/ProjectDetailPage";

export default function App() {
    return (
        <div>
            <BrowserRouter>
                <Routes>
                    <Route element={<AppLayout/>}>
                        <Route index element={<OverviewPage/>}/>
                        <Route path="/projects" element={<ProjectsPage/>}/>
                        <Route path="/projects/:projectId" element={<ProjectDetailPage/>}/>
                    </Route>
                </Routes>
            </BrowserRouter>
        </div>
    );
}


