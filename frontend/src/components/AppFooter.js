import "../styles/AppFooter.css";

export default function AppFooter() {
    return(
        <footer className="footer">
            <div className="container">
                <div className="row">
                    <p className="fo-text">&copy; {new Date().getFullYear()} Article Summaries</p>
                </div>
            </div>
        </footer>
    )
}