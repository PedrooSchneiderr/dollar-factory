import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const logPath = path.join(process.cwd(), "clicks_log.jsonl");
    fs.appendFileSync(logPath, JSON.stringify(body) + "\n", "utf-8");
    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ ok: false }, { status: 400 });
  }
}
