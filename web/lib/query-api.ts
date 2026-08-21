export type QueryResponse = {
  answer: string;
  sources: string[];
};

type ErrorResponse = {
  detail?: string;
};

const DEFAULT_ERROR = "The knowledge service is unavailable. Try again in a moment.";

export async function queryKnowledgeBase(question: string): Promise<QueryResponse> {
  const response = await fetch("/api/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    let errorResponse: ErrorResponse = {};

    try {
      errorResponse = (await response.json()) as ErrorResponse;
    } catch {
      errorResponse = {};
    }

    throw new Error(errorResponse.detail ?? DEFAULT_ERROR);
  }

  return (await response.json()) as QueryResponse;
}
