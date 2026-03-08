const API_BASE_URL = "http://localhost:8000";

export type TelemetryRequest = {
  year: number;
  session: string;
  driver: string;
};

export async function getApiHealth(): Promise<{ status: string; service: string }> {
  const response = await fetch(`${API_BASE_URL}/`, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`Health check failed with status ${response.status}`);
  }

  return response.json();
}

export async function getDriverTelemetry(params: TelemetryRequest): Promise<unknown> {
  const query = new URLSearchParams({
    year: String(params.year),
    session: params.session,
    driver: params.driver,
  });

  const response = await fetch(`${API_BASE_URL}/telemetry?${query.toString()}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Telemetry request failed with status ${response.status}`);
  }

  return response.json();
}
