use anchor_lang::prelude::*;
use crate::state::{TravelGoal, Sponsorship};
use crate::errors::TravelError;

#[derive(Accounts)]
pub struct RefundSponsor<'info> {
    #[account(mut)]
    pub travel_goal: Account<'info, TravelGoal>,
    #[account(mut, has_one = goal @ TravelError::Unauthorized)]
    pub sponsorship: Account<'info, Sponsorship>,
    #[account(mut)]
    pub sponsor: SystemAccount<'info>,
    pub authority: Signer<'info>,
}

pub fn handler(ctx: Context<RefundSponsor>) -> Result<()> {
    let sp = &mut ctx.accounts.sponsorship;
    require!(!sp.refunded, TravelError::AlreadyRefunded);
    require!(ctx.accounts.authority.key() == ctx.accounts.travel_goal.authority, TravelError::Unauthorized);

    let amount = sp.amount_lamports;
    sp.refunded = true;
    ctx.accounts.travel_goal.funded_lamports -= amount;

    **ctx.accounts.travel_goal.to_account_info().try_borrow_mut_lamports()? -= amount;
    **ctx.accounts.sponsor.try_borrow_mut_lamports()? += amount;

    Ok(())
}
