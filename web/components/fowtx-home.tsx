"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { ArrowRight, BookOpenText, ExternalLink, FileText, Waves } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

const examples = ["Dynamic cables", "Mooring", "Hydrodynamics", "Platforms"];

export function FowtxHome() {
  const [question, setQuestion] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
  }

  return (
    <main className="min-h-screen bg-[linear-gradient(180deg,#f8faf9_0%,#eef4f2_100%)] text-slate-950">
      <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-5 py-5 sm:px-8 lg:px-10">
        <header className="flex items-center justify-between border-b border-slate-200/80 pb-4">
          <Link href="/" className="flex items-center gap-3" aria-label="FOWTX home">
            <span className="flex size-9 items-center justify-center rounded-md border border-teal-900/15 bg-white text-teal-800 shadow-sm">
              <Waves className="size-4" aria-hidden="true" />
            </span>
            <span className="text-sm font-semibold tracking-[0.22em] text-slate-900">FOWTX</span>
          </Link>
          <a
            href="https://github.com/yangzhouore/fowtx_rag"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 rounded-md px-2 py-1 text-sm font-medium text-slate-600 transition-colors hover:text-slate-950"
          >
            GitHub
            <ExternalLink className="size-3.5" aria-hidden="true" />
          </a>
        </header>

        <section className="grid flex-1 items-start gap-10 py-8 lg:grid-cols-[minmax(0,1.08fr)_minmax(320px,0.92fr)] lg:py-10">
          <div className="max-w-3xl">
            <div className="mb-6 inline-flex items-center gap-2 rounded-md border border-teal-900/10 bg-white/80 px-3 py-1 text-sm font-medium text-teal-900 shadow-sm">
              <BookOpenText className="size-4" aria-hidden="true" />
              Engineering research interface
            </div>

            <h1 className="max-w-3xl text-5xl font-semibold leading-[1.02] tracking-normal text-slate-950 sm:text-6xl lg:text-7xl">
              Floating Offshore Wind Knowledge Base
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600 sm:text-xl">
              Engineering and research knowledge for floating offshore wind systems, from platform concepts to moorings, hydrodynamics, and dynamic export cables.
            </p>

            <form onSubmit={handleSubmit} className="mt-9 max-w-2xl">
              <div className="rounded-lg border border-slate-200 bg-white p-2 shadow-sm shadow-slate-200/70">
                <label htmlFor="question" className="sr-only">
                  Ask a floating offshore wind question
                </label>
                <Textarea
                  id="question"
                  value={question}
                  onChange={(event) => setQuestion(event.target.value)}
                  placeholder="Ask about platforms, moorings, cables, installation methods..."
                  className="min-h-28 resize-none border-0 bg-transparent px-3 py-3 text-base leading-7 shadow-none focus-visible:ring-0"
                />
                <div className="flex items-center justify-between gap-3 border-t border-slate-100 px-3 py-2">
                  <span className="text-xs font-medium text-slate-500">Ask a question to explore the knowledge base.</span>
                  <Button type="submit" size="icon" aria-label="Submit question" className="rounded-md bg-teal-800 text-white hover:bg-teal-900">
                    <ArrowRight className="size-4" aria-hidden="true" />
                  </Button>
                </div>
              </div>
            </form>

            <div className="mt-7 flex flex-wrap items-center gap-2">
              <span className="mr-1 text-sm font-medium text-slate-500">Explore:</span>
              {examples.map((example) => (
                <button key={example} type="button" onClick={() => setQuestion(example)}>
                  <Badge variant="secondary" className="rounded-md border border-slate-200 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 hover:border-teal-800/30 hover:text-teal-900">
                    {example}
                  </Badge>
                </button>
              ))}
            </div>
          </div>

          <aside className="border-t border-slate-200 pt-8 lg:border-l lg:border-t-0 lg:pl-10 lg:pt-0">
            <div className="space-y-6">
              <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex items-center gap-3 text-slate-900">
                  <FileText className="size-5 text-teal-800" aria-hidden="true" />
                  <h2 className="text-lg font-semibold">Answer</h2>
                </div>
                <p className="mt-4 text-sm leading-6 text-slate-500">
                  Answers and supporting sources will appear here.
                </p>
              </section>

              <section className="rounded-lg border border-dashed border-slate-300 bg-white/70 p-6">
                <h2 className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-500">Sources</h2>
                <div className="mt-4 space-y-3">
                  <div className="h-3 w-3/4 rounded bg-slate-200" />
                  <div className="h-3 w-2/3 rounded bg-slate-200" />
                  <div className="h-3 w-1/2 rounded bg-slate-200" />
                </div>
                <p className="mt-5 text-sm leading-6 text-slate-500">
                  Source citations and page references will be listed here with each future answer.
                </p>
              </section>
            </div>
          </aside>
        </section>
      </div>
    </main>
  );
}