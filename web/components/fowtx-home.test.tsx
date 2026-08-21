import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FowtxHome } from "@/components/fowtx-home";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("FowtxHome", () => {
  it("does not submit blank questions", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);

    render(<FowtxHome />);

    fireEvent.change(screen.getByLabelText("Ask a floating offshore wind question"), {
      target: { value: "   " },
    });
    fireEvent.submit(screen.getByRole("button", { name: "Submit question" }).closest("form")!);

    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("submits valid questions to the frontend query route", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ answer: "A semi-submersible uses buoyant columns.", sources: [] }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<FowtxHome />);

    fireEvent.change(screen.getByLabelText("Ask a floating offshore wind question"), {
      target: { value: "What is a semi-submersible platform?" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Submit question" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/query",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ question: "What is a semi-submersible platform?" }),
      }),
    );
  });

  it("shows loading while the query is in flight", async () => {
    let resolveQuery: (response: Response) => void = () => {};
    const queryPromise = new Promise<Response>((resolve) => {
      resolveQuery = resolve;
    });
    const fetchMock = vi.fn().mockReturnValue(queryPromise);
    vi.stubGlobal("fetch", fetchMock);

    render(<FowtxHome />);

    fireEvent.change(screen.getByLabelText("Ask a floating offshore wind question"), {
      target: { value: "Dynamic cables" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Submit question" }));

    expect(await screen.findAllByText("Searching the knowledge base...")).not.toHaveLength(0);

    resolveQuery(
      new Response(JSON.stringify({ answer: "Dynamic cables tolerate motion.", sources: [] }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    expect(await screen.findByText("Dynamic cables tolerate motion.")).toBeInTheDocument();
  });

  it("renders successful answers and returned sources", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          answer: "Mooring systems keep floating platforms on station.",
          sources: ["source-a.pdf (page 1)", "source-b.pdf (page 4)"],
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<FowtxHome />);

    fireEvent.change(screen.getByLabelText("Ask a floating offshore wind question"), {
      target: { value: "Mooring" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Submit question" }));

    expect(await screen.findByText("Mooring systems keep floating platforms on station.")).toBeInTheDocument();
    expect(screen.getByText("source-a.pdf (page 1)")).toBeInTheDocument();
    expect(screen.getByText("source-b.pdf (page 4)")).toBeInTheDocument();
  });

  it("shows a user-facing error on query failure", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: "RAG service unavailable" }), {
        status: 503,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<FowtxHome />);

    fireEvent.change(screen.getByLabelText("Ask a floating offshore wind question"), {
      target: { value: "Platforms" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Submit question" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("The knowledge service is unavailable. Try again in a moment.");
  });
  it("clears stale answer and sources when a follow-up query starts and fails", async () => {
    let resolveSecondQuery: (response: Response) => void = () => {};
    const secondQueryPromise = new Promise<Response>((resolve) => {
      resolveSecondQuery = resolve;
    });
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            answer: "First answer about mooring.",
            sources: ["first-source.pdf (page 2)"],
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      )
      .mockReturnValueOnce(secondQueryPromise);
    vi.stubGlobal("fetch", fetchMock);

    render(<FowtxHome />);

    fireEvent.change(screen.getByLabelText("Ask a floating offshore wind question"), {
      target: { value: "Mooring" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Submit question" }));

    expect(await screen.findByText("First answer about mooring.")).toBeInTheDocument();
    expect(screen.getByText("first-source.pdf (page 2)")).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("Ask a floating offshore wind question"), {
      target: { value: "Platforms" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Submit question" }));

    expect(await screen.findAllByText("Searching the knowledge base...")).not.toHaveLength(0);
    expect(screen.queryByText("First answer about mooring.")).not.toBeInTheDocument();
    expect(screen.queryByText("first-source.pdf (page 2)")).not.toBeInTheDocument();

    resolveSecondQuery(
      new Response(JSON.stringify({ detail: "RAG service unavailable" }), {
        status: 503,
        headers: { "Content-Type": "application/json" },
      }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent("The knowledge service is unavailable. Try again in a moment.");
    expect(screen.queryByText("First answer about mooring.")).not.toBeInTheDocument();
    expect(screen.queryByText("first-source.pdf (page 2)")).not.toBeInTheDocument();
  });
});
