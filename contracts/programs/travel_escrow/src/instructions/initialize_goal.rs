use anchor_lang::prelude::*;
use crate::state::TravelGoal;

#[derive(Accounts)]
#[instruction(goal_id: String)]
pub struct InitializeGoal<'info> {
    #[account(
        init,
        payer = traveler,
        space = TravelGoal::LEN,
        seeds = [b"goal", goal_id.as_bytes()],
        bump
    )]
    pub travel_goal: Account<'info, TravelGoal>,
    #[account(mut)]
    pub traveler: Signer<'info>,
    /// CHECK: backend authority pubkey
    pub authority: UncheckedAccount<'info>,
    pub system_program: Program<'info, System>,
}

pub fn handler(ctx: Context<InitializeGoal>, goal_id: String, target_lamports: u64) -> Result<()> {
    let goal = &mut ctx.accounts.travel_goal;
    goal.goal_id = goal_id;
    goal.traveler = ctx.accounts.traveler.key();
    goal.authority = ctx.accounts.authority.key();
    goal.target_lamports = target_lamports;
    goal.funded_lamports = 0;
    goal.released = false;
    goal.bump = ctx.bumps.travel_goal;
    Ok(())
}
