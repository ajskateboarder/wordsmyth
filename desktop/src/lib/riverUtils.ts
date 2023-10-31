import { getClient, ResponseType } from "@tauri-apps/api/http";
import type BinaryFileContents from "@tauri-apps/api/fs";

export async function getLatestRelease(): Promise<string[]> {
  const client = await getClient();
  const response = await client.get(
    "https://api.github.com/repos/ajskateboarder/river/releases/latest",
    {
      headers: { "User-Agent": "bot" },
      timeout: 30,
      responseType: ResponseType.JSON,
    }
  );
  const downloadLinks = (response.data as Record<string, any>).assets.map(
    (item: any) => item.browser_download_url
  );
  return downloadLinks;
}

export async function downloadEXE(url: string) {
  const client = await getClient();
  return (
    await client.get(url, {
      headers: { "User-Agent": "bot" },
      timeout: 30,
      responseType: ResponseType.Binary,
    })
  ).data as BinaryFileContents;
}

export type Response = {
  type: "status" | "response";
  message?: string;
  reviewText: string;
  overall: number;
  productId: string;
  title: string;
  image: string;
  rating: string;
};
