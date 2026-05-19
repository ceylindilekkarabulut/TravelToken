use anchor_lang::prelude::*;

pub mod errors;
pub mod instructions;
pub mod state;

use instructions::*;

declare_id!("F5bahTsQSG9ukd4X6PUTQLZ8MkyX35qnkRYi9rRijMhh");

#[program]
pub mod travel_escrow {
    use super::*;

    pub fn initialize_goal(
        ctx: Context<InitializeGoal>,
        goal_id: String,
        target_lamports: u64,
    ) -> Result<()> {
        instructions::initialize_goal::handler(ctx, goal_id, target_lamports)
    }

    pub fn sponsor(ctx: Context<Sponsor>, amount_lamports: u64) -> Result<()> {
        instructions::sponsor::handler(ctx, amount_lamports)
    }

    pub fn release_funds(ctx: Context<ReleaseFunds>) -> Result<()> {
        instructions::release_funds::handler(ctx)
    }

    pub fn refund_sponsor(ctx: Context<RefundSponsor>) -> Result<()> {
        instructions::refund_sponsor::handler(ctx)
    }
}
