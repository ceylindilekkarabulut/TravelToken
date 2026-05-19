use anchor_lang::prelude::*;
use anchor_lang::system_program;
use crate::state::{TravelGoal, Sponsorship};
use crate::errors::TravelError;

#[derive(Accounts)]
pub struct Sponsor<'info> {
    #[account(mut)]
    pub travel_goal: Account<'info, TravelGoal>,
    #[account(
        init,
        payer = sponsor,
        space = Sponsorship::LEN,
        seeds = [b"sponsorship", travel_goal.key().as_ref(), sponsor.key().as_ref()],
        bump
    )]
    pub sponsorship: Account<'info, Sponsorship>,
    #[account(mut)]
    pub sponsor: Signer<'info>,
    pub system_program: Program<'info, System>,
}

pub fn handler(ctx: Context<Sponsor>, amount_lamports: u64) -> Result<()> {
    require!(!ctx.accounts.travel_goal.released, TravelError::AlreadyReleased);

    system_program::transfer(
        CpiContext::new(
            ctx.accounts.system_program.to_account_info(),
            system_program::Transfer {
                from: ctx.accounts.sponsor.to_account_info(),
                to: ctx.accounts.travel_goal.to_account_info(),
            },
        ),
        amount_lamports,
    )?;

    let sp = &mut ctx.accounts.sponsorship;
    sp.goal = ctx.accounts.travel_goal.key();
    sp.sponsor = ctx.accounts.sponsor.key();
    sp.amount_lamports = amount_lamports;
    sp.refunded = false;
    sp.bump = ctx.bumps.sponsorship;

    ctx.accounts.travel_goal.funded_lamports += amount_lamports;

    emit!(GoalFunded {
        goal: ctx.accounts.travel_goal.key(),
        total_funded: ctx.accounts.travel_goal.funded_lamports,
    });

    Ok(())
}

#[event]
pub struct GoalFunded {
    pub goal: Pubkey,
    pub total_funded: u64,
}
