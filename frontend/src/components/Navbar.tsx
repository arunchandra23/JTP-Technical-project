// Navbar.tsx
/**
 * Represents the navigation bar component.
 * This component displays the title of the image recommendation system.
 */
const Navbar: React.FC = () => {
  return (
    <nav className="bg-indigo-700 text-white p-6 sticky top-0 left-0 w-full z-10">
      <div className="container mx-auto flex justify-center">
        <h1 className="text-2xl font-bold">
          Image Recommendation System
        </h1>
      </div>
    </nav>
  );
};
  
  export default Navbar;
  