use anchor_lang::prelude::*;

#[error_code]
pub enum TravelError {
    #[msg("Goal already released")]
    AlreadyReleased,
    #[msg("Not the authority")]
    Unauthorized,
    #[msg("Goal not fully funded")]
    NotFullyFunded,
    #[msg("Sponsorship already refunded")]
    AlreadyRefunded,
}
