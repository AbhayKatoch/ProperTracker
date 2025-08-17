import React, { useEffect, useState } from "react";
import "./App.css"; 

function App() {
  const [properties, setProperties] = useState([]);

  useEffect(() => {
    fetch("https://propertracker.onrender.com/property")
      .then((res) => res.json())
      .then((data) => setProperties(data))
      .catch((err) => console.error("Error fetching properties:", err));
  }, []);

  return (
    <div className="relative min-h-screen px-6 py-10 font-inter overflow-hidden ">
      <div className="absolute inset-0 z-0 animate-gradient bg-gradient-to-br from-indigo-100 via-blue-50 to-white bg-[length:400%_400%]" />

      <div className="absolute top-[-80px] left-[-80px] w-[300px] h-[300px] bg-indigo-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 z-0 animate-pulse" />
      <div className="absolute bottom-[-80px] right-[-80px] w-[300px] h-[300px] bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 z-0 animate-pulse" />

      <div className="absolute inset-0 bg-[url('/noise.png')] opacity-10 z-0 pointer-events-none" />

      {/* Main Content */}
      <div className="relative z-10">
        <h1 className="text-5xl font-extrabold text-indigo-800 text-center mb-14 drop-shadow-lg">
          ProperTracker
        </h1>

        {properties.length === 0 ? (
          <div className="text-center text-gray-600 mt-20 text-xl">
            Loading properties...
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10">
            {properties.map((prop) => (
              <div
                key={prop.id}
                className="bg-white/80 backdrop-blur-lg border border-gray-200 rounded-3xl shadow-md hover:shadow-2xl transition duration-300 overflow-hidden flex flex-col"
              >
                {/* Images */}
                <div className="relative">
                  {prop.images && prop.images.length > 0 ? (
                    <img
                      src={`https://propertracker.onrender.com/media/${prop.images[0]}/`}
                      alt="property"
                      className="w-full h-60 object-cover transition-transform duration-300 hover:scale-105"
                    />
                  ) : (
                    <div className="relative w-full h-60">
                      <img
                        src="/8257026.jpg"
                        alt="default property"
                        className="w-full h-60 object-cover"
                      />
                      <div className="absolute inset-0 flex items-center justify-center bg-black/30">
                        <span className="text-white font-semibold text-sm">
                          No Image Available
                        </span>
                      </div>
                    </div>
                  )}
                  <span className="absolute top-3 right-3 bg-indigo-600 text-white text-xs px-4 py-1 rounded-full shadow-md">
                    {prop.bhk ? `${prop.bhk} BHK` : "Property"}
                  </span>
                </div>

                {/* Content */}
                <div className="p-6 flex-1 flex flex-col">
                  <h3 className="text-2xl font-bold text-indigo-700 mb-2">
                    {prop.broker_name}
                  </h3>
                  <p className="text-gray-600 mb-4 line-clamp-3 text-sm">
                    {prop.description}
                  </p>

                  {/* Property Info Badges */}
                  <div className="grid grid-cols-2 gap-3 text-sm font-medium text-gray-800 mb-4">
                    <span className="bg-indigo-50 text-indigo-700 px-3 py-1 rounded-xl shadow-sm flex items-center gap-1">
                      💲 {prop.ai_structure?.rent_amount || "N/A"}
                    </span>
                    <span className="bg-green-50 text-green-700 px-3 py-1 rounded-xl shadow-sm flex items-center gap-1">
                      📍 {prop.ai_structure?.location || "Unknown"}
                    </span>
                    <span className="bg-yellow-50 text-yellow-700 px-3 py-1 rounded-xl shadow-sm flex items-center gap-1">
                      🛋 {prop.ai_structure?.furnishing || "N/A"}
                    </span>
                    <span className="bg-pink-50 text-pink-700 px-3 py-1 rounded-xl shadow-sm flex items-center gap-1">
                      🔑 Deposit: {prop.ai_structure?.deposit_amount || "N/A"}
                    </span>
                  </div>

                  <div className="flex-grow"></div>

                  {/* Footer */}
                  <div className="text-xs text-gray-500 mt-3 border-t pt-3">
                    Posted on{" "}
                    {new Date(prop.timestamp).toLocaleDateString(undefined, {
                      month: "short",
                      day: "numeric",
                      year: "numeric",
                    })}{" "}
                    at{" "}
                    {new Date(prop.timestamp).toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
