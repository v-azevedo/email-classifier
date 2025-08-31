const Header = () => {
  return (
    <header className="flex justify-between items-center pt-8">
      <div className="text-left">
        <h1 className="font-quicksand-700 text-5xl text-primary hover:text-gray-700 cursor-pointer">ClassifyAI</h1>
        <p className="text-gray-400 font-quicksand-400">The only email classifier you will ever need!</p>
      </div>
      <nav className="font-quicksand-800 text-primary text-xl transition-all">
        <a href="/" className="hover:text-gray-700">
          Home
        </a>
      </nav>
    </header>
  );
};

export default Header;
