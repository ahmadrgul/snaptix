import { useState } from "react"
import { useNavigate } from "react-router-dom";


const Hero = () => {
    const [ inputId, setInputId ] = useState('');
    const navigate = useNavigate()
    
    const handleClick = () => {
      navigate(`/events/${inputId}`)
    }

    return (
      <div
        className="h-screen w-screen bg-[url('/src/assets/hero.jpg')] bg-cover bg-center flex items-center justify-center bg-black/70 bg-blend-overlay"
      >
        <div 
          className="relative bottom-1/12 flex items-center justify-center flex-col"
        >
          <div className="text-white mb-10">
            <h1 className="text-6xl font-bold mb-3">Simple. Fast. Seamless.</h1>
            <h4 className="text-center font-mono">Enter the event id below and book your spot in seconds</h4>
          </div>
          <form>
            <label className="flex border rounded-full w-xl h-14 pl-4 pr-1 items-center bg-white">
              <input
                className="w-full  outline-none h-full border-none"
                placeholder="Enter event id e.g abcd-efgh-ijkl-mnop-qrst"
                value={inputId}
                onChange={e => setInputId(e.target.value)}
              />
              <div>
                <button
                  className="rounded-full select-none flex items-center justify-center text-4xl bg-cyan-800 cursor-pointer text-white h-12 w-12 hover:shadow-inner disabled:bg-gray-400 disabled:cursor-not-allowed transition-all"
                  disabled={inputId == ""}
                  onClick={handleClick}
                  type="submit"
                >
                  &#10132;
                </button>
              </div>
            </label>
            {/* <a className="font-mono text-blue-600 underline text-sm">Explore listed events</a> */}
          </form>
        </div>
      </div>
    )
}

export default Hero