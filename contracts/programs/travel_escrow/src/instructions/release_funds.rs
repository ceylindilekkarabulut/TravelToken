use anchor_lang::prelude::*;
use crate::state::TravelGoal;
use crate::errors::TravelError;

#[derive(Accounts)]
pub struct ReleaseFunds<'info> {
    #[account(mut)]
    pub travel_goal: Account<'info, TravelGoal>,
    #[account(mut)]
    pub traveler: SystemAccount<'info>,
    pub authority: Signer<'info>,
}

pub fn handler(ctx: Context<ReleaseFunds>) -> Result<()> {
    let goal = &mut ctx.accounts.travel_goal;
    require!(!goal.released, TravelError::AlreadyReleased);
    require!(ctx.accounts.authority.key() == goal.authority, TravelError::Unauthorized);

    let amount = goal.funded_lamports;
    goal.released = true;

    **goal.to_account_info().try_borrow_mut_lamports()? -= amount;
    **ctx.accounts.traveler.try_borrow_mut_lamports()? += amount;

    emit!(GoalReleased {
        goal: goal.key(),
        traveler: goal.traveler,
        amount,
    });

    Ok(())
}

#[event]
pub struct GoalReleased {
    pub goal: Pubkey,
    pub traveler: Pubkey,
    pub amount: u64,
}
