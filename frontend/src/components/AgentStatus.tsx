import React from 'react';
import { Globe, BarChart3, PenTool, Loader2 } from 'lucide-react';

export const AgentStatus = ({ data }: { data: any }) => {
  const getStatus = (step: string) => {
    if (!data) return 'wait';
    if (step === 'research') return data.status === 'pending' ? 'loading' : 'done';
    if (step === 'data') return data.analysis_data ? 'done' : (data.status === 'processing' ? 'loading' : 'wait');
    if (step === 'writer') return data.status === 'completed' ? 'done' : 'wait';
    return 'wait';
  };

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-semibold uppercase text-slate-500 mb-4 tracking-wider">Fluxo de Agentes</h3>
      <StatusItem icon={<Globe size={18} />} label="Research" status={getStatus('research')} />
      <StatusItem icon={<BarChart3 size={18} />} label="Analysis" status={getStatus('data')} />
      <StatusItem icon={<PenTool size={18} />} label="Writing" status={getStatus('writer')} />
    </div>
  );
};

const StatusItem = ({ icon, label, status }: any) => {
  const styles: any = {
    done: "border-green-500/30 bg-green-500/5 text-green-400",
    loading: "border-blue-500/50 bg-blue-500/10 text-blue-400 animate-pulse",
    wait: "border-slate-700 bg-slate-800/50 text-slate-500 opacity-50"
  };

  return (
    <div className={`border p-4 rounded-xl flex items-center gap-3 transition-all ${styles[status]}`}>
      {status === 'loading' ? <Loader2 size={18} className="animate-spin" /> : icon}
      <span className="font-bold">{label}</span>
    </div>
  );
};