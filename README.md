# MILP modeling the search for MITM preimage attack on round-reduced Whirlpool

This repository provides source codes as follows: 

* `MITM_MILP_Whirlpool.py` is for generating MILP models searching for MITM preimage attack on round-reduced Whirlpool

* `Drawer_MITM_MILP_Whirlpool.py` is for generating latex tikz codes to visualize the attack configurations obtained by solving the MILP models. 

Please refer to [\[1\]]( https://eprint.iacr.org/2021/575) for details of the MILP modeling.


## Remark

* In `Basic_Guess.py`, use `WhirlpoolParameters_small` (resp. `WhirlpoolParameters_half`, `WhirlpoolParameters_real`) to search for MITM attack configurations on $4 \times 4$ (resp.  $8 \times 4$, $8 \times 8$) state version. Attack configurations on $4 \times 4$ and $8 \times 4$ state versions can be projected to attacks on $8 \times 8$ state version according to the symmetry of the cipher (refer to [\[1\]]( https://eprint.iacr.org/2021/575)).


## References

[1] Zhenzhen Bao, Jian Guo, Danping Shi, and Yi Tu: Superposition Meet-in-the-Middle Attacks: Updates on Fundamental Security of AES-like Hashing. Cryptology ePrint Archive, Report 2021/575, 2021. https://eprint.iacr.org/2021/575
