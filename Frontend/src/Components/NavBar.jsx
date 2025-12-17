import {navLinks} from "../constants";

const NavBar = ({ onSearchClick }) => {
    return (
        <header>
            <nav>
                <img  src="/logo.svg" alt="Nike logo" />

                <ul>
                    {navLinks.map(({ label }) => (
                        <li key={label}>
                            <a href={label}>{label}</a>
                        </li>
                    ))}
                </ul>

                <div className="flex-center gap-3">
                    <button 
                        onClick={onSearchClick}
                        className="hover:scale-110 transition-transform"
                        title="Search products"
                    >
                        <img src="/search.svg" alt="Search" />
                    </button>
                    <button>
                        <img src="/cart.svg" alt="Cart" />
                    </button>
                </div>
            </nav>
        </header>
    )
}
export default NavBar
