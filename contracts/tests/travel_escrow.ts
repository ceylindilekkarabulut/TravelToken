import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { TravelEscrow } from "../target/types/travel_escrow";
import { assert } from "chai";

describe("travel_escrow", () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.TravelEscrow as Program<TravelEscrow>;

  it("Initializes a travel goal", async () => {
    const goalId = "test-goal-001";
    const [goalPda] = anchor.web3.PublicKey.findProgramAddressSync(
      [Buffer.from("goal"), Buffer.from(goalId)],
      program.programId
    );

    await program.methods
      .initializeGoal(goalId, new anchor.BN(1_000_000_000))
      .accounts({
        travelGoal: goalPda,
        traveler: provider.wallet.publicKey,
        authority: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .rpc();

    const goal = await program.account.travelGoal.fetch(goalPda);
    assert.equal(goal.goalId, goalId);
    assert.equal(goal.released, false);
  });
});
