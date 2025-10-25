import React, { useState } from 'react';
import { Search, Play, Pause, Download, Trash2 } from 'lucide-react';

const AudioManager = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [playingId, setPlayingId] = useState(null);
  const [hoveredRow, setHoveredRow] = useState(null);

  const audioFiles = [
    {
      id: 1,
      filename: 'Rec.001.wav',
      date: 'Apr, 12, 2025',
      labels: ['Persona Recognition', 'Max Mustermann']
    },
    {
      id: 2,
      filename: 'Rec.001.wav',
      date: 'Apr, 12, 2025',
      labels: ['Commander conversation', 'Background activity']
    },
    {
      id: 3,
      filename: 'Rec.001.wav',
      date: 'Apr, 12, 2025',
      labels: ['Persona Recognition', 'Max Mustermann']
    },
    {
      id: 4,
      filename: 'Rec.001.wav',
      date: 'Apr, 12, 2025',
      labels: ['Location Identification', 'Niu-York', 'Train noises']
    },
    {
      id: 5,
      filename: 'Rec.001.wav',
      date: 'Apr, 12, 2025',
      labels: ['Noises', 'River']
    }
  ];

  const filteredFiles = audioFiles.filter(file => 
    file.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
    file.labels.some(label => label.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const handlePlay = (id) => {
    setPlayingId(playingId === id ? null : id);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12 animate-fadeIn">
          <div className="flex items-center gap-3 mb-8">
            <div className="relative">
              <div className="w-12 h-12 rounded-full bg-cyan-500 flex items-center justify-center animate-pulse">
                <div className="w-8 h-8 rounded-full border-4 border-white"></div>
              </div>
              <div className="absolute inset-0 w-12 h-12 rounded-full bg-cyan-400 animate-ping opacity-20"></div>
            </div>
            <h1 className="text-4xl font-bold text-white">Echologia</h1>
          </div>

          {/* Search Bar */}
          <div className="relative group">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-cyan-400 w-5 h-5 transition-all group-hover:scale-110" />
            <input
              type="text"
              placeholder="Search anything..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-800/50 border border-slate-700 rounded-xl py-4 pl-12 pr-4 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:bg-slate-800/80 transition-all duration-300 backdrop-blur-sm"
            />
          </div>
        </div>

        {/* Table */}
        <div className="bg-slate-800/30 backdrop-blur-md rounded-2xl border border-slate-700/50 overflow-hidden shadow-2xl">
          {/* Table Header */}
          <div className="grid grid-cols-12 gap-4 px-6 py-4 bg-slate-800/50 border-b border-slate-700/50">
            <div className="col-span-3 text-slate-400 text-sm font-semibold tracking-wider uppercase">File Name</div>
            <div className="col-span-2 text-slate-400 text-sm font-semibold tracking-wider uppercase">Date</div>
            <div className="col-span-6 text-slate-400 text-sm font-semibold tracking-wider uppercase">Labels</div>
            <div className="col-span-1 text-slate-400 text-sm font-semibold tracking-wider uppercase">Actions</div>
          </div>

          {/* Table Body */}
          <div className="divide-y divide-slate-700/30">
            {filteredFiles.map((file, index) => (
              <div
                key={file.id}
                className={`grid grid-cols-12 gap-4 px-6 py-5 transition-all duration-300 cursor-pointer ${
                  hoveredRow === file.id ? 'bg-slate-700/30 scale-[1.01]' : 'hover:bg-slate-700/20'
                }`}
                onMouseEnter={() => setHoveredRow(file.id)}
                onMouseLeave={() => setHoveredRow(null)}
                style={{
                  animation: `slideIn 0.5s ease-out ${index * 0.1}s both`
                }}
              >
                {/* Filename */}
                <div className="col-span-3 flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    playingId === file.id ? 'bg-cyan-400 animate-pulse' : 'bg-slate-600'
                  }`}></div>
                  <span className="text-slate-200 font-medium">{file.filename}</span>
                </div>

                {/* Date */}
                <div className="col-span-2 flex items-center text-slate-400">
                  {file.date}
                </div>

                {/* Labels */}
                <div className="col-span-6 flex flex-wrap gap-2 items-center">
                  {file.labels.map((label, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-slate-700/50 text-cyan-300 text-sm rounded-full border border-slate-600/50 transition-all duration-300 hover:bg-slate-600/50 hover:scale-105"
                      style={{
                        animation: `fadeIn 0.5s ease-out ${index * 0.1 + idx * 0.05}s both`
                      }}
                    >
                      {label}
                    </span>
                  ))}
                </div>

                {/* Actions */}
                <div className="col-span-1 flex items-center gap-2">
                  <button
                    onClick={() => handlePlay(file.id)}
                    className="p-2 rounded-lg bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30 transition-all duration-300 hover:scale-110"
                  >
                    {playingId === file.id ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Stats Footer */}
        <div className="mt-8 flex justify-between items-center text-slate-400 text-sm">
          <div className="flex gap-6">
            <span className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-cyan-400"></div>
              {filteredFiles.length} recordings
            </span>
            <span className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-400"></div>
              All synced
            </span>
          </div>
          <div>Last updated: Today</div>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateX(-20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        .animate-fadeIn {
          animation: fadeIn 0.8s ease-out;
        }
      `}</style>
    </div>
  );
};

export default AudioManager;