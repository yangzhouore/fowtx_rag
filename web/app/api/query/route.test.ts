import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";

import { POST } from "@/app/api/query/route";

function request(question: string) {
  return new NextRequest("http://localhost/api/query", {
    method: "POST",
    body: JSON.stringify({ question }),
  });
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

describe("POST /api/query", () => {
  it("forwards the question to the configured FastAPI query endpoint", async () => {
    vi.stubEnv("FOWTX_API_BASE_URL", "http://fastapi.test:8000");
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ answer: "Answer", sources: ["source.pdf (page 1)"] }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    const response = await POST(request("  What is spar?  "));

    expect(fetchMock).toHaveBeenCalledWith(
      new URL("http://fastapi.test:8000/query"),
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ question: "What is spar?" }),
      }),
    );
    expect(response.status).toBe(200);
  });

  it("returns successful backend JSON", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ answer: "Answer", sources: ["source.pdf (page 1)"] }), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    const response = await POST(request("Mooring"));

    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({ answer: "Answer", sources: ["source.pdf (page 1)"] });
  });

  it("returns a controlled error for backend failures", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: "internal details" }), {
          status: 503,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    const response = await POST(request("Hydrodynamics"));

    expect(response.status).toBe(503);
    await expect(response.json()).resolves.toEqual({ detail: "The knowledge service is unavailable. Try again in a moment." });
  });

  it("returns a controlled error for network failures", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("network unavailable")));

    const response = await POST(request("Platforms"));

    expect(response.status).toBe(502);
    await expect(response.json()).resolves.toEqual({ detail: "The knowledge service is unavailable. Try again in a moment." });
  });
});
