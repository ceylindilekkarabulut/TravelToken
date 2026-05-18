import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { wallet, signature } = await req.json();
  if (!wallet) return NextResponse.json({ error: "Missing wallet" }, { status: 400 });
  // TODO: verify signature, issue session cookie
  return NextResponse.json({ ok: true, wallet });
}
