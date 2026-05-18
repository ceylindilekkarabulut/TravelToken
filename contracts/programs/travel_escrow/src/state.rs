use anchor_lang::prelude::*;

#[account]
pub struct TravelGoal {
    pub goal_id: String,
    pub traveler: Pubkey,
    pub authority: Pubkey,
    pub target_lamports: u64,
    pub funded_lamports: u64,
    pub released: bool,
    pub bump: u8,
}

impl TravelGoal {
    pub const LEN: usize = 8 + 64 + 32 + 32 + 8 + 8 + 1 + 1;
}

#[account]
pub struct Sponsorship {
    pub goal: Pubkey,
    pub sponsor: Pubkey,
    pub amount_lamports: u64,
    pub refunded: bool,
    pub bump: u8,
}

impl Sponsorship {
    pub const LEN: usize = 8 + 32 + 32 + 8 + 1 + 1;
}
