export interface GoalResponse {
  id: string;
  user_wallet: string;
  destination: string;
  origin: string;
  travel_date: string;
  budget_usd: number;
  status: string;
  final_report_md: string | null;
  solana_goal_pda: string | null;
  created_at: string;
}

export interface SponsorshipResponse {
  id: string;
  goal_id: string;
  sponsor_wallet: string;
  amount_sol: number;
  tx_signature: string | null;
  refunded: boolean;
  created_at: string;
}

export interface RouteResponse {
  id: string;
  origin: string;
  destination: string;
  description_md: string;
  tags: string;
  copy_count: number;
  creator_wallet: string | null;
  created_at: string;
}

export interface PriceHistoryEntry {
  id: number;
  goal_id: string;
  flight_price_usd: number | null;
  hotel_price_usd: number | null;
  is_buy_signal: boolean;
  recorded_at: string;
}
