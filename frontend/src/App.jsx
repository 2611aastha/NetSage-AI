import React, { useState, useEffect } from 'react';

export default function App() {
  const [cases, setCases] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [diagnosis, setDiagnosis] = useState(null);
  const [ruleResults, setRuleResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/api/cases')
      .then(res => res.json())
      .then(data => {
        setCases(data);
        if (data.length > 0) handleSelectCase(data[0]);
      })
      .catch(err => console.error("API error:", err));
  }, []);

  const handleSelectCase = (c) => {
    setSelectedCase(c);
    setLoading(true);
    setDiagnosis(null);
    setRuleResults([]);

    Promise.all([
      fetch(`http://localhost:8000/api/diagnose/${c.case_id}`, { method: 'POST' }).then(r => r.json()),
      fetch(`http://localhost:8000/api/rule-check/${c.case_id}`, { method: 'POST' }).then(r => r.json())
    ]).then(([diagData, rulesData]) => {
      setDiagnosis(diagData);
      setRuleResults(rulesData);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  const handleReview = (decision) => {
    if (!selectedCase) return;

    fetch('http://localhost:8000/api/review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        case_id: selectedCase.case_id,
        decision: decision,
        notes: `Operator selected ${decision} on case ${selectedCase.case_id}`
      })
    })
      .then(res => res.json())
      .then(data => {
        alert(`Decision Logged: ${decision}`);
      })
      .catch(err => {
        console.error("Failed to log review:", err);
        alert("Error logging decision to backend.");
      });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Navigation Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 px-6 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-wide text-cyan-400">NetSage AI</h1>
          <p className="text-xs text-slate-400">Evidence-Backed Network Troubleshooting System</p>
        </div>
        <div className="bg-amber-500/10 border border-amber-500/30 text-amber-400 px-3 py-1 rounded text-xs font-mono">
          HUMAN REVIEW REQUIRED — ADVISORY MODE ONLY
        </div>
      </header>

      {/* Main Operations Grid */}
      <div className="flex-1 grid grid-cols-12 gap-6 p-6">
        {/* Left Table Panel */}
        <div className="col-span-5 bg-slate-900 border border-slate-800 rounded-lg p-4 flex flex-col">
          <h2 className="text-sm font-semibold text-slate-300 uppercase font-mono mb-3">Diagnostic Cases</h2>
          <div className="overflow-y-auto flex-1 space-y-2 max-h-[70vh]">
            {cases.map((c) => (
              <div
                key={c.case_id}
                onClick={() => handleSelectCase(c)}
                className={`p-3 rounded border cursor-pointer transition ${
                  selectedCase?.case_id === c.case_id
                    ? 'bg-slate-800 border-cyan-500/50'
                    : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex justify-between items-center mb-1">
                  <span className="font-mono text-xs font-bold text-cyan-400">{c.case_id}</span>
                  <span className={`text-[10px] px-2 py-0.5 rounded uppercase font-mono ${
                    c.severity === 'Critical' ? 'bg-red-950 text-red-300 border border-red-800' : 'bg-slate-800 text-slate-300'
                  }`}>
                    {c.severity}
                  </span>
                </div>
                <p className="text-xs text-slate-300 truncate">{c.symptom}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Inspection & Review Workspace */}
        <div className="col-span-7 bg-slate-900 border border-slate-800 rounded-lg p-6 overflow-y-auto max-h-[80vh]">
          {selectedCase ? (
            <div className="space-y-6">
              <div>
                <span className="text-xs font-mono text-cyan-400">{selectedCase.case_id} — Detail View</span>
                <h2 className="text-lg font-bold text-white mt-1">{selectedCase.symptom}</h2>
                <p className="text-xs text-slate-400 font-mono mt-1">{selectedCase.topology_note}</p>
              </div>

              {/* Show Outputs */}
              <div className="bg-slate-950 border border-slate-800 rounded p-3">
                <div className="text-xs font-mono text-slate-400 mb-2 uppercase">CLI Evidence Output</div>
                <pre className="text-xs font-mono text-emerald-400 whitespace-pre-wrap">{selectedCase.show_outputs}</pre>
              </div>

              {/* Rule Checker Output */}
              <div>
                <h3 className="text-xs font-mono text-slate-400 uppercase mb-2">Deterministic Rule Checker</h3>
                <div className="space-y-2">
                  {ruleResults.map((r, i) => (
                    <div key={i} className={`p-2.5 rounded border text-xs font-mono ${
                      r.status === 'FAIL' ? 'bg-red-950/30 border-red-800/50 text-red-300' : 'bg-slate-950 border-slate-800 text-slate-400'
                    }`}>
                      <div className="font-bold">{r.check_name}: {r.status}</div>
                      <div>{r.explanation}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* AI Diagnosis Panel */}
              {loading ? (
                <div className="text-xs font-mono text-slate-400 animate-pulse">Running Diagnostic AI Engine...</div>
              ) : diagnosis ? (
                <div className="bg-slate-950 border border-violet-900/40 rounded p-4 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-mono text-violet-400">AI Diagnostic Inference</span>
                    <span className="text-xs font-mono text-teal-400">Confidence: {diagnosis.confidence}%</span>
                  </div>
                  <div className="text-sm font-semibold text-slate-200">{diagnosis.root_cause}</div>
                  
                  <div className="text-xs font-mono text-slate-400">
                    <div className="font-bold text-slate-300 mb-1">Recommended Commands:</div>
                    <code className="text-cyan-300">{diagnosis.next_command}</code>
                  </div>

                  {/* Human Decision Buttons */}
                  <div className="pt-3 border-t border-slate-800 flex gap-2">
                    <button 
                      onClick={() => handleReview("ACCEPTED")} 
                      className="px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-white rounded text-xs font-sans cursor-pointer transition"
                    >
                      Accept Fix
                    </button>
                    <button 
                      onClick={() => handleReview("REJECTED")} 
                      className="px-3 py-1.5 bg-red-950 hover:bg-red-900 text-red-200 border border-red-800 rounded text-xs font-sans cursor-pointer transition"
                    >
                      Reject
                    </button>
                  </div>
                </div>
              ) : null}
            </div>
          ) : (
            <div className="text-xs font-mono text-slate-500">Select a diagnostic case from the queue.</div>
          )}
        </div>
      </div>
    </div>
  );
}