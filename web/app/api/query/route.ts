import { NextRequest, NextResponse } from "next/server";

type QueryRequest = {
  question?: unknown;
};

const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";
const SERVICE_UNAVAILABLE = "The knowledge service is unavailable. Try again in a moment.";

function queryUrl() {
  return new URL("/query", process.env.FOWTX_API_BASE_URL ?? DEFAULT_API_BASE_URL);
}

export async function POST(request: NextRequest) {
  const body = (await request.json()) as QueryRequest;
  const question = typeof body.question === "string" ? body.question.trim() : "";

  if (!question) {
    return NextResponse.json({ detail: "Enter a question to search the knowledge base." }, { status: 400 });
  }

  try {
    const response = await fetch(queryUrl(), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      return NextResponse.json({ detail: SERVICE_UNAVAILABLE }, { status: response.status });
    }

    return NextResponse.json(await response.json());
  } catch {
    return NextResponse.json({ detail: SERVICE_UNAVAILABLE }, { status: 502 });
  }
}
