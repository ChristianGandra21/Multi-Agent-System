import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export const ReportView = ({ report }: { report: string }) => {
    if (! report) return null;

    return (
        <div className="prose prose-invert max-w-none prose-blue prose-table:border prose-table:border-slate-700">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {report}
        </ReactMarkdown>
        </div>
    );
    };