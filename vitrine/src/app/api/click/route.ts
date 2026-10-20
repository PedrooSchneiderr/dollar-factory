import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const line = JSON.stringify(body);

    // Em producao (Vercel) o filesystem e somente leitura: registra no log do runtime.
    console.log("[click]", line);

    // Em desenvolvimento local, mantem tambem o arquivo clicks_log.jsonl.
    if (!process.env.VERCEL) {
      const logPath = path.join(process.cwd(), "clicks_log.jsonl");
      fs.appendFileSync(logPath, line + "\n", "utf-8");
    }
    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ ok: false }, { status: 400 });
  }
}
