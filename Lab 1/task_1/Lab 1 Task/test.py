import comparesignals
import  dsp

s1=dsp.read_signal('signal1.txt')

dsp.display_disc(s1)

dsp.display_continuous(s1)

x_sin = dsp.sin_signal(3,  1.96349540849362, 360, 720)

x_cos = dsp.cos_signal(3,  2.35619449019235, 200, 500)

comparesignals.SignalSamplesAreEqual('SinOutput.txt', x_sin[:, 0], x_sin[:, 1])

comparesignals.SignalSamplesAreEqual('CosOutput.txt', x_cos[:, 0], x_cos[:, 1])
