import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Props {
  markdown: string;
}

export function FinalReportRenderer({ markdown }: Props) {
  if (!markdown) return <p className="text-slate-400">Report not yet generated.</p>;

  return (
    <div className="prose prose-invert prose-purple max-w-none">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
    </div>
  );
}
