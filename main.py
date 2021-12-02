import numpy as np
import matplotlib.pyplot as plt
import numpy.random as nr
import numpy.linalg as nl

blockLength = 1000 # Number of symbol per block
nBlocks = 1000 # Number of blocks
Nr = 2 # 2 Receive antennas
Nt = 2 # 2 Transmit antennas
SNRdB = np.arange(1.0, 25.0, 1.0)  # SNR range in dB
BER = np.zeros(len(SNRdB))
BERt = np.zeros(len(SNRdB))
SNR = 10 ** (SNRdB / 10)  # Linear SNR

for blk in range(nBlocks):
    H = (nr.normal(0.0, 1.0, (Nr, Nt)) + 1j * nr.normal(0.0, 1.0, (Nr, Nt))) / np.sqrt(2) #  Fading channel coefficient
    noise = nr.normal(0.0, 1.0, (Nr, blockLength)) + 1j * nr.normal(0.0, 1.0, (Nr, blockLength))  # AWGN
    Sym = 2 * nr.randint(2, size=(Nt, blockLength)) - 1 # BPSK symbols
    for K in range(len(SNRdB)):
        TxBits = np.sqrt(SNR[K]) * Sym
        RxBits = np.matmul(H, TxBits) + noise  # Channel effects ( Fading + AWGN )
        ZFout = np.matmul(nl.pinv(H), RxBits)  # Zero-Forcing Equalizer
        DecBits = 2 * (np.real(ZFout) > 0) - 1 # 0 threshold detection
        BER[K] = BER[K] + np.sum(DecBits != Sym)

BER = BER / blockLength / nBlocks / Nt  # Calculate the BER
BERt = 1 / 2 * (1 - np.sqrt(SNR / (2 + SNR)))  # Theoretical BER
plt.yscale('log')
plt.plot(SNRdB, BER, 'g-')
plt.plot(SNRdB, BERt, 'ro')
plt.grid(1, which='both')
plt.suptitle('BER for MIMO Channel')
plt.legend(["Simulation", "Theory"], loc="lower left")
plt.xlabel('SNR (dB)')
plt.ylabel('BER')
plt.savefig('BER for MIMO Channel.png', dpi=300)
