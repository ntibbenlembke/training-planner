import { Outlet } from "react-router-dom"
import Header from "../components/Header"

export default function Root() {
    return (
        <div className="flex flex-col min-h-screen bg-paper">
            <Header />
            <Outlet />

            
        </div>
    );
}