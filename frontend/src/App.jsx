import './App.css';
import HomeSection from './components/HomeSection.jsx';

function App() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <div className="absolute inset-0 z-[-1] bg-[url('/grid.svg')] bg-repeat bg-[length:40px_40px]" />
      <main className="relative w-full px-4">
        <HomeSection />
      </main>
    </div>
  )
}

export default App;