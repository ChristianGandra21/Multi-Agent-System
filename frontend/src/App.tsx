import React, { useState } from "react";
import { SearchBar } from "./components/SearchBar";
import { AgentStatus } from "./components/AgentStatus";
import { researchService } from "./services/api";
import { ReportView } from "./components/ReportView";

function App() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const handleSearch = async (query: string) => {
    setLoading(true);
    try {
      const response = await researchService.createResearch(query);
      setData(response);

      const interval = setInterval(async () => {
        const updated = await researchService.getResearchStatus(response.id);
        setData(updated);
        if (updated.status === "completed" || updated.status === "failed") {
          clearInterval(interval);
          setLoading(false);
        }
      }, 3000);
    } catch (err) {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-10 flex items-center gap-2">
          <div className="bg-blue-600 p-2 rounded-lg font-bold text-white italic">
            AI
          </div>
          <h1 className="text-2xl font-bold">Research Station</h1>
        </header>

        <SearchBar onSearch={handleSearch} isLoading={loading} />

        {data && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="md:col-span-1">
              <AgentStatus data={data} />
            </div>
            <div className="md:col-span-3 bg-slate-800/40 border border-slate-700 rounded-2xl p-6">
              {data.status === "completed" ? (
                <div className="space-y-6">
                  <ReportView report={data.final_report} />
                  
                  {/* Exibir gráfico se disponível */}
                  {data.code_outputs?.chart_base64 && (
                    <div className="mt-6 border-t border-slate-700 pt-6">
                      <h3 className="text-lg font-semibold mb-4 text-slate-300">📊 Visualização de Dados</h3>
                      <img 
                        src={`data:image/png;base64,${data.code_outputs.chart_base64}`}
                        alt="Gráfico gerado pela IA"
                        className="max-w-full h-auto rounded-lg border border-slate-600"
                      />
                    </div>
                  )}
                </div>
              ) : (
                <div className="h-64 flex items-center justify-center text-slate-500 italic">
                  Processando inteligência...
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
