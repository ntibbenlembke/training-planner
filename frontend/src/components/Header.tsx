export default function Header() {
    return (
        <div className="bg-paper border-2 border-gray-800 mx-4 mt-4 p-4">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                    <div className="grid gap-1">
                        <div className="w-8 h-1 bg-blue"></div>
                        <div className="w-8 h-1 bg-blue"></div>
                        <div className="w-8 h-1 bg-blue"></div>
                        <div className="w-8 h-1 bg-blue"></div>
                    </div>
                </div>
                <h1 className="text-xl font-bold tracking-wider">
                    BIKING SCHEDULER v0.6
                </h1>
                <div className="flex items-center space-x-4">
                    <div className="grid gap-1">
                        <div className="w-8 h-1 bg-blue"></div>
                        <div className="w-8 h-1 bg-blue"></div>
                        <div className="w-8 h-1 bg-blue"></div>
                        <div className="w-8 h-1 bg-blue"></div>
                    </div>
                </div>
            </div>
        </div>
    )
}